"""Classes and functions for handling interaction with online storage services."""
import logging
import os
from pathlib import Path
from typing import Any, BinaryIO, Final, List, Optional, Tuple, Union

import msgpack
import requests
from requests import HTTPError, RequestException, Response

from bitfount.types import _S3PresignedPOSTFields, _S3PresignedPOSTURL, _S3PresignedURL

__all__: List[str] = []

logger = logging.getLogger(__name__)

# This forces `requests` to make IPv4 connections
# TODO: [BIT-1443] Remove this once Hub/AM support IPv6
requests.packages.urllib3.util.connection.HAS_IPV6 = False  # type: ignore[attr-defined] # Reason: see above # noqa: B950


# Status codes that we consider as OK responses for upload
_OK_UPLOAD_STATUS_CODES: Tuple[int, ...] = (200, 201, 203, 204)
# Status codes that we consider as OK responses for download
_OK_DOWNLOAD_STATUS_CODES: Tuple[int, ...] = (200,)

_DEFAULT_FILE_NAME: Final[str] = "bitfount_file"


def _handle_request_exception(
    exc: RequestException, response: Optional[Response], err_message: str
) -> None:
    """Handles request exceptions in storage functions."""
    # Explicit None check needed due to truthyness of Response objects
    if response is not None:
        err_message += f": ({response.status_code})"
        if response.text:
            err_message += f" {response.text}"
    # Raise same type as what was passed in
    raise type(exc)(err_message) from exc


def _upload_to_s3(
    upload_url: _S3PresignedPOSTURL,
    presigned_fields: _S3PresignedPOSTFields,
    to_upload: Union[bytes, BinaryIO],
    file_name: str = _DEFAULT_FILE_NAME,
) -> None:
    """Base s3 upload function.

    Handles the upload and response.
    """
    try:
        response = requests.post(
            url=upload_url,
            data=presigned_fields,
            files={"file": (file_name, to_upload)},
        )

        response.raise_for_status()

        if response.status_code not in _OK_UPLOAD_STATUS_CODES:
            raise HTTPError(f"Response not OK; not one of {_OK_UPLOAD_STATUS_CODES}")
    except RequestException as ex:
        try:
            # noinspection PyUnboundLocalVariable
            err_response: Optional[Response] = response
        except NameError:
            # response variable wasn't created yet
            err_response = None
        _handle_request_exception(ex, err_response, "Issue uploading object to S3")


def _upload_data_to_s3(
    upload_url: _S3PresignedPOSTURL,
    presigned_fields: _S3PresignedPOSTFields,
    data: Any,
) -> None:
    """Uploads an object to an s3 presigned POST url.

    Data will be packed via msgpack automatically before upload.

    Args:
        upload_url: The s3 presigned URL to upload to.
        presigned_fields: The additional fields needed to upload to the presigned
                          URL. These are provided when the presigned URL is created.
        data: The data to upload.

    Raises:
        HTTPError: If the response code is not 200 or 201.
        RequestException: If the response is not OK for another reason.
    """
    packed_data: bytes = msgpack.dumps(data)
    _upload_to_s3(upload_url, presigned_fields, packed_data)


def _upload_file_to_s3(
    upload_url: _S3PresignedPOSTURL,
    presigned_fields: _S3PresignedPOSTFields,
    file_path: Optional[Union[str, os.PathLike]] = None,
    file_contents: Optional[Union[str, bytes]] = None,
    file_encoding: str = "utf-8",
    file_name: Optional[str] = None,
) -> None:
    """Uploads a file to an s3 presigned POST url.

    The file is read and uploaded in binary mode as this is recommended for
    `requests.post()`.

    Args:
        upload_url: The s3 presigned URL to upload to.
        presigned_fields: The additional fields needed to upload to the presigned
                          URL. These are provided when the presigned URL is created.
        file_path: The path to the file to be uploaded. Cannot be provided if
                   file_contents is.
        file_contents: The contents of a file to be uploaded. Cannot be provided
                       if file_path is.
        file_encoding: The encoding to use to convert string file contents to bytes.
        file_name: The name to upload the file with. Optional, default will be extracted
                  automatically if using file_path, and use a default filename
                  if using file_contents.

    Raises:
        HTTPError: If the response code is not 200 or 201.
        RequestException: If the response is not OK for another reason.
    """
    if bool(file_path) == bool(file_contents):
        raise ValueError(
            "One of file_path and file_contents must be provided, but not both."
        )

    # Handle if file_path provided
    if file_path:
        file_path = Path(file_path)

        # Use file's name if one not provided
        if not file_name:
            file_name = file_path.name

        with open(file_path, "rb") as f:
            _upload_to_s3(upload_url, presigned_fields, f, file_name)

    # Handle if file_contents provided
    if file_contents:
        # Use default filename if one not provided
        if not file_name:
            file_name = _DEFAULT_FILE_NAME

        # Convert to bytes as this is what's supported in `requests.post()`
        if isinstance(file_contents, str):
            file_contents = file_contents.encode(file_encoding)

        _upload_to_s3(upload_url, presigned_fields, file_contents, file_name)


def _download_from_s3(download_url: _S3PresignedURL) -> bytes:
    """Base s3 download function.

    Handles the download and response parsing.
    """
    try:
        response = requests.get(url=download_url)

        response.raise_for_status()

        if response.status_code not in _OK_DOWNLOAD_STATUS_CODES:
            raise HTTPError(f"Response not OK; not one of {_OK_UPLOAD_STATUS_CODES}")
    except RequestException as ex:
        try:
            # noinspection PyUnboundLocalVariable
            err_response: Optional[Response] = response
        except NameError:
            # response variable wasn't created yet
            err_response = None
        _handle_request_exception(
            ex, err_response, "Issue whilst retrieving data from S3"
        )
    return response.content


def _download_data_from_s3(download_url: _S3PresignedURL) -> Any:
    """Downloads data from the specified s3 URL.

    Will unpack the data using msgpack.

    Args:
        download_url: The s3 URL to download the data from.

    Raises:
        HTTPError: If the response code is not 200.
        RequestException: If the response is not OK.
    """
    data: bytes = _download_from_s3(download_url)
    return msgpack.loads(data)


def _download_file_from_s3(
    download_url: _S3PresignedURL, encoding: Optional[str] = None
) -> Union[str, bytes]:
    """Downloads a file from the specified s3 URL.

    Args:
        download_url: The s3 URL to download the data from.
        encoding: Optional. A string encoding to use to decode the data.

    Returns:
        The file contents, as a string if `encoding` provided otherwise as bytes.

    Raises:
        HTTPError: If the response code is not 200.
        RequestException: If the response is not OK.
    """
    data: bytes = _download_from_s3(download_url)
    if encoding:
        return data.decode(encoding)
    else:
        return data


def _get_packed_data_object_size(data: Any) -> int:
    """Get the size of a packed object as it will be uploaded to S3.

    Args:
        data: The object that will be uploaded to S3.

    Returns:
        The size of the packed object in bytes.
    """
    packed: bytes = msgpack.dumps(data)
    return len(packed)
