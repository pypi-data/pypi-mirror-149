"""Classes concerning sources of data."""
from __future__ import annotations

from abc import ABC, abstractmethod
import logging
import os
from typing import (
    Any,
    Dict,
    Iterable,
    Iterator,
    List,
    Optional,
    Sequence,
    Set,
    Union,
    cast,
)

import numpy as np
import pandas as pd
from pydantic import AnyUrl
import sqlalchemy
from sqlalchemy import MetaData, Table, text
from sqlalchemy.orm import Session

from bitfount.data.datasplitters import DatasetSplitter, PercentageSplitter
from bitfount.data.exceptions import DataNotLoadedError
from bitfount.data.types import DataPathModifiers, DataSplit
from bitfount.data.utils import (
    DatabaseConnection,
    _convert_python_dtypes_to_pandas_dtypes,
    _generate_dtypes_hash,
    _hash_str,
)
from bitfount.types import _Dtypes
from bitfount.utils import seed_all

logger = logging.getLogger(__name__)

_DATABASE_PARTITION_SIZE: int = 100
_DATABASE_MAX_ROW_BUFFER: int = 500


class _BaseLoader(ABC):
    """Abstract Base Loader from which all other data loaders must inherit."""

    def __init__(self) -> None:
        self.data: Optional[pd.DataFrame] = None

    @abstractmethod
    def get_values(
        self, col_names: List[str], **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Implement this method to get distinct values from list of columns."""
        raise NotImplementedError

    @abstractmethod
    def get_column(self, col_name: str, **kwargs: Any) -> Union[np.ndarray, pd.Series]:
        """Implement this method to get single column from dataset."""
        raise NotImplementedError

    @abstractmethod
    def get_data(self, **kwargs: Any) -> Optional[pd.DataFrame]:
        """Implement this method to loads and return dataset."""
        raise NotImplementedError

    @abstractmethod
    def get_dtypes(self, **kwargs: Any) -> _Dtypes:
        """Implement this method to get the columns and column types from dataset."""
        raise NotImplementedError

    @abstractmethod
    def __len__(self) -> int:
        """Implement this method to get the number of rows in the dataset."""
        raise NotImplementedError


class CSVLoader(_BaseLoader):
    """Loader for loading csv files.

    Args:
        path: The path to the csv file.
        **kwargs: Additional arguments to be passed to `pandas.read_csv`.
    """

    def __init__(self, path: Union[os.PathLike, AnyUrl, str], **kwargs: Any):
        super().__init__()
        if not str(path).endswith(".csv"):
            raise TypeError("Please provide a Path or URL to a CSV file.")
        self.path = str(path)
        self.data: pd.DataFrame = pd.read_csv(self.path, **kwargs)

    def get_data(self, **kwargs: Any) -> pd.DataFrame:
        """Loads and returns data from CSV dataset.

        Returns:
            A DataFrame-type object which contains the data.
        """
        return self.data

    def get_values(
        self, col_names: List[str], **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Get distinct values from columns in CSV dataset.

        Args:
            col_names: The list of the columns whose distinct values should be
                returned.

        Returns:
            The distinct values of the requested column as a mapping from col name to
            a series of distinct values.

        """
        return {col: self.data[col].unique() for col in col_names}

    def get_column(self, col_name: str, **kwargs: Any) -> Union[np.ndarray, pd.Series]:
        """Loads and returns single column from CSV dataset.

        Args:
            col_name: The name of the column which should be loaded.

        Returns:
            The column request as a series.
        """
        csv_df: pd.DataFrame = pd.read_csv(self.path, usecols=np.asarray([col_name]))
        return csv_df[col_name]

    def get_dtypes(self, **kwargs: Any) -> _Dtypes:
        """Loads and returns the columns and column types of the CSV dataset.

        Returns:
            A mapping from column names to column types.
        """
        data = self.data.convert_dtypes()
        dtypes: _Dtypes = data.dtypes.to_dict()
        return dtypes

    def __len__(self) -> int:
        return len(self.data)


class DataFrameLoader(_BaseLoader):
    """Loader for loading dataframes.

    Args:
        data: The dataframe to be loaded.
    """

    def __init__(self, data: pd.DataFrame, **kwargs: Any):
        super().__init__()
        self.data: pd.DataFrame = data

    def get_values(
        self, col_names: List[str], **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Get distinct values from columns in DataFrame dataset.

        Args:
            col_names: The list of the columns whose distinct values should be
                returned.

        Returns:
            The distinct values of the requested column as a mapping from col name to
            a series of distinct values.
        """
        return {col: self.data[col].unique() for col in col_names}

    def get_column(self, col_name: str, **kwargs: Any) -> Union[np.ndarray, pd.Series]:
        """Loads and returns single column from dataframe dataset.

        Args:
            col_name: The name of the column which should be loaded.

        Returns:
            The column request as a series.
        """
        return self.data[col_name]

    def get_data(self, **kwargs: Any) -> pd.DataFrame:
        """Loads and returns datafrom DataFrame dataset.

        Returns:
            A DataFrame-type object which contains the data.
        """
        return self.data

    def get_dtypes(self, **kwargs: Any) -> _Dtypes:
        """Loads and returns the columns and column types from the Dataframe dataset.

        Returns:
            A mapping from column names to column types.
        """
        data = self.data.convert_dtypes()
        dtypes: _Dtypes = data.dtypes.to_dict()
        return dtypes

    def __len__(self) -> int:
        return len(self.data)


class DatabaseLoader(_BaseLoader):
    """Data source for loading data from databases."""

    def __init__(
        self,
        db_conn: DatabaseConnection,
        database_partition_size: int = _DATABASE_PARTITION_SIZE,
        max_row_buffer: int = _DATABASE_MAX_ROW_BUFFER,
        **kwargs: Any,
    ):
        super().__init__()
        self.db_conn: DatabaseConnection = db_conn
        self.database_partition_size = database_partition_size
        self.max_row_buffer = max_row_buffer
        self.data: Optional[pd.DataFrame] = None
        self.table_names = self.db_conn.table_names
        self._con: Optional[sqlalchemy.engine.Engine] = None
        self.datastructure_query: Optional[str] = None
        self.datastructure_table_name: Optional[str] = None

    @property
    def query(self) -> Optional[str]:
        """A Database query as a string.

        The query is resolved in the following order:
            1. The query specified in the database connection.
            2. The table name specified in the database connection if just 1 table.
            3. The query specified by the datastructure (if multi-table).
            4. The table name specified by the datastructure (if multi-table).
            5. None.
        """
        if self.db_conn.query:
            return self.db_conn.query
        elif self.db_conn.table_names and len(self.db_conn.table_names) == 1:
            # Table name has been validated
            return f"SELECT * FROM {self.db_conn.table_names[0]}"  # nosec
        elif self.datastructure_query:
            return self.datastructure_query
        elif self.datastructure_table_name:
            # Table name has been validated
            return f"SELECT * FROM {self.datastructure_table_name}"  # nosec

        return None

    @property
    def con(self) -> sqlalchemy.engine.Engine:
        """Sqlalchemy engine.

        Connection options are set to stream results using a server side cursor where
        possible (depends on the database backend's support for this feature) with a
        maximum client side row buffer of `self.max_row_buffer` rows.
        """
        if not self._con:
            self._con = self.db_conn.con.execution_options(
                stream_results=True, max_row_buffer=self.max_row_buffer
            )
        return self._con

    def __len__(self) -> int:
        if self.data is not None:
            return len(self.data)
        elif not self.db_conn.multi_table:
            data = cast(pd.DataFrame, self.get_data())
            return len(data)

        with self.con.connect() as con:
            # Ignoring the security warning because the sql query is trusted and
            # will be executed regardless.
            result = con.execute(
                text(f"SELECT COUNT(*) FROM ({self.query}) q")  # nosec
            )
            return cast(int, result.scalar_one())

    def _validate_table_name(self, table_name: Optional[str]) -> None:
        """Validate the table name exists in the database.

        Args:
            table_name: The name of the table.

        Raises:
            ValueError: If the data is multi-table but no table name provided.
            ValueError: If the table name is not found in the data.
            ValueError: If the database connection does not have any table names.
        """
        if table_name is None:
            raise ValueError("No table name provided for multi-table datasource.")
        elif not self.table_names:
            raise ValueError("Database Connection is not aware of any tables.")
        elif table_name not in self.table_names:
            raise ValueError(
                f"Table name {table_name} not found in the data. "
                f"Available tables: {self.table_names}"
            )

    def get_values(
        self, col_names: List[str], table_name: Optional[str] = None, **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Get distinct values from columns in Database dataset.

        Args:
            col_names: The list of the columns whose distinct values should be
                returned.
            table_name: The name of the table to which the column exists. Required
                for multi-table databases.

        Returns:
            The distinct values of the requested column as a mapping from col name to
            a series of distinct values.
        """
        metadata = MetaData(self.con)
        output: Dict[str, Iterable[Any]] = {}
        if self.query is not None:
            # TODO: [BIT-1595] change to load memory using sqlalchemy FrozenResult
            self.data = cast(pd.DataFrame, pd.read_sql(self.query, con=self.con))
            for col_name in col_names:
                output[col_name] = self.data[col_name].unique()
        else:
            self._validate_table_name(table_name)

            table = Table(
                table_name,
                metadata,
                schema=self.db_conn.db_schema,
                autoload=True,
                autoload_with=self.con,
            )
            with Session(self.con) as session:
                for col_name in col_names:
                    values = np.array(
                        [v for v, in session.query(table.columns[col_name]).distinct()]
                    )
                    output[col_name] = values
        return output

    def get_column(
        self, col_name: str, table_name: Optional[str] = None, **kwargs: Any
    ) -> Union[np.ndarray, pd.Series]:
        """Loads and returns single column from Database dataset.

        Args:
            col_name: The name of the column which should be loaded.
            table_name: The name of the table to which the column exists. Required
                for multi-table databases.

        Returns:
            The column request as a series.

        Raises:
            ValueError: If the data is multi-table but no table name provided.
            ValueError: If the table name is not found in the data.
        """
        results: Iterable[Any]
        metadata = MetaData(self.con)
        if self.query is not None:
            with Session(self.con) as session:
                results = session.execute(text(self.query)).columns(col_name)
        else:
            self._validate_table_name(table_name)
            table = Table(
                table_name,
                metadata,
                schema=self.db_conn.db_schema,
                autoload=True,
                autoload_with=self.con,
            )
            with Session(self.con) as session:
                results = session.query(table.columns[col_name])

        series = pd.Series([v for v, in results])
        return series

    def get_data(
        self,
        sql_query: Optional[str] = None,
        table_name: Optional[str] = None,
        **kwargs: Any,
    ) -> Optional[pd.DataFrame]:
        """Loads and returns data from Database dataset.

        Args:
            sql_query: A SQL query string required for multi table data sources. This
                comes from the DataStructure and takes precedence over the table_name.
            table_name: Table name for multi table data sources. This
                comes from the DataStructure and is ignored if sql_query has been
                provided.

        Returns:
            A DataFrame-type object which contains the data.
        """
        data: Optional[pd.DataFrame] = None
        if self.db_conn.multi_table:
            # If multi-table, we don't actually load the data, we just set the query and
            # table name for the iterator.
            if sql_query is not None:
                self.datastructure_query = sql_query
            if table_name is not None:
                self.datastructure_table_name = table_name
        elif self.db_conn.query:
            data = pd.read_sql_query(sql=self.db_conn.query, con=self.con)
        else:
            # If the data is not multi-table and there is no query, there must
            # necessarily be one table name. Reassuring mypy of this.
            assert self.table_names is not None and len(self.table_names) == 1  # nosec
            data = pd.read_sql_table(
                table_name=self.table_names[0],
                con=self.con,
                schema=self.db_conn.db_schema,
            )
        self.data = data
        return data

    def get_dtypes(self, table_name: Optional[str] = None, **kwargs: Any) -> _Dtypes:
        """Loads and returns the columns and column types from the Database dataset.

        Args:
            table_name: The name of the column which should be loaded. Only
                required for multitable database.

        Returns:
            A mapping from column names to column types.
        """
        metadata = MetaData(self.con)
        dtypes: _Dtypes
        if self.query is not None:
            with Session(self.con) as session:
                result = session.execute(text(self.query)).first()
            data = pd.DataFrame([result])
            dtypes = data.convert_dtypes().dtypes.to_dict()

        else:
            self._validate_table_name(table_name)

            table = Table(
                table_name,
                metadata,
                schema=self.db_conn.db_schema,
                autoload=True,
                autoload_with=self.con,
            )
            dtypes = {
                col.name: _convert_python_dtypes_to_pandas_dtypes(
                    col.type.python_type, col.name
                )
                for col in table.columns
            }
        return dtypes


class DataSource:
    """DataSource class which encapsulates data.

    Args:
        data_ref: The reference of the data to load.
        data_splitter: Approach used for splitting the data into training, test,
            validation. Defaults to None.
        seed: Random number seed. Used for setting random seed for all libraries.
            Defaults to None.
        modifiers: Dictionary used for modifying paths/ extensions in the dataframe.
            Defaults to None.
        ignore_cols: Column/list of columns to be ignored from the data.
            Defaults to None.
        **kwargs: Additional keyword arguments to be passed to the underlying function
            which loads the data.

    Attributes:
        data: A Dataframe-type object which contains the data.
        data_ref: The reference of the data to load.
        data_splitter: Approach used for splitting the data into training, test,
            validation.
        seed: Random number seed. Used for setting random seed for all libraries.
        train_idxs: A numpy array containing the indices of the data which
            will be used for training.
        validation_idxs: A numpy array containing the indices of the data which
            will be used for validation.
        test_idxs: A numpy array containing the indices of the data which
            will be used for testing.

    Raises:
        TypeError: If data format is not supported.
        ValueError: If `image_col` is specified but can't be found in `data`.
        ValueError: If both `ignore_cols` and `selected_cols` are specified.
    """

    def __init__(
        self,
        data_ref: Union[os.PathLike, AnyUrl, DatabaseConnection, pd.DataFrame],
        data_splitter: Optional[DatasetSplitter] = None,
        seed: Optional[int] = None,
        modifiers: Optional[Dict[str, DataPathModifiers]] = None,
        ignore_cols: Optional[Union[str, Sequence[str]]] = None,
        **loader_kwargs: Any,
    ):
        self.data_ref = data_ref
        self.data_splitter = data_splitter
        self._loader_kwargs = loader_kwargs
        self.data: pd.DataFrame
        self.loader = self.get_loader()
        self._data_is_split: bool = False
        self._data_is_loaded: bool = False
        self.seed = seed
        self._modifiers = modifiers
        seed_all(self.seed)

        self._train_idxs: Optional[np.ndarray] = None
        self._validation_idxs: Optional[np.ndarray] = None
        self._test_idxs: Optional[np.ndarray] = None
        self._table_hashes: Set[str] = set()

        self._ignore_cols: List[str] = []
        if isinstance(ignore_cols, str):
            self._ignore_cols = [ignore_cols]
        elif ignore_cols is not None:
            self._ignore_cols = list(ignore_cols)

    @property
    def multi_table(self) -> bool:
        """Attribute to specify whether the datasource is multi table."""
        if isinstance(self.data_ref, DatabaseConnection):
            return self.data_ref.multi_table
        else:
            return False

    @property
    def hash(self) -> str:
        """The hash associated with this DataSource.

        This is the hash of the static information regarding the underlying DataFrame,
        primarily column names and content types but NOT anything content-related
        itself. It should be consistent across invocations, even if additional data
        is added, as long as the DataFrame is still compatible in its format.

        Returns:
            The hexdigest of the DataFrame hash.
        """
        if not self._table_hashes:
            raise DataNotLoadedError(
                "Data is not loaded yet. Please call `get_dtypes` first."
            )
        else:
            return _hash_str(str(sorted(self._table_hashes)))

    def get_loader(self) -> _BaseLoader:
        """Determine loader based on the type of the `data_ref`."""
        loader: _BaseLoader
        if isinstance(self.data_ref, (os.PathLike, AnyUrl, str)):
            if not str(self.data_ref).endswith(".csv"):
                raise TypeError("Please provide a Path or URL to a CSV file.")
            loader = CSVLoader(self.data_ref, **self._loader_kwargs)
        elif isinstance(self.data_ref, pd.DataFrame):
            loader = DataFrameLoader(self.data_ref, **self._loader_kwargs)
        elif isinstance(self.data_ref, DatabaseConnection):
            loader = DatabaseLoader(self.data_ref, **self._loader_kwargs)
        else:
            raise TypeError(f"Can't read data of type {type(self.data_ref)}")
        return loader

    def _modify_column(
        self,
        column: Union[np.ndarray, pd.Series],
        modifier_dict: DataPathModifiers,
    ) -> Union[np.ndarray, pd.Series]:
        """Modify the given column.

        Args:
            column: The column you are operating on.
            modifier_dict: A dictionary with the key as the
            prefix/suffix and the value to be prefixed/suffixed.
        """
        # Get the modifier dictionary:
        for modifier_type, modifier_string in modifier_dict.items():
            if modifier_type == "prefix":
                column = modifier_string + column.astype(str)

            elif modifier_type == "suffix":
                column = column.astype(str) + modifier_string
        return column

    def _modify_file_paths(self, modifiers: Dict[str, DataPathModifiers]) -> None:
        """Modifies image file paths if provided.

        Args:
            modifiers: A dictionary with the column name and
            prefix and/or suffix to modify file path.
        """
        for column_name in modifiers.keys():
            # Get the modifier dictionary:
            modifier_dict = modifiers[column_name]
            self.data[column_name] = self._modify_column(
                self.data[column_name], modifier_dict
            )

    def _get_data(
        self, sql_query: Optional[str] = None, table_name: Optional[str] = None
    ) -> Optional[pd.DataFrame]:
        """Loads and returns data.

        Args:
            sql_query: A SQL query string required for multi table data sources.

        Returns:
            A DataFrame-type object which contains the data.
        """
        data = self.loader.get_data(sql_query=sql_query, table_name=table_name)
        return data

    def get_features(self) -> List[str]:
        """Returns the features of the data.

        Returns:
            A list of the feature names in the data.

        Raises:
            DataNotLoadedError: If data is not loaded.
        """
        if self._data_is_loaded:
            feature_names: List[str] = self.data.columns
            return feature_names

        raise DataNotLoadedError(
            "Data is not loaded yet. Please call `load_data` first."
        )

    def get_dtypes(self, table_name: Optional[str] = None) -> _Dtypes:
        """Loads and returns the columns and column types of the data.

        Args:
            table_name: The name of the column which should be loaded. Only
                required for multitable database.

        Returns:
            A mapping from column names to column types.
        """
        dtypes: _Dtypes = self.loader.get_dtypes(table_name=table_name)
        if not self._data_is_loaded and self.loader.data is not None:
            self.data = self.loader.data
            self._data_is_loaded = True

        for col in self._ignore_cols:
            if col in dtypes.keys():
                del dtypes[col]

        self._table_hashes.add(_generate_dtypes_hash(dtypes))
        return dtypes

    def get_values(
        self, col_names: List[str], table_name: Optional[str] = None
    ) -> Dict[str, Iterable[Any]]:
        """Get distinct values from columns in data.

        Args:
            col_names: The list of the column whose distinct values should be
                returned.
            table_name: The name of the table to which the column exists. Required
                for multi-table databases.

        Returns:
            The distinct values of the requested column as a mapping from col name to
            a series of distinct values.
        """
        return self.loader.get_values(col_names=col_names, table_name=table_name)

    def get_column(
        self, col_name: str, table_name: str
    ) -> Union[np.ndarray, pd.Series]:
        """Loads and returns single column from dataset.

        Args:
            col_name: The name of the column which should be loaded.
            table_name: The name of the table to which the column exists. Required
                for multi-table databases.

        Returns:
            The column request as a series.
        """
        column = self.loader.get_column(col_name=col_name, table_name=table_name)
        if self._modifiers:
            if modifier_dict := self._modifiers.get(col_name):
                column = self._modify_column(column, modifier_dict)
        return column

    def load_data(
        self, sql_query: Optional[str] = None, table_name: Optional[str] = None
    ) -> None:
        """Load the data for the datasource.

        This method is idempotent so it can be called multiple times without
        reloading the data.

        Raises:
            TypeError: If data format is not supported.
        """
        if not self._data_is_loaded:
            data = self._get_data(sql_query=sql_query, table_name=table_name)

            if data is not None:  # i.e. if not multi_table
                # If columns already missing in data, ignore errors.
                self.data = data.drop(self._ignore_cols, axis=1, errors="ignore")

                if self._modifiers:
                    self._modify_file_paths(self._modifiers)

                self._data_is_loaded = True

    def _resolve_data_splitter(
        self,
        data_splitter: Optional[DatasetSplitter] = None,
    ) -> DatasetSplitter:
        """Resolves the data splitter.

        The data splitter is resolved in the following order:
            1. DataSource data_splitter if specified
            2. Provided data_splitter if specified
            3. PercentageSplitter (default)

        Returns:
            The appropriate data splitter to use.
        """
        if self.data_splitter:
            if data_splitter:
                logger.warning(
                    "Ignoring provided data splitter as the DataSource already has one."
                )
            data_splitter = self.data_splitter
        elif not data_splitter:
            logger.warning(
                "No data splitter provided. Using default PercentageSplitter."
            )
            data_splitter = PercentageSplitter()

        return data_splitter

    def _split_data(self, data_splitter: Optional[DatasetSplitter] = None) -> None:
        """Split the data into training, validation and test datasets.

        This method is idempotent so it can be called multiple times without
        re-splitting the data.

        Args:
            data_splitter: An optional data splitter object.
        """
        if not self._data_is_split:
            data_splitter = self._resolve_data_splitter(data_splitter)

            (
                self._train_idxs,
                self._validation_idxs,
                self._test_idxs,
            ) = data_splitter.create_dataset_splits(self.data)

            self._data_is_split = True
        else:
            logger.debug("Data is already split, keeping the current split.")

    def yield_dataset_split(
        self,
        split: DataSplit,
        data_splitter: Optional[DatasetSplitter] = None,
    ) -> Iterator[pd.DataFrame]:
        """Returns an iterator over the relevant data split.

        Args:
            split: The portion of data to yield from.
            data_splitter: The splitter object used to split the data.

        Returns:
            A iterator of pandas dataframes containing the relevant data split.

        Raises:
            ValueError: If no query or table name has been supplied for multi-table
                data.
            ValueError: If attempting to iterate over in-memory data.
        """
        if isinstance(self.loader, DatabaseLoader):
            if not self.loader.query:
                raise ValueError("No query or table name specified.")

            query = self._resolve_data_splitter(data_splitter).get_split_query(
                self.loader, split
            )
            with self.loader.con.connect() as con:
                result = con.execute(text(query))
                for partition in result.partitions(self.loader.database_partition_size):
                    yield pd.DataFrame(partition, columns=list(result.keys()))
        else:
            raise ValueError(
                "Iterating over in-memory data is currently not supported."
            )

    def get_dataset_split(
        self,
        split: DataSplit,
        data_splitter: Optional[DatasetSplitter] = None,
    ) -> pd.DataFrame:
        """Returns the relevant portion of `self.data`.

        Args:
            split: The portion of data to return.
            data_splitter: The splitter object used to split the data.

        Returns:
            A dataframe-type object containing the data points specified by the data
            splitter.

        Raises:
            DataNotLoadedError: If data has not been loaded.
        """
        if not self._data_is_loaded:
            raise DataNotLoadedError(
                "Please load data before accessing a split. "
                "If the data is remote, it must be iterated."
            )

        self._split_data(data_splitter)  # idempotent
        indices: np.ndarray = getattr(self, f"_{split.value}_idxs")
        df: pd.DataFrame = self.data.loc[indices.tolist()]
        return df.reset_index(drop=True)

    def get_dataset_split_length(
        self, split: DataSplit, data_splitter: Optional[DatasetSplitter] = None
    ) -> int:
        """Returns the length of the specified dataset split.

        Args:
            split: The split to get the length of.
            data_splitter: The splitter object used to split the data if the DataSource
                does not have one.

        Returns:
            The length of the specified dataset split.

        Raises:
            DataNotLoadedError: If unable to get the length of the dataset split.
        """
        data_splitter = self._resolve_data_splitter(data_splitter)

        # If PercentageSplitter is used regardless of the data loader.
        if isinstance(data_splitter, PercentageSplitter):
            len_loader = len(self.loader)
            if split == DataSplit.TRAIN:
                return int(len_loader * data_splitter.train_percentage / 100)
            elif split == DataSplit.VALIDATION:
                return int(len_loader * data_splitter.validation_percentage / 100)
            elif split == DataSplit.TEST:
                return int(len_loader * data_splitter.test_percentage / 100)

        # If the data is held in memory with any other splitter.
        elif self._data_is_loaded:
            return len(self.get_dataset_split(split=split, data_splitter=data_splitter))

        # If the data is held in a database with any other splitter. This is because
        # it requires the database to be queried in order to determine the length of
        # a split e.g. `SplitterDefinedInData`
        elif isinstance(self.loader, DatabaseLoader):
            query = self._resolve_data_splitter(data_splitter).get_split_query(
                self.loader, split
            )
            with self.loader.con.connect() as con:
                # Ignoring the security warning because the sql query is trusted and
                # will be executed regardless.
                result = con.execute(text(f"SELECT COUNT(*) FROM ({query}) q"))  # nosec
                return cast(int, result.scalar_one())

        # `load_data` should be called to avoid this error being raised
        raise DataNotLoadedError("Unable to get length of dataset split")
