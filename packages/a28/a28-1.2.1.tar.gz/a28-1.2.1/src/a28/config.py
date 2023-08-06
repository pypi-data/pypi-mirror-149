"""Manage the CLI config file."""
import json
import os
from typing import Any, Dict

from a28 import utils


class ConfigError(Exception):
    """Custom exception for config errors."""

    pass


class ConfigFile:
    """Handles the config file storing token, endpoints and configs.

    `_save` is 'private' so that we're force to use ConfigFile as a
    context manager to load/save.
    """

    def __enter__(self) -> Dict[str, Any]:
        """Load the config file data on context creation."""
        self.data = self.load()
        return self.data

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Save the file to the disk on context exit."""
        return self._save(self.data)

    @staticmethod
    def get_token(region: str) -> str:
        """Retrieve the token from config.

        Load configuration information and return the token for the
        given region.
        """
        config = ConfigFile.load()

        if region not in config or 'token' not in config[region]:
            raise ConfigError('please authenticate')

        return config[region]['token']

    @staticmethod
    def load() -> Dict[str, Any]:
        """Load configuration information if information exists."""
        try:
            with open(utils.CONFIG) as json_file:
                data = json.load(json_file)
            return data
        except OSError:
            return {}
        except Exception as err:
            raise ConfigError(err)

    @staticmethod
    def _save(data: Dict[str, Any]) -> None:
        """Save all configuration values to the config file."""
        content = json.dumps(data, indent=4)

        # create the config path if it doesn't exist
        os.makedirs(utils.CONFIG_PATH, exist_ok=True)

        # save the configuration data to file
        with open(utils.CONFIG, 'w') as config:
            config.write(content)
