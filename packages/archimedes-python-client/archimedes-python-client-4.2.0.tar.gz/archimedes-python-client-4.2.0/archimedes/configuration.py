import os
from typing import Optional
import abc
import pandas as pd
from dynaconf import Dynaconf
import requests

# Global archimedes config
USER_HOME_DIR = os.path.expanduser("~")
ARCHIMEDES_CONF_DIR = os.path.join(USER_HOME_DIR, ".archimedes")
SAVED_CONFIG_PATH = os.path.join(ARCHIMEDES_CONF_DIR, "arcl.json")
SAVED_MSAL_TOKEN_CACHE_PATH = os.path.join(ARCHIMEDES_CONF_DIR, "msal.cache.bin")

# Local archimedes config
CONFIG_FILE_NAME = "archimedes.toml"
CONFIG_ENV_VAR_PREFIX = "ARCHIMEDES"

ARCHIMEDES_API_CONFIG_URL = "https://arcl.optimeering.no/config.json"


class ConfigNotFoundException(Exception):
    pass


def _find_config_file_path(path=None) -> Optional[str]:
    """Find the path to the archimedes.toml file"""
    if path is None:
        path = os.path.abspath(os.getcwd())

    if CONFIG_FILE_NAME in os.listdir(path):
        return os.path.join(path, CONFIG_FILE_NAME)

    new_path = os.path.dirname(path)
    if new_path == path:
        return None

    return _find_config_file_path(new_path)


def _find_root_folder():
    """Find the root folder of the project"""
    config_file_path = _find_config_file_path()
    if config_file_path is None:
        raise FileNotFoundError(f"Missing the {CONFIG_FILE_NAME} configuration file.")
    return os.path.dirname(config_file_path)


def get_config():
    config_file_path = os.getenv("ARCHIMEDES_CONFIG_FILE_PATH")
    return Dynaconf(
        envvar_prefix=CONFIG_ENV_VAR_PREFIX,
        settings_files=[_find_config_file_path(config_file_path)],
    )


class ArchimedesConstants:
    DATE_LOW = pd.to_datetime("1900-01-01T00:00:00+00:00")
    DATE_HIGH = pd.to_datetime("2090-01-01T00:00:00+00:00")


class InvalidEnvironmentException(Exception):
    pass


class ApiConfig(abc.ABC):
    def __init__(self, env):
        config_result = requests.get(ARCHIMEDES_API_CONFIG_URL)
        self.config = config_result.json()
        if env not in self.config.keys():
            raise InvalidEnvironmentException(
                f"Invalid environment {env}, "
                f"supported values are {', '.join([str(key) for key in self.config.keys()])}"
            )
        self.environment = env.lower()

    def __getattr__(self, item):
        env_config = self.config[self.environment]
        return env_config[item]


def get_api_config():
    environment_override = os.getenv("ENVIRONMENT")
    environment = (
        environment_override
        if environment_override
        else get_config().project.environment
    )
    return ApiConfig(environment)
