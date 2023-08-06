"""Tests for storage.py."""
from pathlib import Path
import pickle
import re
from typing import Any, Callable, Dict, Literal, Mapping, Optional, Tuple, Union
from unittest.mock import Mock

import msgpack
import pytest
from pytest import fixture
from requests import HTTPError, PreparedRequest, RequestException
from requests_toolbelt import MultipartDecoder
import responses

from bitfount.storage import (
    _DEFAULT_FILE_NAME,
    _download_data_from_s3,
    _download_file_from_s3,
    _download_from_s3,
    _get_packed_data_object_size,
    _upload_data_to_s3,
    _upload_file_to_s3,
    _upload_to_s3,
)
from bitfount.types import _S3PresignedPOSTFields, _S3PresignedPOSTURL, _S3PresignedURL
from tests.utils.helper import unit_test

# Apply unit_test mark to all tests in file
pytestmark = unit_test


def multipart_or_form_data_matcher(
    data: Optional[Mapping[str, str]] = None,
    files: Optional[Mapping[Literal["file"], Tuple[str, bytes]]] = None,
) -> Callable[
    [PreparedRequest],
    Any,  # Actually Tuple[bool, str], but needs to be Any to match responses type hints # noqa: B950
]:
    """Custom `responses` matcher for file upload HTTP body."""
    # A multipart_matcher is included in responses>=0.16.0 but has a bug when
    # comparing non-UTF-8 strings (https://github.com/getsentry/responses/issues/443).
    # Can remove this custom matcher and use the provided one once that issue is
    # resolved.
    if not data:
        data = {}

    if not files:
        files = {}

    def match(request: PreparedRequest) -> Tuple[bool, str]:
        """Asserts that the expected fields are in the multipart data request body."""
        # Extract multipart data boundary
        try:
            content_type: str = request.headers["Content-Type"]
            if "multipart/form-data" not in content_type:
                raise TypeError("Request is not a multipart/form-data request.")
            boundary: str = content_type.split("boundary=")[1]
        except KeyError:
            return False, "Unable to extract Content-Type from request headers"
        except TypeError:
            # noinspection PyUnboundLocalVariable
            return (
                False,
                f'Wrong Content-Type; expected "multipart/form-data", '
                f"got {content_type}",
            )

        # Extract request body, convert to workable form
        request_body = request.body
        if not request_body:
            return False, "Request body is missing"
        if isinstance(request_body, str):
            # Need to work in bytes
            request_body = request_body.encode("utf-8")

        # Check data fields (i.e. uploadFields)
        assert data is not None
        for name, value in data.items():
            # TODO: [BIT-990] Expand this to handle the different formats that `value`
            #       can take in the `requests` `data` parameter.
            #       https://docs.python-requests.org/en/latest/api/#requests.request
            #       Only some of them are possible in multipart/form-data requests.
            # Build data content entry
            expected_part = str.encode(
                f"Content-Disposition: form-data; "
                f'name="{name}"'
                f"\r\n\r\n"
                f"{value}"
                f"\r\n"
                f"--{boundary}",
                encoding="utf-8",
            )

            if expected_part not in request_body:
                return (
                    False,
                    f"form-data for {{{name}: {value}}} was not found in the "
                    f"request body",
                )

        # Check files fields
        assert files is not None
        for name, (filename, file_contents) in files.items():
            # TODO: [BIT-990] Expand this to handle the different formats that `value`
            #       can take in the `requests` `file` parameter.
            #       https://docs.python-requests.org/en/latest/api/#requests.request
            # Build file content entry. Because file content may be bytes that
            # cannot be UTF-8 encoded we have to construct this manually.
            expected_part_start = str.encode(
                f"Content-Disposition: form-data; "
                f'name="{name}"; '
                f'filename="{filename}"'
                f"\r\n\r\n",
                encoding="utf-8",
            )
            expected_part_end = str.encode(f"\r\n--{boundary}", encoding="utf-8")
            expected_part = expected_part_start + file_contents + expected_part_end

            if expected_part not in request_body:
                return (
                    False,
                    f'form-data for file "{filename}" was not found in the request'
                    f" body.",
                )

        # If we've reached this point, everything looks good.
        return True, ""

    return match


@fixture
def data() -> Dict[str, Union[int, str]]:
    """Data to upload."""
    return {"this": "is", "some": "data", "object": 1}


