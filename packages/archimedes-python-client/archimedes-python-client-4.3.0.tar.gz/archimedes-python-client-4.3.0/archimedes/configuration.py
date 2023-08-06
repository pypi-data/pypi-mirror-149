import os
import abc
import pandas as pd
import requests

# Global archimedes config
USER_HOME_DIR = os.path.expanduser("~")
ARCHIMEDES_CONF_DIR = os.path.join(USER_HOME_DIR, ".archimedes")
SAVED_CONFIG_PATH = os.path.join(ARCHIMEDES_CONF_DIR, "arcl.json")
SAVED_MSAL_TOKEN_CACHE_PATH = os.path.join(ARCHIMEDES_CONF_DIR, "msal.cache.bin")

# Local archimedes config
ARCHIMEDES_API_CONFIG_URL = "https://arcl.optimeering.no/config.json"


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
    environment = os.getenv("ARCHIMEDES_ENVIRONMENT", "prod")
    return ApiConfig(environment)
