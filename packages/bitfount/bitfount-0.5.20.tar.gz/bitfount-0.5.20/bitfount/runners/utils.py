"""Utility functions for the runner modules."""
from datetime import datetime
import logging
import os
from pathlib import Path
import sys
from typing import Dict, List, Optional, cast
import urllib

from yaml import SafeLoader, ScalarNode

from bitfount.config import BITFOUNT_LOGS_DIR

logger = logging.getLogger(__name__)


def setup_loggers(
    loggers: List[logging.Logger], name: Optional[str] = None
) -> List[logging.Logger]:
    """Set up loggers with console and file handlers.

    Creates a logfile in 'logs' directory with the current date and time and outputs all
    logs at the "DEBUG" level. Also outputs logs to stdout at the "INFO" level. A common
    scenario is to attach handlers only to the root logger, and to let propagation take
    care of the rest.

    Args:
        loggers (List[logging.Logger]): logger(s) to setup
        name (Optional[str], optional): creates a subdirectory inside BITFOUNT_LOGS_DIR
            if provided. Defaults to None.

    Returns:
        List[logging.Logger]: updated logger(s)
    """
    handlers: List[logging.Handler] = []

    # Check if logging to file is not disabled
    if os.environ.get("BITFOUNT_LOG_TO_FILE", "true") == "true":
        # Create directory if it doesn't exist
        parent_logfile_dir = (
            Path(os.environ.get("BITFOUNT_LOGS_DIR", ".")) / BITFOUNT_LOGS_DIR
        )
        logfile_dir = parent_logfile_dir if not name else parent_logfile_dir / name
        logfile_dir.mkdir(parents=True, exist_ok=True)

        # Set file logging configuration
        file_handler = logging.FileHandler(
            f"{logfile_dir}/{datetime.now():%Y-%m-%d-%H%M%S}.log"
        )
        file_log_formatter = logging.Formatter(
            "%(asctime)s %(thread)-12d [%(levelname)-8s] %(name)s: %(message)s"
        )
        file_handler.setFormatter(file_log_formatter)
        file_handler.setLevel(logging.DEBUG)
        handlers.append(file_handler)

    # Set console logging configuration
    console_handler = logging.StreamHandler(sys.stdout)
    console_log_formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s]: %(message)s", datefmt="%H:%M:%S"
    )
    console_handler.setFormatter(console_log_formatter)
    console_handler.setLevel(logging.INFO)
    handlers.append(console_handler)

    # Cannot use `logger` as iter-variable as shadows outer name.
    for i_logger in loggers:
        # Clear any existing configuration
        list(map(i_logger.removeHandler, i_logger.handlers))
        list(map(i_logger.removeFilter, i_logger.filters))

        # Set base level to DEBUG and ensure messages are not duplicated
        i_logger.setLevel(logging.DEBUG)
        i_logger.propagate = False

        # Add handlers to loggers
        list(map(i_logger.addHandler, handlers))

    return loggers


# Extract environment variables to pass to the yaml format constructor.

# TODO: [BIT-1613] Update to parse any environment variable specified in connection string # noqa: B950
def format_constructor(loader: SafeLoader, node: ScalarNode) -> str:
    """Format constructor for passing variables in yaml file.

    This is used only for adding the environment variables to the pod yaml config.
    """
    values: Dict[str, str]
    try:
        username = os.environ.get("USERNAME").strip()  # type: ignore[union-attr] # Reason: it is in a try...except statement # noqa: B950
        password = urllib.parse.quote_plus(
            os.environ.get("DBPASSWORD")  # type: ignore[arg-type] # Reason: it is in a try...except statement # noqa: B950
        ).strip()
        db_host = os.environ.get("DBHOST").strip()  # type: ignore[union-attr] # Reason: it is in a try...except statement # noqa: B950
        db_name = os.environ.get("DBNAME").strip()  # type: ignore[union-attr] # Reason: it is in a try...except statement # noqa: B950
        values = {
            "username": username,
            "password": password,
            "db_host": db_host,
            "db_name": db_name,
        }
    except Exception:
        values = {
            "username": "",
            "password": "",
            "db_host": "",
            "db_name": "",
        }
    return cast(str, loader.construct_scalar(node)).format(**values)
