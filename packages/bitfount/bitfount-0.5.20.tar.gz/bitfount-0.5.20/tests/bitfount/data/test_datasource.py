"""Tests datasource.py."""
from functools import partial
import logging
from pathlib import Path
import re
from typing import Callable, Iterator, Optional, Tuple
from unittest.mock import Mock

from _pytest.logging import LogCaptureFixture
import numpy as np
import pandas as pd
import pytest
from pytest import fixture
from pytest_mock import MockerFixture
import sqlalchemy

from bitfount.data.datasource import (
    CSVLoader,
    DatabaseLoader,
    DataFrameLoader,
    DataSource,
)
from bitfount.data.datasplitters import (
    DatasetSplitter,
    PercentageSplitter,
    SplitterDefinedInData,
)
from bitfount.data.exceptions import DataNotLoadedError
from bitfount.data.types import DataPathModifiers, DataSplit
from bitfount.data.utils import DatabaseConnection, _hash_str
from tests.utils import PytestRequest
from tests.utils.helper import (
    DATASET_ROW_COUNT,
    create_dataset,
    integration_test,
    unit_test,
)


@fixture
def dataframe() -> pd.DataFrame:
    """Dataframe fixture."""
    return create_dataset()


class FakeSplitter(DatasetSplitter):
    """Fake Splitter that just returns predefined indices."""

    def __init__(
        self,
        train_indices: np.ndarray,
        validation_indices: np.ndarray,
        test_indices: np.ndarray,
    ):
        self.train_indices = train_indices
        self.validation_indices = validation_indices
        self.test_indices = test_indices

    @classmethod
    def splitter_name(cls) -> str:
        """Splitter name for config."""
        return "FakeSplitter"

    def create_dataset_splits(
        self, data: pd.DataFrame
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Returns predefined indices and provided data."""
        return self.train_indices, self.validation_indices, self.test_indices

    def get_split_query(self, loader: DatabaseLoader, split: DataSplit) -> str:
        """Returns query for given split."""
        ...


@unit_test
class TestDataSource:
    """Tests core DataSource functionality with a CSV file."""

    @fixture(scope="function", params=["pandas", "image"])
    def datasource_generator(self, request: PytestRequest) -> Callable[..., DataSource]:
        """Dataset loader for use in tests."""
        image = False
        if request.param == "image":
            image = True
        data = create_dataset(image=image)
        if image:
            return partial(DataSource, data_ref=data, seed=420)

        return partial(DataSource, data_ref=data, seed=420)

    def test_training_set(
        self,
        datasource_generator: Callable[..., DataSource],
    ) -> None:
        """Checks training set is behaving correctly."""
        test_percentage = 25
        validation_percentage = 55
        train_percentage = (100 - test_percentage) - validation_percentage
        data_source = datasource_generator(
            data_splitter=FakeSplitter(
                np.array(range(int(DATASET_ROW_COUNT * (train_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (validation_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (test_percentage / 100)))),
            )
        )
        data_source.load_data()
        data_source._split_data()
        # assert columns match the original data
        assert (
            data_source.data.shape[1]
            == data_source.get_dataset_split(DataSplit.TRAIN).shape[1]
        )
        # assert there are the expected number of rows
        assert (
            int(train_percentage * data_source.data.shape[0] / 100)
            == data_source.get_dataset_split(DataSplit.TRAIN).shape[0]
        )

    def test_validation_set(
        self,
        datasource_generator: Callable[..., DataSource],
    ) -> None:
        """Checks validation set is behaving correctly."""
        test_percentage = 25
        validation_percentage = 55
        train_percentage = (100 - test_percentage) - validation_percentage
        data_source = datasource_generator(
            data_splitter=FakeSplitter(
                np.array(range(int(DATASET_ROW_COUNT * (train_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (validation_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (test_percentage / 100)))),
            )
        )
        data_source.load_data()
        data_source._split_data()
        # assert columns match the original data
        assert (
            data_source.data.shape[1]
            == data_source.get_dataset_split(DataSplit.VALIDATION).shape[1]
        )
        # assert there are the expected number of rows
        assert (
            int(validation_percentage * data_source.data.shape[0] / 100)
            == data_source.get_dataset_split(DataSplit.VALIDATION).shape[0]
        )

    def test_test_set(
        self,
        datasource_generator: Callable[..., DataSource],
    ) -> None:
        """Checks test set is behaving correctly."""
        test_percentage = 25
        validation_percentage = 55
        train_percentage = (100 - test_percentage) - validation_percentage
        data_source = datasource_generator(
            data_splitter=FakeSplitter(
                np.array(range(int(DATASET_ROW_COUNT * (train_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (validation_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (test_percentage / 100)))),
            )
        )
        data_source.load_data()
        data_source._split_data()
        # assert columns match the original data
        assert (
            data_source.data.shape[1]
            == data_source.get_dataset_split(DataSplit.TEST).shape[1]
        )
        # assert there are the expected number of rows
        assert (
            int(test_percentage * data_source.data.shape[0] / 100)
            == data_source.get_dataset_split(DataSplit.TEST).shape[0]
        )

    def test_zero_validation_test_size(
        self,
        datasource_generator: Callable[..., DataSource],
    ) -> None:
        """Checks Dataset object behaves properly when if valid and test pct are 0."""
        data_source = datasource_generator(
            data_splitter=FakeSplitter(
                train_indices=np.array(range(DATASET_ROW_COUNT)),
                validation_indices=np.array([]),
                test_indices=np.array([]),
            )
        )
        data_source.load_data()
        data_source._split_data()
        assert len(data_source.data) == len(
            data_source.get_dataset_split(DataSplit.TRAIN)
        )
        assert data_source._test_idxs is not None
        assert data_source._validation_idxs is not None
        assert len(data_source._test_idxs) == 0
        assert len(data_source._validation_idxs) == 0

    def test_tabular_datasource_errors(self) -> None:
        """Checks DataSource object errors via wrong first argument."""
        with pytest.raises(TypeError):
            DataSource("test1", seed=420).load_data()  # type: ignore[arg-type] # Reason: purpose of test # noqa: B950

        with pytest.raises(TypeError):
            test_path = Path("/my/root/directory")
            DataSource(test_path, seed=420).load_data()

    def test_datasource_modifiers_path_prefix(self, dataframe: pd.DataFrame) -> None:
        """Tests functionality for providing image path prefix."""
        dataframe["image"] = "image_file_name"
        modifiers = {"image": DataPathModifiers({"prefix": "/path/to/"})}
        datasource = DataSource(data_ref=dataframe, seed=420, modifiers=modifiers)
        datasource.load_data()
        assert len(datasource.data["image"].unique()) == 1
        assert datasource.data["image"].unique()[0] == "/path/to/image_file_name"

    def test_image_datasource_ext_suffix(self, dataframe: pd.DataFrame) -> None:
        """Tests functionality for finding images by file extension."""
        dataframe["image"] = "image_file_name"
        modifiers = {"image": DataPathModifiers({"suffix": ".jpeg"})}
        datasource = DataSource(data_ref=dataframe, seed=420, modifiers=modifiers)
        datasource.load_data()
        assert len(datasource.data["image"].unique()) == 1
        assert datasource.data["image"].unique()[0] == "image_file_name.jpeg"

    def test_image_datasource_ext_prefix_suffix(self, dataframe: pd.DataFrame) -> None:
        """Tests functionality for finding images by file extension."""
        dataframe["image"] = "image_file_name"
        modifiers = {
            "image": DataPathModifiers({"prefix": "/path/to/", "suffix": ".jpeg"})
        }
        datasource = DataSource(data_ref=dataframe, seed=420, modifiers=modifiers)
        datasource.load_data()
        assert len(datasource.data["image"].unique()) == 1
        assert datasource.data["image"].unique()[0] == "/path/to/image_file_name.jpeg"

    def test_multiple_img_datasource_modifiers(self) -> None:
        """Tests functionality for finding multiple images by file extension."""
        data = create_dataset(multiimage=True, img_size=1)
        data["image1"] = "image1_file_name"
        data["image2"] = "image2_file_name"
        modifiers = {
            "image1": DataPathModifiers({"prefix": "/path/to/"}),
            "image2": DataPathModifiers({"suffix": ".jpeg"}),
        }
        datasource = DataSource(data_ref=data, seed=420, modifiers=modifiers)
        datasource.load_data()
        assert len(datasource.data["image1"].unique()) == 1
        assert datasource.data["image1"].unique()[0] == "/path/to/image1_file_name"
        assert len(datasource.data["image2"].unique()) == 1
        assert datasource.data["image2"].unique()[0] == "image2_file_name.jpeg"

    def test_tabular_datasource_read_csv_correctly(
        self, dataframe: pd.DataFrame, tmp_path: Path
    ) -> None:
        """Tests DataSource loading from csv."""
        file_path = tmp_path / "tabular_data_test.csv"
        dataframe.to_csv(file_path)
        ds = DataSource(file_path)
        ds.load_data()
        assert hasattr(ds, "data")

    def test_ignored_cols_list_excluded_from_df(self, dataframe: pd.DataFrame) -> None:
        """Tests that a list of ignore_cols are ignored in the data."""
        dataframe["image"] = "image_file_name"
        ignore_cols = ["N", "O", "P"]
        datasource = DataSource(
            data_ref=dataframe,
            seed=420,
            ignore_cols=ignore_cols,
            image_col=["image"],
            image_extension="jpeg",
        )
        datasource.load_data()
        assert not any(item in datasource.data.columns for item in ignore_cols)

    def test_ignored_single_col_list_excluded_from_df(
        self, dataframe: pd.DataFrame
    ) -> None:
        """Tests that a str ignore_cols is ignored in the data."""
        dataframe["image"] = "image_file_name"
        ignore_cols = "N"
        datasource = DataSource(
            data_ref=dataframe,
            seed=420,
            ignore_cols=ignore_cols,
            image_col=["image"],
            image_extension="jpeg",
        )
        datasource.load_data()
        assert ignore_cols not in datasource.data.columns

    def test_hash(
        self, datasource_generator: Callable[..., DataSource], mocker: MockerFixture
    ) -> None:
        """Tests hash is called on the dtypes."""
        datasource = datasource_generator()
        expected_hash = f"hash_{id(datasource._table_hashes)}"
        mock_hash_function: Mock = mocker.patch(
            "bitfount.data.datasource._generate_dtypes_hash",
            return_value=expected_hash,
            autospec=True,
        )
        datasource.get_dtypes()

        actual_hash = datasource.hash

        # Check hash is expected return and how it was called
        assert actual_hash == _hash_str(str([expected_hash]))
        mock_hash_function.assert_called_once()

    def test_datasource_data_split_flag_updated(self, dataframe: pd.DataFrame) -> None:
        """Tests that the data_is_split flag is updated."""
        ds = DataSource(dataframe, selected_cols=["M", "F"])
        ds.load_data()
        assert ds._data_is_split is False
        # split data in DataBunch into training, validation, test sets
        ds._split_data()
        assert ds._data_is_split is True

    def test_datasource_data_split_called_twice(
        self, caplog: LogCaptureFixture, dataframe: pd.DataFrame
    ) -> None:
        """Tests that the log is printed if split_data called twice."""
        caplog.set_level(logging.DEBUG)
        ds = DataSource(dataframe, selected_cols=["M", "F"])
        ds.load_data()
        assert ds._data_is_split is False
        # split data in DataBunch into training, validation, test sets
        ds._split_data()
        assert ds._data_is_split is True
        # split data in DataBunch into training, validation, test sets
        ds._split_data()
        assert "Data is already split, keeping the current split." in caplog.text

    @pytest.mark.parametrize(
        "datasource_splitter, datastructure_splitter",
        [
            (PercentageSplitter(), PercentageSplitter()),
            (PercentageSplitter(), None),
            (None, PercentageSplitter()),
            (None, None),
        ],
    )
    def test_resolve_data_splitter(
        self,
        dataframe: pd.DataFrame,
        datasource_splitter: Optional[DatasetSplitter],
        datastructure_splitter: Optional[DatasetSplitter],
    ) -> None:
        """Checks data splitter is resolved correctly.

        If datasource has a data_splitter, use it to split the data.
        Else if the datastructure has a data_splitter use that splitter.
        Else use the PercentageSplitter.
        """
        datasource = DataSource(dataframe, data_splitter=datasource_splitter)
        resolved_splitter = datasource._resolve_data_splitter(datastructure_splitter)
        assert isinstance(resolved_splitter, PercentageSplitter)

        if datasource_splitter:
            assert datasource.data_splitter is not None
            assert resolved_splitter is datasource.data_splitter
            assert resolved_splitter is not datastructure_splitter
        elif datastructure_splitter:
            assert datasource.data_splitter is None
            assert resolved_splitter is datastructure_splitter
        else:
            assert resolved_splitter is not datastructure_splitter
            assert resolved_splitter is not datasource_splitter

    def test_get_dataset_split_length_raises_value_error(
        self, dataframe: pd.DataFrame
    ) -> None:
        """Tests that a DataNotLoadedError is raised in `get_dataset_split_length`.

        This happens if the split length can't be retrieved because the data hasn't
        been loaded yet.
        """
        dataframe["BITFOUNT_SPLIT_CATEGORY"] = np.random.choice(
            ["TRAIN", "VALIDATE", "TEST"], size=dataframe.shape[0]
        )

        ds = DataSource(dataframe, data_splitter=SplitterDefinedInData())

        with pytest.raises(
            DataNotLoadedError, match="Unable to get length of dataset split"
        ):
            # ds.load_data() # Data has not been loaded yet
            ds.get_dataset_split_length(DataSplit.TRAIN)

    def test_get_dataset_split_length_returns_length_correctly(
        self, dataframe: pd.DataFrame
    ) -> None:
        """Tests that `get_dataset_split_length` returns the correct length.

        This is done with the `SplitterDefinedInData` splitter.
        """
        dataframe["BITFOUNT_SPLIT_CATEGORY"] = np.random.choice(
            ["TRAIN", "VALIDATE", "TEST"], size=dataframe.shape[0]
        )

        ds = DataSource(dataframe, data_splitter=SplitterDefinedInData())
        ds.load_data()
        train_length = ds.get_dataset_split_length(DataSplit.TRAIN)
        assert train_length == len(
            dataframe.loc[dataframe["BITFOUNT_SPLIT_CATEGORY"] == "TRAIN"]
        )


class TestDatabaseConnectionDataSource:
    """Tests DataSource with a DatabaseConnection."""

    @unit_test
    def test_get_dataset_split_length_with_mock_multitable_database_connection(
        self, dataframe: pd.DataFrame, mock_engine: Mock, mocker: MockerFixture
    ) -> None:
        """Tests that `get_dataset_split_length` returns the correct length."""
        mock_db_connection = Mock()
        mock_result = Mock()
        mock_result.scalar_one.return_value = len(
            dataframe.loc[dataframe["M"] == True]  # noqa: E712
        )
        mock_db_connection.execute.return_value = mock_result
        mock_engine.execution_options.return_value = mock_engine

        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )

        # Mocks `connect` method and resulting context manager on SQLAlchemy Engine
        mocker.patch.object(
            db_conn.con, "connect"
        ).return_value.__enter__.return_value = mock_db_connection

        datasource = DataSource(
            db_conn,
            data_splitter=SplitterDefinedInData(
                column_name='q."M"', training_set_label="True"
            ),
        )

        datasource.load_data(sql_query="SELECT * FROM dummy_data")
        train_length = datasource.get_dataset_split_length(DataSplit.TRAIN)
        assert train_length == len(dataframe.loc[dataframe["M"] == True])  # noqa: E712

    @integration_test
    def test_get_dataset_split_length_with_multitable_database_connection(
        self, dataframe: pd.DataFrame, db_session: sqlalchemy.engine.base.Engine
    ) -> None:
        """Tests that `get_dataset_split_length` returns the correct length."""
        db_conn = DatabaseConnection(
            db_session, table_names=["dummy_data", "dummy_data_2"]
        )
        datasource = DataSource(
            db_conn,
            data_splitter=SplitterDefinedInData(
                column_name='q."M"', training_set_label="True"
            ),
        )
        datasource.load_data(sql_query="SELECT * FROM dummy_data")
        train_length = datasource.get_dataset_split_length(DataSplit.TRAIN)
        assert train_length == len(dataframe.loc[dataframe["M"] == True])  # noqa: E712

    @integration_test
    def test_database_single_table_input(
        self,
        db_session: sqlalchemy.engine.base.Engine,
    ) -> None:
        """Checks DataSource initialises correctly with `DatabaseConnection`.

        Single table database connection.
        """
        db_conn = DatabaseConnection(db_session, table_names=["dummy_data"])
        datasource = DataSource(db_conn, seed=420)
        datasource.load_data()
        datasource._split_data()
        assert datasource.data is not None
        assert not datasource.multi_table
        assert datasource._train_idxs is not None
        assert datasource._validation_idxs is not None
        assert datasource._test_idxs is not None
        assert len(datasource._train_idxs) + len(datasource._validation_idxs) + len(
            datasource._test_idxs
        ) == len(datasource.data)

    @unit_test
    def test_mock_database_single_table_input(
        self,
        mock_engine: Mock,
        mock_pandas_read_sql_table: None,
    ) -> None:
        """Checks DataSource initialises correctly with `DatabaseConnection`.

        Mock single table database connection.
        """
        db_conn = DatabaseConnection(mock_engine, table_names=["dummy_data"])
        datasource = DataSource(db_conn, seed=420)
        datasource.load_data()
        datasource._split_data()
        assert datasource.data is not None
        assert not datasource.multi_table
        assert datasource._train_idxs is not None
        assert datasource._validation_idxs is not None
        assert datasource._test_idxs is not None
        assert len(datasource._train_idxs) + len(datasource._validation_idxs) + len(
            datasource._test_idxs
        ) == len(datasource.data)

    @integration_test
    def test_database_multi_table_input(
        self,
        db_session: sqlalchemy.engine.base.Engine,
    ) -> None:
        """Checks DataSource initialises correctly with `DatabaseConnection`.

        Multi-table database connection.
        """
        db_conn = DatabaseConnection(
            db_session, table_names=["dummy_data", "dummy_data_2"]
        )

        datasource = DataSource(
            db_conn, seed=420, data_splitter=PercentageSplitter(0, 0)
        )

        # Test when load_data is called without query
        # DataSource has no data attribute
        datasource.load_data()
        assert datasource.multi_table
        assert not hasattr(datasource, "data")
        # Test when load_data is called WITH query
        # DataSource has no data attribute
        query = "SELECT 'Date', 'TARGET' FROM dummy_data"
        datasource.load_data(sql_query=query)
        assert not hasattr(datasource, "data")
        assert isinstance(datasource.loader, DatabaseLoader)
        expected_output = pd.read_sql(
            f"{query} LIMIT {datasource.loader.database_partition_size}",
            con=db_conn.con,
        )
        pd.testing.assert_frame_equal(
            next(datasource.yield_dataset_split(split=DataSplit.TRAIN)), expected_output
        )

    @unit_test
    def test_database_multi_table_input_table_name(
        self,
        db_session: sqlalchemy.engine.base.Engine,
    ) -> None:
        """Checks DataSource initialises correctly with `DatabaseConnection`.

        Multi-table database connection, load single table. Check that table is iterated
        instead of loaded.
        """
        db_conn = DatabaseConnection(
            db_session, table_names=["dummy_data", "dummy_data_2"]
        )

        database_partition_size = 10
        datasource = DataSource(
            db_conn, seed=420, database_partition_size=database_partition_size
        )

        # Test when load_data is called without query
        # DataSource has no data attribute
        datasource.load_data()
        assert not hasattr(datasource, "data")
        # Test when load_data is called WITH query
        # DataSource has no data attribute
        table_name = "dummy_data"
        datasource.load_data(table_name=table_name)
        assert not hasattr(datasource, "data")  # data is not set
        iterator = datasource.yield_dataset_split(split=DataSplit.TRAIN)
        df = next(iterator)
        assert len(df) == database_partition_size

    @integration_test
    def test_database_query_input(
        self,
        db_session: sqlalchemy.engine.base.Engine,
    ) -> None:
        """Checks DataSource initialises correctly with `DatabaseConnection`.

        Query database connection.
        """
        db_conn = DatabaseConnection(
            db_session,
            query="""
            SELECT *
            FROM dummy_data d1
            LEFT JOIN dummy_data_2 d2
            ON 'd1.Date' = 'd2.Date'
            """,
        )
        datasource = DataSource(db_conn, seed=420)
        datasource.load_data()
        datasource._split_data()
        assert not datasource.multi_table
        assert datasource.data is not None
        assert datasource._train_idxs is not None
        assert datasource._validation_idxs is not None
        assert datasource._test_idxs is not None
        assert len(datasource._train_idxs) + len(datasource._validation_idxs) + len(
            datasource._test_idxs
        ) == len(datasource.data)

    @integration_test
    @pytest.mark.parametrize(
        "query",
        [
            'SELECT "Date", "TARGET" FROM blah',
            'SELECT "invalid", FROM blah',
            '"invalid" from blah',
        ],
    )
    def test_database_query_sql_error(
        self, db_session: sqlalchemy.engine.base.Engine, query: str
    ) -> None:
        """Checks DataSource raises sqlalchemy error."""
        db_conn = DatabaseConnection(
            db_session,
            table_names=["dummy_data", "dummy_data_2"],
        )

        datasource = DataSource(db_conn, seed=420)
        datasource.load_data(sql_query=query)
        with pytest.raises(sqlalchemy.exc.ProgrammingError):
            next(datasource.yield_dataset_split(split=DataSplit.TRAIN))

    @unit_test
    def test_mock_database_query_input(
        self,
        mock_engine: Mock,
        mock_pandas_read_sql_query: None,
    ) -> None:
        """Checks DataSource initialises correctly with `DatabaseConnection`.

        Mock query database connection.
        """
        db_conn = DatabaseConnection(
            mock_engine,
            query="""
            SELECT *
            FROM dummy_data d1
            LEFT JOIN dummy_data_2 d2
            ON 'd1.Date' = 'd2.Date'
            """,
        )
        datasource = DataSource(db_conn, seed=420)
        datasource.load_data()
        datasource._split_data()
        assert not datasource.multi_table
        assert datasource.data is not None
        assert datasource._train_idxs is not None
        assert datasource._validation_idxs is not None
        assert datasource._test_idxs is not None
        assert len(datasource._train_idxs) + len(datasource._validation_idxs) + len(
            datasource._test_idxs
        ) == len(datasource.data)

    @unit_test
    def test_hash_multitable_raises_value_error(self, mock_engine: Mock) -> None:
        """Tests hash function raises `DataNotLoadedError` if data is not loaded."""
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        datasource = DataSource(db_conn, seed=420)
        with pytest.raises(DataNotLoadedError):
            datasource.hash

    @unit_test
    def test_training_set_unloaded_raises_error(self, mock_engine: Mock) -> None:
        """Tests that calling the `training_set` property raises an error.

        The error should be a `DataNotLoadedError` when the data is multi-table because
        it is never loaded.
        """
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        datasource = DataSource(db_conn, seed=420)
        datasource.load_data()
        with pytest.raises(DataNotLoadedError):
            datasource.get_dataset_split(DataSplit.TRAIN)

    @unit_test
    def test_validation_set_unsplit_raises_error(self, mock_engine: Mock) -> None:
        """Tests that calling the `validation_set` property raises an error.

        The error should be a `DataNotLoadedError` when the data is multi-table because
        it is never loaded.
        """
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        datasource = DataSource(db_conn, seed=420)
        datasource.load_data()
        with pytest.raises(DataNotLoadedError):
            datasource.get_dataset_split(DataSplit.VALIDATION)

    @unit_test
    def test_test_set_unsplit_raises_error(self, mock_engine: Mock) -> None:
        """Tests that calling the `test_set` property raises an error.

        The error should be a `DataNotLoadedError` when the data is multi-table because
        it is never loaded.
        """
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        datasource = DataSource(db_conn, seed=420)
        datasource.load_data()
        with pytest.raises(DataNotLoadedError):
            datasource.get_dataset_split(DataSplit.TEST)

    @unit_test
    def test_value_error_raised_if_no_table_name_provided_for_multitable_datasource(
        self, mock_engine: Mock
    ) -> None:
        """Tests ValueError raised if table_name missing for multi-table DataSource."""
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        ds = DataSource(db_conn, seed=420)
        ds.load_data()
        with pytest.raises(
            ValueError, match="No table name provided for multi-table datasource."
        ):
            ds.get_dtypes()

    @unit_test
    def test_value_error_raised_if_table_not_found_for_multitable_datasource(
        self, mock_engine: Mock
    ) -> None:
        """Tests ValueError raised if table is missing for multi-table DataSource."""
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        ds = DataSource(db_conn, seed=420)
        ds.load_data()
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Table name not_a_table not found in the data. "
                + "Available tables: ['dummy_data', 'dummy_data_2']"
            ),
        ):
            ds.get_dtypes("not_a_table")

    @unit_test
    def test_mock_get_dtypes_reads_and_returns_table_schema(
        self, mock_engine: Mock, mocker: MockerFixture
    ) -> None:
        """Tests that the `get_dtypes` method returns a dictionary.

        Also checks that the dtypes hash is added appropriately.
        """
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        ds = DataSource(db_conn, seed=420)
        mocker.patch.object(ds.loader, "get_dtypes", return_value={})

        assert len(ds._table_hashes) == 0
        assert isinstance(ds.get_dtypes("dummy_data"), dict)
        assert len(ds._table_hashes) == 1

    @integration_test
    def test_get_dtypes_reads_and_returns_table_schema(
        self, db_session: sqlalchemy.engine.base.Engine
    ) -> None:
        """Tests that the `get_dtypes` method returns a dictionary.

        Also checks that the dtypes hash is added appropriately.
        """
        db_conn = DatabaseConnection(
            db_session, table_names=["dummy_data", "dummy_data_2"]
        )
        ds = DataSource(db_conn, seed=420)
        assert len(ds._table_hashes) == 0
        table = ds.get_dtypes("dummy_data")
        assert isinstance(table, dict)
        assert len(ds._table_hashes) == 1

    @unit_test
    def test_yield_dataset_split_raises_value_error_if_no_query_or_table_name_provided(
        self,
        mock_engine: Mock,
    ) -> None:
        """Tests that ValueError is raised if no query or table name provided."""
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        ds = DataSource(db_conn, seed=420)
        with pytest.raises(ValueError, match="No query or table name specified."):
            next(ds.yield_dataset_split(DataSplit.TRAIN))

    @unit_test
    def test_yield_dataset_split_raises_value_error_if_not_database_loader(
        self, dataframe: pd.DataFrame
    ) -> None:
        """Tests that ValueError is raised if loader is not a DatabaseLoader."""
        ds = DataSource(dataframe, seed=420)
        with pytest.raises(
            ValueError,
            match="Iterating over in-memory data is currently not supported.",
        ):
            next(ds.yield_dataset_split(DataSplit.TRAIN))

    @unit_test
    def test_yield_dataset_split_works_correctly(
        self, dataframe: pd.DataFrame, mock_engine: Mock, mocker: MockerFixture
    ) -> None:
        """Tests that `yield_dataset_split` method works as expected."""
        mock_db_connection = Mock()
        mock_result = Mock()

        class MockPartition:
            """Mock class to represent database result paritions."""

            def __iter__(self) -> Iterator[np.ndarray]:
                """Iterator just returns one set of dataframe values."""
                yield dataframe.values

        mock_result.partitions.return_value = MockPartition()
        mock_result.keys.return_value = dataframe.columns
        mock_result.scalar_one.return_value = DATASET_ROW_COUNT
        mock_engine.execution_options.return_value = mock_engine
        mock_db_connection.execute.return_value = mock_result

        # Creates a multitable DatabaseConnection object
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data", "dummy_data_2"],
        )
        # Mocks `connect` method and resulting context manager on SQLAlchemy Engine
        mocker.patch.object(
            db_conn.con, "connect"
        ).return_value.__enter__.return_value = mock_db_connection

        # Creates DataSource
        ds = DataSource(db_conn, seed=420)
        ds.load_data(table_name="dummy_data")

        # Iterates over datasource split
        df = next(ds.yield_dataset_split(DataSplit.TRAIN))  # First output of iterator
        assert isinstance(df, pd.DataFrame)

        # Makes assertions on call stack
        # Ignoring mypy errors because `connect` has been patched to return a Mock
        db_conn.con.connect.assert_called()  # type: ignore[attr-defined] # Reason: see above # noqa: B950
        db_conn.con.connect.return_value.__enter__.assert_called()  # type: ignore[attr-defined] # Reason: see above # noqa: B950
        db_conn.con.execution_options.assert_called_once()  # type: ignore[attr-defined] # Reason: see above # noqa: B950
        mock_db_connection.execute.assert_called()
        mock_result.partitions.assert_called_once()
        mock_result.keys.assert_called_once()
        mock_result.scalar_one.assert_called_once()


@unit_test
class TestDatabaseLoader:
    """Tests DatabaseLoader class."""

    def test_len_magic_method(self, mock_engine: Mock, mocker: MockerFixture) -> None:
        """Tests that __len__ magic method returns correct row count."""
        # Mocks `execute` method on the SQLAlchemy connection object and the
        # `scalar_one` method on the resulting cursor result to return the
        # dataset row count
        mock_db_connection = Mock()
        mock_result = Mock()
        mock_result.scalar_one.return_value = DATASET_ROW_COUNT
        mock_db_connection.execute.return_value = mock_result
        mock_engine.execution_options.return_value = mock_engine

        # Creates a multitable DatabaseConnection object
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data", "dummy_data_2"],
        )
        # Mocks `connect` method and resulting context manager on SQLAlchemy Engine
        mocker.patch.object(
            db_conn.con, "connect"
        ).return_value.__enter__.return_value = mock_db_connection
        loader = DatabaseLoader(db_conn)

        # Calls __len__ method on loader
        dataset_length = len(loader)

        # Makes assertions on call stack in order
        # Ignoring mypy errors because `connect` has been patched to return a Mock
        db_conn.con.connect.assert_called_once()  # type: ignore[attr-defined] # Reason: see above # noqa: B950
        db_conn.con.connect.return_value.__enter__.assert_called_once()  # type: ignore[attr-defined]  # Reason: see above # noqa: B950
        mock_db_connection.execute.assert_called_once()
        mock_result.scalar_one.assert_called_once()

        # Makes assertion on final result
        assert dataset_length == DATASET_ROW_COUNT

    def test_validate_table_name_raises_value_error_if_table_name_is_none(
        self, mock_engine: Mock
    ) -> None:
        """Tests that ValueError is raised if there is no table name provided."""
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data", "dummy_data_2"],
        )
        loader = DatabaseLoader(db_conn)
        with pytest.raises(
            ValueError, match="No table name provided for multi-table datasource."
        ):
            loader._validate_table_name(None)

    def test_validate_table_name_raises_value_error_if_tables_dont_exist(
        self, mock_engine: Mock
    ) -> None:
        """Tests that ValueError is raised if there are no tables."""
        db_conn = DatabaseConnection(
            mock_engine,
            query="DUMMY QUERY",
        )
        loader = DatabaseLoader(db_conn)
        with pytest.raises(
            ValueError, match="Database Connection is not aware of any tables."
        ):
            loader._validate_table_name("dummy_data")

    def test_validate_table_name_raises_value_error_if_table_name_not_found(
        self, mock_engine: Mock
    ) -> None:
        """Tests that ValueError is raised if the table name is not found."""
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data", "dummy_data_2"],
        )
        loader = DatabaseLoader(db_conn)
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Table name blah not found in the data. "
                "Available tables: ['dummy_data', 'dummy_data_2']",
            ),
        ):
            loader._validate_table_name("blah")


@unit_test
class TestCSVLoader:
    """Tests CSVLoader."""

    def test_len(self, dataframe: pd.DataFrame, tmp_path: Path) -> None:
        """Tests that __len__ magic method returns correct row count."""
        file_path = tmp_path / "tabular_data_test.csv"
        dataframe.to_csv(file_path)
        loader = CSVLoader(file_path)
        assert len(loader) == DATASET_ROW_COUNT


@unit_test
class TestDataFrameLoader:
    """Tests DataFrameLoader."""

    def test_len(self, dataframe: pd.DataFrame) -> None:
        """Tests that __len__ magic method returns correct row count."""
        loader = DataFrameLoader(dataframe)
        assert len(loader) == DATASET_ROW_COUNT
