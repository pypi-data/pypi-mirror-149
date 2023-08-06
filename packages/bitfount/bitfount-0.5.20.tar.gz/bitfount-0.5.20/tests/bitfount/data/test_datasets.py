"""Test dataset classes in data/datasets.py."""

from typing import Iterator
from unittest.mock import MagicMock, Mock

from PIL import Image
from _pytest.logging import LogCaptureFixture
import numpy as np
import pandas as pd
import pytest
from pytest import fixture
from pytest_mock import MockerFixture

from bitfount.data.datasets import _BitfountDataset, _IterableBitfountDataset
from bitfount.data.datasource import DatabaseLoader, DataSource
from bitfount.data.datasplitters import PercentageSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from bitfount.data.types import DataSplit, SemanticType
from bitfount.data.utils import DatabaseConnection
from tests.utils.helper import DATASET_ROW_COUNT, TABLE_NAME, create_dataset, unit_test


@fixture
def tabular_dataframe() -> pd.DataFrame:
    """Underlying dataframe for tabular datasets."""
    return create_dataset()


@unit_test
class TestBaseBitfountDataset:
    """Tests BaseBitfountDataset class."""

    def test_transform_image_with_custom_batch_transformation(
        self, image_dataset: _BitfountDataset
    ) -> None:
        """Test transform_image method."""
        assert image_dataset.batch_transforms is not None
        img_array = np.array(Image.new("RGB", size=(224, 224), color=(55, 100, 2)))
        transformed_image = image_dataset._transform_image(img_array.copy(), 0)
        assert isinstance(transformed_image, np.ndarray)
        assert transformed_image.shape == (224, 224, 3)

        # Assert that the transformed image is not the same as the original
        with pytest.raises(AssertionError):
            np.testing.assert_array_equal(img_array, transformed_image)

    def test_load_image(self, image_dataset: _BitfountDataset) -> None:
        """Test transform_image method."""
        loaded_transformed_image = image_dataset._load_images(0)
        assert isinstance(loaded_transformed_image, np.ndarray)
        assert loaded_transformed_image.shape == (224, 224, 3)

    def test_apply_schema(
        self, caplog: LogCaptureFixture, tabular_dataframe: pd.DataFrame
    ) -> None:
        """Tests data is loaded according to `selected_cols` and schema."""
        target = "TARGET"
        datasource = DataSource(
            tabular_dataframe, ignore_cols=["image"], data_splitter=PercentageSplitter()
        )
        datasource.load_data()
        datasource.data = datasource.data.drop(columns=["I", "J", "K", "L"])
        schema = BitfountSchema()
        schema.add_datasource_tables(datasource, table_name=TABLE_NAME)

        datastructure = DataStructure(
            target=target, ignore_cols=["image"], table=TABLE_NAME
        )
        datastructure.set_training_column_split_by_semantic_type(schema.tables[0])
        tabular_dataset = _BitfountDataset(
            datasource=datasource,
            target=target,
            selected_cols=datastructure.selected_cols,
            data_split=DataSplit.TRAIN,
            schema=schema.get_table_schema(TABLE_NAME),
            selected_cols_semantic_types=datastructure.selected_cols_w_types,
        )

        assert set(tabular_dataset.data.columns).issubset(
            set(tabular_dataset.selected_cols)
        )
        assert set(tabular_dataset.data.columns).issubset(
            set(tabular_dataset.schema.get_feature_names())
        )

        for record in caplog.records:
            if record.levelname == "WARNING":
                assert (
                    record.message
                    == "Selected columns `I,J,K,L` were not found in the data, continuing without them."  # noqa: B950
                )

    def test_apply_schema_with_extra_columns(
        self, caplog: LogCaptureFixture, tabular_dataframe: pd.DataFrame
    ) -> None:
        """Tests data is loaded according to `selected_cols` and schema.

        Checks that even if extra columns are provided in the `selected_cols` from the
        DataStructure, they are not used when loading the datasource.
        """
        target = "TARGET"
        datasource = DataSource(tabular_dataframe, ignore_cols=["image"])
        datasource.load_data()

        schema = BitfountSchema()
        schema.add_datasource_tables(datasource, table_name=TABLE_NAME)
        datasource.data = datasource.data.drop(
            columns=schema.get_feature_names(TABLE_NAME, SemanticType.TEXT)
        )
        datastructure = DataStructure(
            target=target, ignore_cols=["image"], table=TABLE_NAME
        )
        datastructure.set_training_column_split_by_semantic_type(schema.tables[0])
        tabular_dataset = _BitfountDataset(
            datasource=datasource,
            target=target,
            selected_cols=datastructure.selected_cols,
            data_split=DataSplit.TRAIN,
            schema=schema.get_table_schema(TABLE_NAME),
            selected_cols_semantic_types=datastructure.selected_cols_w_types,
        )

        assert set(tabular_dataset.data.columns).issubset(
            set(tabular_dataset.selected_cols)
        )
        assert set(tabular_dataset.data.columns).issubset(
            set(tabular_dataset.schema.get_feature_names())
        )
        assert (
            "Selected columns `I,J,K,L` were not found in the data, continuing without them."  # noqa: B950
            in caplog.text
        )