@fixture
def packed_data(data: Dict[str, Union[int, str]]) -> bytes:
    """Data form when it has been packed by msgpack."""
    return msgpack.dumps(data)


@fixture
def file_name() -> str:
    """Filename for data file."""
    return "data_file.txt"


@fixture
def custom_filename() -> str:
    """Custom filename to use for tests."""
    return "custom_filename.txt"


@fixture
def data_file(data: Dict[str, Union[int, str]], file_name: str, tmp_path: Path) -> Path:
    """Data written out as pickled binary to a file."""
    data_file_path = tmp_path / file_name
    with open(data_file_path, "wb") as f:
        pickle.dump(data, f)
    return data_file_path


@fixture
def file_data(data_file: Path) -> bytes:
    """Pickled data form when packed by msgpack."""
    with open(data_file, "rb") as f:
        return f.read()


@fixture
def bad_response_text() -> str:
    """Body text for a bad response."""
    return "BAD BODY"


@responses.activate
def test__upload_to_s3(
    file_name: str,
    packed_data: bytes,
    s3_upload_fields: _S3PresignedPOSTFields,
    s3_upload_url: _S3PresignedPOSTURL,
) -> None:
    """Tests _upload_to_s3 works correctly.

    Data should be uploaded with the expected fields.
    """
    responses.add(
        method=responses.POST,
        url=s3_upload_url,
        match=[
            multipart_or_form_data_matcher(
                data=s3_upload_fields, files={"file": (file_name, packed_data)}
            )
        ],
    )

    _upload_to_s3(
        s3_upload_url, s3_upload_fields, to_upload=packed_data, file_name=file_name
    )


@responses.activate
def test__upload_to_s3_default_file_name(
    packed_data: bytes,
    s3_upload_fields: _S3PresignedPOSTFields,
    s3_upload_url: _S3PresignedPOSTURL,
) -> None:
    """Tests _upload_to_s3 works correctly.

    Data should be uploaded with the expected fields.
    """
    responses.add(
        method=responses.POST,
        url=s3_upload_url,
        match=[
            multipart_or_form_data_matcher(
                data=s3_upload_fields, files={"file": (_DEFAULT_FILE_NAME, packed_data)}
            )
        ],
    )

    _upload_to_s3(s3_upload_url, s3_upload_fields, to_upload=packed_data)


@responses.activate
def test__upload_to_s3_file_handler(
    packed_data: bytes,
    s3_upload_fields: _S3PresignedPOSTFields,
    s3_upload_url: _S3PresignedPOSTURL,
    tmp_path: Path,
) -> None:
    """Tests _upload_to_s3 works correctly.

    Data should be uploaded with the expected fields.
    """
    with open(tmp_path / "packed_data", "wb") as f:
        f.write(packed_data)

    responses.add(
        method=responses.POST,
        url=s3_upload_url,
        match=[
            multipart_or_form_data_matcher(
                data=s3_upload_fields, files={"file": (_DEFAULT_FILE_NAME, packed_data)}
            )
        ],
    )

    with open(tmp_path / "packed_data", "rb") as f:
        _upload_to_s3(s3_upload_url, s3_upload_fields, to_upload=f)


@responses.activate
def test__upload_to_s3_failure_request_exception(
    packed_data: bytes,
    s3_upload_fields: _S3PresignedPOSTFields,
    s3_upload_url: _S3PresignedPOSTURL,
) -> None:
    """Tests _upload_to_s3 fails when RequestException encountered."""
    responses.add(
        method=responses.POST,
        url=s3_upload_url,
        match=[
            multipart_or_form_data_matcher(
                data=s3_upload_fields, files={"file": (_DEFAULT_FILE_NAME, packed_data)}
            )
        ],
        body=RequestException(),
    )

    # Error message
    with pytest.raises(RequestException, match="Issue uploading object to S3$"):
        _upload_to_s3(s3_upload_url, s3_upload_fields, packed_data)


