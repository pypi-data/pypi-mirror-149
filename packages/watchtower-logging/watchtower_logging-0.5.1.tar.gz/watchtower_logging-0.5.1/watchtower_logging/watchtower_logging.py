import logging
import os
import types
from watchtower_logging.watchtower_handler import WatchTowerHandler
from watchtower_logging.exceptions import loggingException
from watchtower_logging.version import __version__
from pythonjsonlogger import jsonlogger
import random
import string
import datetime
import pytz
import traceback
import sys
import hashlib
import json

DONE_LEVEL_NUM = logging.INFO + 4
START_LEVEL_NUM = logging.INFO + 2
EXECUTION_ID_LENGTH = 10
DEFAULT_FLUSH_INTERVAL = 5.0
logging.addLevelName(DONE_LEVEL_NUM, 'DONE')
logging.addLevelName(START_LEVEL_NUM, 'START')

if hasattr(random, 'choices'):
    random_choices = random.choices
else:
    from watchtower_logging.utils import random_choices

DEDUP_ID_KEY = 'dedup_id'

class logLevels(object):

    DEBUG = logging.DEBUG
    INFO = logging.INFO
    START = START_LEVEL_NUM
    DONE = DONE_LEVEL_NUM
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


def logaction(self, msg, lvl_num, args, data=None, **kws):
    if self.isEnabledFor(lvl_num):

        if hasattr(self, '_default_data') and isinstance(self._default_data, dict):
            if data is None:
                data = self._default_data
            else:
                data = {**self._default_data, **data}

        if not data is None:
            if lvl_num >= logLevels.ERROR:
                if not 'traceback' in data:
                    if not sys.exc_info()[2] is None:
                        data['traceback'] = traceback.format_exc()

            if 'extra' in kws:
                if 'data' in kws['extra']:
                    raise loggingException('Duplicate `data` key, please merge the data you are passing with the entry in `extra`.')
                else:
                    extra = kws.pop('extra')
                    extra = {'data': data, **extra}
            else:
                extra = {'data': data}
        else:
            extra = kws.pop('extra', {})

            if lvl_num >= logLevels.ERROR:
                if not sys.exc_info()[2] is None:
                    data = {'traceback': traceback.format_exc()}
                else:
                    data = {}
                if 'data' in extra:
                    raise loggingException('Duplicate `data` key, please merge the data you are passing with the entry in `extra`.')
                extra['data'] = data

        if not self._execution_id is None:
            extra['execution_id'] = self._execution_id

        # adding deduplication-id
        if self.dedup and not DEDUP_ID_KEY in extra:
            if not self.dedup_keys is None and isinstance(self.dedup_keys, (list, tuple, set)):
                dedup_data = {k:v for k,v in extra.items() if k in self.dedup_keys}
                if 'msg' in self.dedup_keys or 'message' in self.dedup_keys:
                    dedup_data['__msg__'] = msg
            else:
                dedup_data = extra
                dedup_data['__msg__'] = msg
            dedup_id = hashlib.md5(json.dumps(dedup_data,
                                              sort_keys=True,
                                              indent=None,
                                              separators=(',',':')).encode('utf-8')).hexdigest()

            extra[self.dedup_id_key] = dedup_id

        # Yes, logger takes its '*args' as 'args'.
        self._log(lvl_num, msg, args, extra=extra, **kws)


def done(self, msg, *args, data=None, **kws):
    self.logaction(msg=msg, lvl_num=DONE_LEVEL_NUM, args=args, data=data, **kws)

def start(self, msg, *args, data=None, **kws):
    self.logaction(msg=msg, lvl_num=START_LEVEL_NUM, args=args, data=data, **kws)

def logdebug(self, msg, *args, data=None, **kws):
    self.logaction(msg=msg, lvl_num=logging.DEBUG, args=args, data=data, **kws)

def info(self, msg, *args, data=None, **kws):
    self.logaction(msg=msg, lvl_num=logging.INFO, args=args, data=data, **kws)

def warning(self, msg, *args, data=None, **kws):
    self.logaction(msg=msg, lvl_num=logging.WARNING, args=args, data=data, **kws)

def error(self, msg, *args, data=None, **kws):
    self.logaction(msg=msg, lvl_num=logging.ERROR, args=args, data=data, **kws)

def critical(self, msg, *args, data=None, **kws):
    self.logaction(msg=msg, lvl_num=logging.CRITICAL, args=args, data=data, **kws)

def setExecutionId(self, execution_id=None):
    if execution_id is None:
        self._execution_id = ''.join(random_choices(string.ascii_lowercase + string.digits, k=EXECUTION_ID_LENGTH))
    else:
        self._execution_id = execution_id

