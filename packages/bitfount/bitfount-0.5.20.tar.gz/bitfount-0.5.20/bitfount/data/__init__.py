"""Modules for handling model data flow."""
from typing import List

from bitfount.data.datasource import DataSource
from bitfount.data.datasplitters import PercentageSplitter, SplitterDefinedInData
from bitfount.data.datastructure import DataStructure
from bitfount.data.exceptions import (
    BitfountSchemaError,
    DatabaseMissingTableError,
    DatabaseSchemaNotFoundError,
    DatabaseUnsupportedQueryError,
    DataNotLoadedError,
    DatasetSplitterError,
    DataStructureError,
    DuplicateColumnError,
)
from bitfount.data.helper import convert_epochs_to_steps
from bitfount.data.schema import BitfountSchema, TableSchema
from bitfount.data.types import (
    CategoricalRecord,
    ContinuousRecord,
    DataPathModifiers,
    ImageRecord,
    SemanticType,
    TextRecord,
)
from bitfount.data.utils import DatabaseConnection

__all__: List[str] = [
    "BitfountSchema",
    "BitfountSchemaError",
    "CategoricalRecord",
    "ContinuousRecord",
    "DatabaseConnection",
    "DatabaseMissingTableError",
    "DatabaseSchemaNotFoundError",
    "DatabaseUnsupportedQueryError",
    "DatasetSplitterError",
    "DataNotLoadedError",
    "DataPathModifiers",
    "DataSource",
    "DataStructure",
    "DataStructureError",
    "DuplicateColumnError",
    "ImageRecord",
    "PercentageSplitter",
    "SemanticType",
    "SplitterDefinedInData",
    "TableSchema",
    "TextRecord",
    "convert_epochs_to_steps",
]

# See top level `__init__.py` for an explanation
__pdoc__ = {}
for _obj in __all__:
    __pdoc__[_obj] = False