@responses.activate
def test__upload_to_s3_failure_status_code(
    bad_response_text: str,
    packed_data: bytes,
    s3_upload_fields: _S3PresignedPOSTFields,
    s3_upload_url: _S3PresignedPOSTURL,
) -> None:
    """Tests _upload_to_s3 fails when status code is 400+."""
    responses.add(
        method=responses.POST,
        url=s3_upload_url,
        match=[
            multipart_or_form_data_matcher(
                data=s3_upload_fields, files={"file": (_DEFAULT_FILE_NAME, packed_data)}
            )
        ],
        status=400,
        body=bad_response_text,
    )

    with pytest.raises(
        HTTPError,
        match=re.escape(f"Issue uploading object to S3: (400) {bad_response_text}"),
    ):
        _upload_to_s3(s3_upload_url, s3_upload_fields, packed_data)


@responses.activate
def test__upload_to_s3_failure_non_ok_status_code(
    bad_response_text: str,
    packed_data: bytes,
    s3_upload_fields: _S3PresignedPOSTFields,
    s3_upload_url: _S3PresignedPOSTURL,
) -> None:
    """Tests _upload_to_s3 fails when status code is not 200 or 201."""
    responses.add(
        method=responses.POST,
        url=s3_upload_url,
        match=[
            multipart_or_form_data_matcher(
                data=s3_upload_fields, files={"file": (_DEFAULT_FILE_NAME, packed_data)}
            )
        ],
        status=300,
        body=bad_response_text,
    )

    with pytest.raises(
        HTTPError,
        match=re.escape(f"Issue uploading object to S3: (300) {bad_response_text}"),
    ):
        _upload_to_s3(s3_upload_url, s3_upload_fields, packed_data)


@responses.activate
def test_upload_data_to_s3(
    data: Dict[str, Union[int, str]],
    packed_data: bytes,
    s3_upload_fields: _S3PresignedPOSTFields,
    s3_upload_url: _S3PresignedPOSTURL,
) -> None:
    """Tests upload_data_to_s3 works correctly.

    Data should be packed and uploaded with the expected fields.
    """
    responses.add(
        method=responses.POST,
        url=s3_upload_url,
        match=[
            multipart_or_form_data_matcher(
                data=s3_upload_fields, files={"file": (_DEFAULT_FILE_NAME, packed_data)}
            )
        ],
    )

    _upload_data_to_s3(s3_upload_url, s3_upload_fields, data=data)


@responses.activate
def test_upload_file_to_s3_with_path(
    data_file: Path,
    file_data: bytes,
    s3_upload_fields: _S3PresignedPOSTFields,
    s3_upload_url: _S3PresignedPOSTURL,
) -> None:
    """Tests upload_file_to_s3 works with file path."""
    responses.add(
        method=responses.POST,
        url=s3_upload_url,
        match=[
            multipart_or_form_data_matcher(
                data=s3_upload_fields,
                files={"file": (data_file.name, file_data)},
            )
        ],
    )

    _upload_file_to_s3(s3_upload_url, s3_upload_fields, file_path=data_file)


@responses.activate
def test_upload_file_to_s3_with_path_and_file_name(
    custom_filename: str,
    data_file: Path,
    file_data: bytes,
    s3_upload_fields: _S3PresignedPOSTFields,
    s3_upload_url: _S3PresignedPOSTURL,
) -> None:
    """Tests upload_file_to_s3 works with file path and custom filename."""
    responses.add(
        method=responses.POST,
        url=s3_upload_url,
        match=[
            multipart_or_form_data_matcher(
                data=s3_upload_fields,
                files={"file": (custom_filename, file_data)},
            )
        ],
    )

    _upload_file_to_s3(
        s3_upload_url, s3_upload_fields, file_path=data_file, file_name=custom_filename
    )


@responses.activate
def test_upload_file_to_s3_with_str_file_contents(
    s3_upload_fields: _S3PresignedPOSTFields, s3_upload_url: _S3PresignedPOSTURL
) -> None:
    """Tests upload_file_to_s3 works with string file-contents."""
    str_contents: str = "Hello, world!"
    bytes_contents: bytes = str_contents.encode("utf-8")

    responses.add(
        method=responses.POST,
        url=s3_upload_url,
        match=[
            multipart_or_form_data_matcher(
                data=s3_upload_fields,
                files={"file": (_DEFAULT_FILE_NAME, bytes_contents)},
            )
        ],
    )

    _upload_file_to_s3(s3_upload_url, s3_upload_fields, file_contents=str_contents)


