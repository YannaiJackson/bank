import yaml


class ConfigLoader:
    _instance = None
    _config = None  # This should be an instance-level attribute

    def __new__(cls, config_path="config.yml"):
        if not cls._instance:
            cls._instance = super(ConfigLoader, cls).__new__(cls)
            cls._instance._load_config(config_path)
        return cls._instance

    def _load_config(self, config_path):
        with open(config_path, "r") as file:
            self._config = yaml.safe_load(file)  # Use self._config here

    def get_config(self):
        return self._config


# Create a ConfigLoader instance that will be used across the app
config = ConfigLoader()
