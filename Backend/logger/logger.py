"""
Logger Manager - Singleton
Gestiona logs centralizados en la aplicación
"""

import logging
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
            fh = logging.FileHandler(LogConstants.LOG_FILE)
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