@responses.activate
def test_upload_file_to_s3_with_str_file_contents_and_custom_filename(
    custom_filename: str,
    s3_upload_fields: _S3PresignedPOSTFields,
    s3_upload_url: _S3PresignedPOSTURL,
) -> None:
    """Tests upload_file_to_s3 works with string file-contents and custom filename."""
    str_contents: str = "Hello, world!"
    bytes_contents: bytes = str_contents.encode("utf-8")

    responses.add(
        method=responses.POST,
        url=s3_upload_url,
        match=[
            multipart_or_form_data_matcher(
                data=s3_upload_fields,
                files={"file": (custom_filename, bytes_contents)},
            )
        ],
    )

    _upload_file_to_s3(
        s3_upload_url,
        s3_upload_fields,
        file_contents=str_contents,
        file_name=custom_filename,
    )


@responses.activate
def test_upload_file_to_s3_with_str_file_contents_and_non_standard_encoding(
    s3_upload_fields: _S3PresignedPOSTFields, s3_upload_url: _S3PresignedPOSTURL
) -> None:
    """Tests upload_file_to_s3 works with string file-contents and encoding."""
    str_contents: str = "Hello, world!"
    encoding = "ascii"
    bytes_contents: bytes = str_contents.encode(encoding)

    responses.add(
        method=responses.POST,
        url=s3_upload_url,
        match=[
            multipart_or_form_data_matcher(
                data=s3_upload_fields,
                files={"file": (_DEFAULT_FILE_NAME, bytes_contents)},
            )
        ],
    )

    _upload_file_to_s3(
        s3_upload_url,
        s3_upload_fields,
        file_contents=str_contents,
        file_encoding=encoding,
    )


@responses.activate
def test_upload_file_to_s3_with_bytes_file_contents(
    s3_upload_fields: _S3PresignedPOSTFields, s3_upload_url: _S3PresignedPOSTURL
) -> None:
    """Tests upload_file_to_s3 works with bytes file-contents."""
    bytes_contents: bytes = b"Hello World!"

    responses.add(
        method=responses.POST,
        url=s3_upload_url,
        match=[
            multipart_or_form_data_matcher(
                data=s3_upload_fields,
                files={"file": (_DEFAULT_FILE_NAME, bytes_contents)},
            )
        ],
    )

    _upload_file_to_s3(s3_upload_url, s3_upload_fields, file_contents=bytes_contents)


@responses.activate
def test_upload_file_to_s3_with_bytes_file_contents_and_custom_filename(
    custom_filename: str,
    s3_upload_fields: _S3PresignedPOSTFields,
    s3_upload_url: _S3PresignedPOSTURL,
) -> None:
    """Tests upload_file_to_s3 works with bytes file-contents and custom filename."""
    bytes_contents: bytes = b"Hello World!"

    responses.add(
        method=responses.POST,
        url=s3_upload_url,
        match=[
            multipart_or_form_data_matcher(
                data=s3_upload_fields,
                files={"file": (custom_filename, bytes_contents)},
            )
        ],
    )

    _upload_file_to_s3(
        s3_upload_url,
        s3_upload_fields,
        file_contents=bytes_contents,
        file_name=custom_filename,
    )


@responses.activate
def test_upload_file_to_s3_fails_if_contents_and_path_provided(
    s3_upload_fields: _S3PresignedPOSTFields, s3_upload_url: _S3PresignedPOSTURL
) -> None:
    """Tests upload_file_to_s3 fails if incompatible args."""
    with pytest.raises(
        ValueError,
        match=re.escape(
            "One of file_path and file_contents must be provided, but not both."
        ),
    ):
        _upload_file_to_s3(
            s3_upload_url, s3_upload_fields, file_path=Mock(), file_contents=Mock()
        )


@responses.activate
def test__download_from_s3(
    packed_data: bytes, s3_download_url: _S3PresignedURL
) -> None:
    """Tests _download_from_s3 works.

    Should download data, which will match the original data.
    """
    responses.add(
        method=responses.GET,
        url=s3_download_url,
        body=packed_data,
    )

    downloaded_data = _download_from_s3(s3_download_url)

    assert downloaded_data == packed_data


@responses.activate
def test__download_from_s3_fails_request_exception(
    s3_download_url: _S3PresignedURL,
) -> None:
    """Tests _download_from_s3 fails when RequestException encountered."""
    responses.add(
        method=responses.GET,
        url=s3_download_url,
        body=RequestException(),
    )

    with pytest.raises(RequestException, match="Issue whilst retrieving data from S3$"):
        _download_from_s3(s3_download_url)


