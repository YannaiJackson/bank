import logging
import logging.handlers
from app.load_config import config


class Logger:
    _instance = None
    _logger = None

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        log_config = config.get("logging", {})

        log_level = log_config.get("level", "DEBUG").upper()
        log_format = log_config.get("format", '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        log_to_file = log_config.get("file", None)

        # Set up logger with the desired level
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(getattr(logging, log_level))  # Set dynamic log level

        formatter = logging.Formatter(log_format)

        # Stream handler (console logging)
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self._logger.addHandler(stream_handler)

        # File handler (if specified in config)
        if log_to_file:
            file_handler = logging.handlers.RotatingFileHandler(
                log_to_file, maxBytes=10 * 1024 * 1024, backupCount=3
            )
            file_handler.setFormatter(formatter)
            self._logger.addHandler(file_handler)

    def get_logger(self):
        return self._logger


# Create a Logger instance that will be used across the app
logger = Logger()
