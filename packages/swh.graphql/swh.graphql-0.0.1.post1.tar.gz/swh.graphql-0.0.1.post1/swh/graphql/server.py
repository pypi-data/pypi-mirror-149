import os
from typing import Any, Dict, Optional

from swh.core import config
from swh.storage import get_storage as get_swhstorage

graphql_cfg = None
storage = None


def get_storage():
    global storage
    if not storage:
        storage = get_swhstorage(**graphql_cfg["storage"])
    return storage


def load_and_check_config(config_path: Optional[str]) -> Dict[str, Any]:
    """Check the minimal configuration is set to run the api or raise an
       error explanation.

    Args:
        config_path: Path to the configuration file to load

    Raises:
        Error if the setup is not as expected

    Returns:
        configuration as a dict

    """
    if not config_path:
        raise EnvironmentError("Configuration file must be defined")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file {config_path} does not exist")

    cfg = config.read(config_path)
    if "storage" not in cfg:
        raise KeyError("Missing 'storage' configuration")

    return cfg


def make_app_from_configfile():
    """Loading the configuration from
    a configuration file.

    SWH_CONFIG_FILENAME environment variable defines the
    configuration path to load.

    """
    from .app import schema

    global graphql_cfg

    if not graphql_cfg:
        config_path = os.environ.get("SWH_CONFIG_FILENAME")
        graphql_cfg = load_and_check_config(config_path)

    if graphql_cfg.get("server-type") == "asgi":
        from ariadne.asgi import GraphQL

        application = GraphQL(schema)
    else:
        from ariadne.wsgi import GraphQL

        application = GraphQL(schema)
    return application