def setDefaultData(self, data, overwrite=False):
    if not isinstance(data, dict):
        raise loggingException('Default data needs to be a dictionary')
    if not overwrite and hasattr(self, '_default_data') and isinstance(self._default_data, dict):
        self._default_data = {**self._default_data, **data}
    else:
        self._default_data = data

class CustomJsonFormatter(jsonlogger.JsonFormatter):

    converter = datetime.datetime.utcfromtimestamp

    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        ct = pytz.utc.localize(ct)
        if datefmt:
            s = ct.strftime(datefmt)
        else:
            t = ct.strftime("%Y-%m-%d %H:%M:%S%z")
            s = "%s,%03d" % (t, record.msecs)
        return s

    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if 'levelno' in log_record:
            log_record['severity'] = log_record.pop('levelno')



def getLogger(beam_id, name=None, execution_id=None, token=None, host=None, protocol=None, dev=False, default_data=None,
              level=logLevels.START, debug=False, path=None, console=False, send=True, use_threading=None, dedup=True,
              dedup_keys=None, retry_count=3, catch_all=True, dedup_id_key=None):

    # create logger
    name = name or os.environ.get('FUNCTION_NAME', 'watchtower-logging')
    logger = logging.getLogger(name)
    logger.logaction = types.MethodType(logaction, logger)
    logger.done = types.MethodType(done, logger)
    logger.start = types.MethodType(start, logger)
    logger.debug = types.MethodType(logdebug, logger)
    logger.info = types.MethodType(info, logger)
    logger.warning = types.MethodType(warning, logger)
    logger.error = types.MethodType(error, logger)
    logger.critical = types.MethodType(critical, logger)
    logger.setExecutionId = types.MethodType(setExecutionId, logger)
    logger.setLevel(level)
    logger.setDefaultData = types.MethodType(setDefaultData, logger)
    logger.dedup = dedup
    logger.dedup_keys = dedup_keys
    logger.dedup_id_key = dedup_id_key or DEDUP_ID_KEY

    if default_data:
        logger.setDefaultData(data=default_data)

    if send:
        if use_threading is None:
            if ((not os.environ.get('GCP_PROJECT') is None) and (not os.environ.get('FUNCTION_NAME') is None)) or \
                    ((not os.environ.get('FUNCTION_TARGET') is None) and (not os.environ.get('K_SERVICE') is None)):
                # Cloud Functions does not allow threading, so set to negative flush interval -> blocking calls
                flush_interval = -1.0
            else:
                flush_interval = DEFAULT_FLUSH_INTERVAL
        elif use_threading:
            flush_interval = DEFAULT_FLUSH_INTERVAL
        else:
            # set to negative flush interval -> blocking calls
            flush_interval = -1.0

        if len(logger.handlers) == 0 or not any(isinstance(handler, WatchTowerHandler) for handler in logger.handlers):

            # create watchtower handler and set level
            wh = WatchTowerHandler(beam_id=beam_id, token=token, debug=debug, host=host, protocol=protocol,
                                   retry_count=retry_count, version=__version__, flush_interval=flush_interval, dev=dev)
            wh.setLevel(level)

            # create formatter
            formatter = CustomJsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(levelno)s - %(message)s - %(dev)s',
                                             datefmt="%Y-%m-%dT%H:%M:%S.%f%z")
            # add formatter to wh
            wh.setFormatter(formatter)

            # add wh to logger
            logger.addHandler(wh)

    if not path is None:

        if len(logger.handlers) == 0 or not any(isinstance(handler, logging.FileHandler) for handler in logger.handlers):

            fh = logging.FileHandler(path)
            fh.setLevel(level)
            f_formatter = CustomJsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                                 datefmt="%Y-%m-%dT%H:%M:%S.%f%z")
            fh.setFormatter(f_formatter)
            logger.addHandler(fh)

    if console:

        if len(logger.handlers) == 0 or not any(isinstance(handler, logging.StreamHandler) for handler in logger.handlers):

            ch = logging.StreamHandler()
            ch.setLevel(level)
            c_formatter = CustomJsonFormatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                                 datefmt="%Y-%m-%dT%H:%M:%S.%f%z")
            ch.setFormatter(c_formatter)
            logger.addHandler(ch)

    if catch_all:

        import sys

        def watchtower_handle_exception(exc_type, exc_value, exc_traceback):
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                return

            logger.critical('Uncaught Exception', data={'traceback': '{exc_type}: {exc_value}\n{traceback}'.format(exc_type=exc_type.__name__,
                                                                                                                   exc_value=exc_value,
                                                                                                                   traceback=''.join(traceback.format_tb(exc_traceback)))})
            sys.__excepthook__(exc_type, exc_value, exc_traceback)

        sys.excepthook = watchtower_handle_exception

    logger.setExecutionId(execution_id=execution_id)

    return logger