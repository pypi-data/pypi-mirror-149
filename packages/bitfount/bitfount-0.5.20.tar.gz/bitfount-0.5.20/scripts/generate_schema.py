"""Generates a schema file from a data file."""
from pathlib import Path
from typing import Any

import fire

from bitfount.data.datasource import DataSource
from bitfount.data.schema import BitfountSchema


def gen_schema(data_file: str, schema_file: str, **datasource_kwargs: Any) -> None:
    """Generates a schema file from a data file.

    Args:
        data_file: The path to the data file.
        schema_file: The path to save the generated schema to.
        datasource_kwargs: Additional keyword arguments to pass to the schema
                           alongside the data.
    """
    # Create DataSource
    datasource = DataSource(Path(data_file).expanduser())

    # Create schema
    if datasource_kwargs:
        print(f"DataSource kwargs: {datasource_kwargs}")
    schema = BitfountSchema(datasource, **datasource_kwargs)

    # Save schema
    schema.dump(Path(schema_file).expanduser())


def main() -> None:
    """Script entry point."""
    fire.Fire(gen_schema)


if __name__ == "__main__":
    main()