@unit_test
class TestBitfountDataset:
    """Tests BitfountDataset class."""

    def test_len_tab_data(self, tabular_dataset: _BitfountDataset) -> None:
        """Tests tabular dataset __len__ method."""
        assert tabular_dataset.datasource._train_idxs is not None
        assert len(tabular_dataset) == len(tabular_dataset.datasource._train_idxs)

    def test_len_img_data(self, image_tab_dataset: _BitfountDataset) -> None:
        """Tests image dataset __len__ method."""
        assert image_tab_dataset.datasource._train_idxs is not None
        assert len(image_tab_dataset) == len(image_tab_dataset.datasource._train_idxs)

    def test_len_img_tab_data(self, image_dataset: _BitfountDataset) -> None:
        """Tests dataset __len__ method."""
        assert image_dataset.datasource._train_idxs is not None
        assert len(image_dataset) == len(image_dataset.datasource._train_idxs)

    def test_len_multiimg_data(self, multiimage_dataset: _BitfountDataset) -> None:
        """Tests multi-image dataset __len__ method."""
        assert multiimage_dataset.datasource._train_idxs is not None
        assert len(multiimage_dataset) == len(multiimage_dataset.datasource._train_idxs)


class TestIterableBitfountDataset:
    """Tests IterableBitfountDataset class."""

    @pytest.mark.parametrize(
        "data_split", [DataSplit.TRAIN, DataSplit.VALIDATION, DataSplit.TEST]
    )
    @pytest.mark.parametrize(
        "validation_percentage,test_percentage", [(0, 0), (10, 10)]
    )
    @unit_test
    def test_len_magic_method(
        self,
        data_split: DataSplit,
        mock_engine: Mock,
        tabular_dataframe: pd.DataFrame,
        test_percentage: int,
        validation_percentage: int,
    ) -> None:
        """Tests that __len__ magic method returns correct row count."""
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data", "dummy_data_2"],
        )
        splitter = PercentageSplitter(
            validation_percentage=validation_percentage,
            test_percentage=test_percentage,
        )
        ds = DataSource(
            db_conn,
            seed=420,
            data_splitter=splitter,
        )
        ds.loader = MagicMock(spec=DatabaseLoader)
        ds.loader.__len__.return_value = DATASET_ROW_COUNT

        schema = BitfountSchema(
            datasource=DataSource(tabular_dataframe), table_name="dummy_data"
        )
        dataset = _IterableBitfountDataset(
            datasource=ds,
            selected_cols_semantic_types={
                "continuous": ["columns", "dont", "matter", "here"]
            },
            selected_cols=[],
            schema=schema.tables[0],
            target="TARGET",
            data_split=data_split,
        )

        # Call __len__ method on dataset
        dataset_length = len(dataset)
        ds.loader.__len__.assert_called_once()

        if data_split == DataSplit.TRAIN:
            assert dataset_length == int(
                DATASET_ROW_COUNT * splitter.train_percentage / 100
            )
        elif data_split == DataSplit.VALIDATION:
            assert dataset_length == int(
                DATASET_ROW_COUNT * splitter.validation_percentage / 100
            )
        elif data_split == DataSplit.TEST:
            assert dataset_length == int(
                DATASET_ROW_COUNT * splitter.test_percentage / 100
            )

    @unit_test
    def test_dataset_len_is_cached(
        self,
        mock_engine: Mock,
        tabular_dataframe: pd.DataFrame,
    ) -> None:
        """Tests that __len__ magic method uses cached length."""
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data", "dummy_data_2"],
        )
        splitter = PercentageSplitter()  # default is 80:10:10
        ds = DataSource(
            db_conn,
            seed=420,
            data_splitter=splitter,
        )
        ds.loader = MagicMock(spec=DatabaseLoader)
        ds.loader.__len__.return_value = DATASET_ROW_COUNT

        schema = BitfountSchema(
            datasource=DataSource(tabular_dataframe), table_name="dummy_data"
        )
        dataset = _IterableBitfountDataset(
            datasource=ds,
            selected_cols_semantic_types={
                "continuous": ["columns", "dont", "matter", "here"]
            },
            selected_cols=[],
            schema=schema.tables[0],
            target="TARGET",
            data_split=DataSplit.TRAIN,
        )

        # Call __len__ method on dataset TWICE
        dataset_length = len(dataset)
        dataset_length_2 = len(dataset)

        # Make assertion that mock only called ONCE
        ds.loader.__len__.assert_called_once()

        # Makes assertion on final result
        assert (
            dataset_length
            == dataset_length_2
            == int(DATASET_ROW_COUNT * splitter.train_percentage / 100)
        )

    @unit_test
    def test_iter_magic_method(
        self, mock_engine: Mock, mocker: MockerFixture, tabular_dataframe: pd.DataFrame
    ) -> None:
        """Tests that __iter__ magic method works as expected."""
        ds = DataSource(tabular_dataframe)
        schema = BitfountSchema(
            datasource=ds,
            table_name="dummy_data",
            force_stypes={"dummy_data": {"categorical": ["TARGET"]}},
        )

        class MockDataSourceIterator:
            """Mock class to represent database result paritions."""

            def __iter__(self) -> Iterator[pd.DataFrame]:
                """Iterator just returns one set of dataframe values."""
                yield tabular_dataframe

        mock_datasource_iterator = MockDataSourceIterator()
        mocker.patch.object(
            ds, "yield_dataset_split", return_value=mock_datasource_iterator
        )

        dataset = _IterableBitfountDataset(
            datasource=ds,
            selected_cols_semantic_types={
                "continuous": ["A", "B"],
                "categorical": ["TARGET"],
            },
            selected_cols=["TARGET", "A", "B"],
            schema=schema.tables[0],
            target="TARGET",
            data_split=DataSplit.TRAIN,
        )

        # Call __iter__ method on dataset
        dataset_iterator = iter(dataset)
        row = next(dataset_iterator)  # First output of iterator
        assert isinstance(row, tuple)
        assert isinstance(row[0], tuple)  # x data
        assert isinstance(row[0][0], np.ndarray)  # tabular x data
        assert isinstance(row[0][1], np.ndarray)  # x support columns
        assert isinstance(row[1], np.integer)  # y data

        ds.yield_dataset_split.assert_called_once()
