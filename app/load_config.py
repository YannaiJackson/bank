import yaml
from threading import Lock


class ConfigLoader:
    _instance = None
    _lock = Lock()
    _config = None

    def __new__(cls, config_path="config.yml"):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super(ConfigLoader, cls).__new__(cls)
                    cls._instance._load_config(config_path)
        return cls._instance

    def _load_config(self, config_path):
        with open(config_path, "r") as f:
            self._config = yaml.safe_load(f)

    def get(self, key, default=None):
        """
        Retrieve a value from the loaded config.

        Args:
            key (str): Dot-separated key to retrieve nested config values.
            default (any): Default value if key not found.

        Returns:
            any: The config value.
        """
        keys = key.split(".")
        value = self._config
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value


config = ConfigLoader()