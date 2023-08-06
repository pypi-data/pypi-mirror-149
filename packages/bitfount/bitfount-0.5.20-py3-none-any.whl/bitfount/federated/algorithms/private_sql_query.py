"""SQL query algorithm."""
from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar, List, Optional, cast

from marshmallow import fields
import pandas as pd
import snsql
from snsql import Privacy

from bitfount.data.datasource import DataSource
from bitfount.data.schema import BitfountSchema
from bitfount.data.types import SemanticType, _SemanticTypeValue
from bitfount.federated.algorithms.base import (
    _BaseAlgorithmFactory,
    _BaseModellerAlgorithm,
    _BaseWorkerAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.mixins import _SQLAlgorithmMixIn
from bitfount.federated.privacy.differential import DPPodConfig, _DifferentiallyPrivate
from bitfount.types import T_FIELDS_DICT

if TYPE_CHECKING:
    from bitfount.hub.api import BitfountHub

logger = _get_federated_logger(__name__)


class _ModellerSide(_BaseModellerAlgorithm):
    """Modeller side of the PrivateSqlQuery algorithm."""

    def initialise(
        self,
        **kwargs: Any,
    ) -> None:
        """Nothing to initialise here."""
        pass

    def run(self, results: List[pd.DataFrame]) -> List[pd.DataFrame]:
        """Simply returns results."""
        return results


class _WorkerSide(_BaseWorkerAlgorithm):
    """Worker side of the PrivateSqlQuery algorithm."""

    def __init__(
        self,
        *,
        query: str,
        epsilon: float,
        delta: float,
        column_ranges: dict,
        hub: BitfountHub,
        **kwargs: Any,
    ) -> None:
        self.datasource: DataSource
        self.pod_identifier: Optional[str] = None
        self.pod_dp: Optional[DPPodConfig] = None
        self.query = query
        self.epsilon = epsilon
        self.delta = delta
        self.column_ranges = column_ranges
        self.hub = hub
        super().__init__(**kwargs)

    def initialise(
        self,
        datasource: DataSource,
        pod_dp: Optional[DPPodConfig] = None,
        pod_identifier: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Sets Datasource."""
        self.datasource = datasource
        if pod_identifier:
            self.pod_identifier = pod_identifier
        if pod_dp:
            self.pod_dp = pod_dp

    def map_types(self, schema: BitfountSchema) -> None:
        for column in self.column_ranges:
            mapped_type = None
            for table_name in schema.table_names:
                # Determine what type we have in the schema for the column
                for stype in SemanticType:
                    for feature in schema.get_table_schema(
                        table_name
                    ).get_feature_names(stype):
                        if feature == column:
                            mapped_type = (
                                schema.get_table_schema(table_name)
                                .features[cast(_SemanticTypeValue, stype.value)][
                                    feature
                                ]
                                .dtype.name
                            )
                            break

            if mapped_type is None:
                logger.error(
                    "No field named '%s' present in the schema"
                    "will proceed assuming it is a string.",
                    column,
                )
                mapped_type = "str"

            # Map the type we have to an equivalent for SmartNoise SQL
            if "int" in mapped_type or "Int" in mapped_type:
                mapped_type = "int"
            elif "float" in mapped_type or "Float" in mapped_type:
                mapped_type = "float"
            elif mapped_type == "object":
                mapped_type = "string"
            elif mapped_type == "string":
                mapped_type = "string"
            else:
                logger.error(
                    "Type %s for column '%s' is not supported"
                    "defaulting to string type.",
                    mapped_type,
                    column,
                )
                mapped_type = "string"

            self.column_ranges[column]["type"] = mapped_type

    def run(self) -> pd.DataFrame:
        """Returns the mean of the field in `DataSource` dataframe."""
        self.datasource.load_data()
        if self.datasource.data is not None:
            df = self.datasource.data
        else:
            # TODO: [BIT-1586] support querying directly from database
            raise ValueError("No data on which to execute SQL query.")

        if self.pod_identifier is None:
            raise ValueError("No pod identifier - cannot get schema to infer types.")

        # Get the schema from the hub, needed for getting the column data types.
        schema = self.hub.get_pod_schema(self.pod_identifier)
        # Map the dtypes to types understood by SmartNoise SQL
        self.map_types(schema)

        # Check that modeller-side dp parameters are within the pod config range.
        dp = _DifferentiallyPrivate(
            {"max_epsilon": self.epsilon, "target_delta": self.delta}
        )
        if self.pod_dp:
            dp.apply_pod_dp(self.pod_dp)

        # Set up the metadata dictionary required for SmartNoise SQL
        meta = {
            # "Collection" name
            "Database": {
                # "Schema" name
                "df": {
                    # "Table" name
                    "df": {
                        "row_privacy": True,
                        "rows": int(len(df.index)),
                    },
                }
            }
        }
        meta["Database"]["df"]["df"].update(self.column_ranges)

        try:
            # Configure privacy and execute the Private SQL query
            privacy = Privacy(
                epsilon=dp._dp_config.max_epsilon,  # type: ignore[union-attr] # reason: this won't actually be None as we initialise it explicitly # noqa: B950
                delta=dp._dp_config.target_delta,  # type: ignore[union-attr] # reason: this won't actually be None as we initialise it explicitly # noqa: B950
            )

            reader = snsql.from_df(df, privacy=privacy, metadata=meta)

            logger.info(
                "Executing SQL query with epsilon {} and delta {}".format(
                    privacy.epsilon, privacy.delta
                )
            )
            output = reader.execute(self.query)
        except Exception as ex:
            raise ValueError(
                f"Error executing PrivateSQL query: [{self.query}], got error [{ex}]"
            )

        return cast(pd.DataFrame, output)


class PrivateSqlQuery(_BaseAlgorithmFactory, _SQLAlgorithmMixIn):
    """Simple algorithm for running a SQL query on a table, with privacy.

    Args:
        query: The SQL query to execute.
        epsilon: The maximum epsilon to use for the privacy budget.
        delta: The target delta to use for the privacy budget.
        column_ranges: A dictionary of column names and their ranges.

    Attributes:
        query: The SQL query to execute.
        epsilon: The maximum epsilon to use for the privacy budget.
        delta: The target delta to use for the privacy budget.
        column_ranges: A dictionary of column names and their ranges.
    """

    fields_dict: ClassVar[T_FIELDS_DICT] = {
        "query": fields.Str(),
        "epsilon": fields.Float(allow_nan=True),
        "delta": fields.Float(allow_nan=True),
        "column_ranges": fields.Dict(),
    }

    def __init__(
        self,
        *,
        query: str,
        epsilon: float,
        delta: float,
        column_ranges: dict,
        **kwargs: Any,
    ):
        super().__init__()
        self.query = query
        self.epsilon = epsilon
        self.delta = delta
        self.column_ranges = column_ranges

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the PrivateSqlQuery algorithm."""
        return _ModellerSide(**kwargs)

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the PrivateSqlQuery algorithm.

        Args:
            **kwargs: Additional keyword arguments to pass to the worker side. `hub`
                must be one of these keyword arguments which provides a `BitfountHub`
                instance.
        """
        return _WorkerSide(
            query=self.query,
            epsilon=self.epsilon,
            delta=self.delta,
            column_ranges=self.column_ranges,
            **kwargs,
        )