@responses.activate
def test__download_from_s3_fails_status_code_bad(
    bad_response_text: str, s3_download_url: _S3PresignedURL
) -> None:
    """Tests _download_from_s3 fails when status code is 400+."""
    responses.add(
        method=responses.GET,
        url=s3_download_url,
        status=500,
        body=bad_response_text,
    )

    with pytest.raises(
        HTTPError,
        match=re.escape(
            f"Issue whilst retrieving data from S3: (500) {bad_response_text}"
        ),
    ):
        _download_from_s3(s3_download_url)


@responses.activate
def test__download_from_s3_fails_status_code_not_good(
    bad_response_text: str, s3_download_url: _S3PresignedURL
) -> None:
    """Tests _download_from_s3 fails when status code is not 200/201."""
    responses.add(
        method=responses.GET,
        url=s3_download_url,
        status=202,
        body=bad_response_text,
    )

    with pytest.raises(
        HTTPError,
        match=re.escape(
            f"Issue whilst retrieving data from S3: (202) {bad_response_text}"
        ),
    ):
        _download_from_s3(s3_download_url)


@responses.activate
def test_download_data_from_s3(
    data: Dict[str, Union[int, str]],
    packed_data: bytes,
    s3_download_url: _S3PresignedURL,
) -> None:
    """Tests download_data_from_s3 works correctly.

    Data should be unpacked upon retrieval.
    """
    responses.add(
        method=responses.GET,
        url=s3_download_url,
        body=packed_data,
    )

    downloaded_data = _download_data_from_s3(s3_download_url)

    # Check was unpacked
    assert downloaded_data == data


@responses.activate
def test_download_file_from_s3(
    packed_data: bytes, s3_download_url: _S3PresignedURL
) -> None:
    """Tests download_file_from_s3 works correctly.

    Data should be downloaded as is, and not encoded.
    """
    responses.add(
        method=responses.GET,
        url=s3_download_url,
        body=packed_data,
    )

    downloaded_data = _download_file_from_s3(s3_download_url)

    # Check was unpacked
    assert downloaded_data == packed_data


@responses.activate
def test_download_file_from_s3_with_encoding(s3_download_url: _S3PresignedURL) -> None:
    """Tests download_file_from_s3 works correctly with encoding.

    Retrieved data should be encoded as a string.
    """
    str_contents: str = "Hello, world!"
    bytes_contents: bytes = str_contents.encode("utf-8")

    responses.add(
        method=responses.GET,
        url=s3_download_url,
        body=bytes_contents,
    )

    downloaded_data = _download_file_from_s3(s3_download_url, encoding="utf-8")

    # Check was encoded correctly
    assert isinstance(downloaded_data, str)
    assert downloaded_data == str_contents


def test_get_packed_data_object_size(
    data: Dict[str, Union[int, str]], packed_data: bytes
) -> None:
    """Tests that get_packed_data_object_size works correctly."""
    expected_length = len(packed_data)

    assert _get_packed_data_object_size(data) == expected_length


@responses.activate
def test_get_packed_data_object_size_corresponds_to_upload(
    data: Dict[str, Union[int, str]],
    packed_data: bytes,
    s3_upload_fields: _S3PresignedPOSTFields,
    s3_upload_url: _S3PresignedPOSTURL,
) -> None:
    """Tests that get_packed_data_object_size matches upload size."""
    # Get output size and check it matches the packed data
    expected_length = _get_packed_data_object_size(data)
    assert len(packed_data) == expected_length

    # Do mocked upload to give us the request
    responses.add(
        method=responses.POST,
        url=s3_upload_url,
    )
    _upload_data_to_s3(s3_upload_url, s3_upload_fields, data)

    # Check request file size as actually uploaded
    request = responses.calls[0].request
    file_contents: Optional[bytes] = None
    # Extract file content bytes from the multipart/form-data request body
    mpd = MultipartDecoder(request.body, content_type=request.headers["content-type"])
    # Find the file part of the body (will have "filename" in the disposition)
    for part in mpd.parts:
        content_disposition: bytes = part.headers[b"Content-Disposition"]
        if b"filename" in content_disposition:
            file_contents = part.content

    # Check that bytes length in request body matches expected_length
    assert file_contents is not None
    assert len(file_contents) == expected_length
