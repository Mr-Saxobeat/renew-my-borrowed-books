import os
import logging


class LoggerApi(logging.Logger):
    """Custom logger for API application"""

    LOG_LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }

    def __init__(self, name='root'):
        """
        Initialize the logger
        :param name: name of the logger
        """
        super().__init__(name)

        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
        handler.setFormatter(formatter)
        
        self.addHandler(handler)
        self.setLevel(self._get_log_level())

    def _get_log_level(self):
        level = os.getenv('LOG_LEVEL', 'info').lower()
        return self.LOG_LEVELS.get(level, logging.INFO)