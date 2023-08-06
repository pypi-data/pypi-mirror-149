"""Contains courtesy classes and functions for making pod running easier."""
import logging
from os import PathLike
from pathlib import Path
from typing import Union

import desert
import yaml

from bitfount.data.utils import DatabaseConnection
from bitfount.federated.pod import Pod
from bitfount.federated.pod_keys_setup import _get_pod_keys
from bitfount.hub.helper import _create_access_manager, _create_bitfounthub
from bitfount.runners.config_schemas import DatabaseConfig, PathConfig, PodConfig
from bitfount.runners.utils import format_constructor

logger = logging.getLogger(__name__)


def setup_pod_from_config_file(path_to_config_yaml: Union[str, PathLike]) -> Pod:
    """Creates a pod from a YAML config file.

    Args:
        path_to_config_yaml: The path to the config file.

    Returns:
        The created pod.
    """
    logger.debug(f"Loading pod config from: {path_to_config_yaml}")
    yaml.SafeLoader.add_constructor("!format", format_constructor)
    with open(path_to_config_yaml) as f:
        config_yaml = yaml.safe_load(f)
    config = desert.schema(PodConfig).load(config_yaml)
    return setup_pod_from_config(config)


def setup_pod_from_config(config: PodConfig) -> Pod:
    """Creates a pod from a loaded config.

    Args:
        config: The configuration as a PodConfig instance.

    Returns:
        The created pod.
    """
    bitfount_hub = _create_bitfounthub(config.username, config.hub.url)
    access_manager = _create_access_manager(
        bitfount_hub.session, config.access_manager.url
    )

    # Load Pod Keys
    pod_directory = bitfount_hub.user_storage_path / "pods" / config.pod_name
    pod_keys = _get_pod_keys(pod_directory)

    # Extra data reference to DatabaseConnection or Path
    data: Union[DatabaseConnection, Path]
    if isinstance(config.data, DatabaseConfig):
        data = config.data.get_db_connection()
    elif isinstance(config.data, PathConfig):
        data = config.data.path

    return Pod(
        name=config.pod_name,
        data=data,
        data_config=config.data_config,
        schema=config.schema,
        pod_details_config=config.pod_details,
        bitfounthub=bitfount_hub,
        ms_config=config.message_service,
        access_manager=access_manager,
        pod_keys=pod_keys,
        approved_pods=config.other_pods,
    )
