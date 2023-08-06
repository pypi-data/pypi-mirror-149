from .watchtower_logging import getLogger
from .watchtower_logging import logLevels
from .version import __version__

DEBUG = logLevels.DEBUG
INFO = logLevels.INFO
START = logLevels.START
DONE = logLevels.DONE
WARNING = logLevels.WARNING
ERROR = logLevels.ERROR
CRITICAL = logLevels.CRITICAL