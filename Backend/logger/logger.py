"""
Logger Manager - Singleton
Gestiona logs centralizados en la aplicación
"""

import logging
from pathlib import Path
from Backend.patterns.singleton import Singleton
from Backend.constants import LogConstants


class LoggerManager(Singleton):
    """
    Gestor de logs - Singleton
    Solo una instancia de logger en toda la app
    """

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self.logger = logging.getLogger("visualion_app")
            self.logger.setLevel(LogConstants.LOG_LEVEL)

            # File handler
            log_file = Path(LogConstants.LOG_FILE)
            if not log_file.is_absolute():
                log_file = Path(__file__).resolve().parents[1] / log_file
            log_file.parent.mkdir(parents=True, exist_ok=True)

            fh = logging.FileHandler(log_file)
            fh.setLevel(logging.DEBUG)

            # Console handler
            ch = logging.StreamHandler()
            ch.setLevel(logging.INFO)

            # Formatter
            formatter = logging.Formatter(LogConstants.LOG_FORMAT)
            fh.setFormatter(formatter)
            ch.setFormatter(formatter)

            self.logger.addHandler(fh)
            self.logger.addHandler(ch)

            self._initialized = True

    def get_logger(self):
        return self.logger


# Instancia global
logger_manager = LoggerManager()
