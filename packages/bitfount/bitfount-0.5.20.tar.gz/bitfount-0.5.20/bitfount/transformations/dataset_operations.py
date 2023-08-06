"""Dataset-related transformations.

This module contains the base class and concrete classes for dataset transformations,
those that potentially act over the entire dataset.
"""
from typing import List, Union

import attr

from bitfount.transformations.base_transformation import Transformation


@attr.dataclass(kw_only=True)
class DatasetTransformation(Transformation):
    """Base transformation for all dataset transformation classes.

    User can specify "all" to have it act on every relevant column as defined
    in the schema.

    Args:
        output: Whether or not this transformation should be included in the final
            output. This must be True for all dataset transformations. Defaults to True.
        cols: The columns to act on as a list of strings. Defaults to "all" which acts
            on all columns in the dataset.

    Raises:
        ValueError: If `output` is False.
    """

    output: bool = True
    cols: Union[str, List[str]] = "all"

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        if not self.output:
            raise ValueError("`output` cannot be False for a DatasetTransformation")


@attr.dataclass(kw_only=True)
class CleanDataTransformation(DatasetTransformation):
    """Dataset transformation that will "clean" the specified columns.

    For continuous columns this will replace all infinities and NaNs with 0.
    For categorical columns this will replace all NaN's with "nan" explicitly.
    """

    _registry_name = "cleandata"


@attr.dataclass(kw_only=True)
class NormalizeDataTransformation(DatasetTransformation):
    """Dataset transformation that will normalise the specified continuous columns.

    Note: This will change integer dtypes in the dataset to float dtypes necessarily.
    """

    _registry_name = "normalizedata"
