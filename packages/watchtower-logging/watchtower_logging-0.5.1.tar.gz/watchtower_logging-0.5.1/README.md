## WatchTower Logging

This module is meant to enable easy logging to a WatchTower Beam (endpoint).

### Installation

```
pip install watchtower_logging --upgrade
```

### Setting up the logger object
To instantiate a logger object do:
```
import watchtower_logging
logger = watchtower_logging.getLogger(host='my.example.host.com', beam_id='my_beam_id')
```
This returns a regular [Python logger](https://docs.python.org/3/howto/logging.html) object with an additional WatchTower handler that will send logs to the WatchTower endpoint that corresponds to the `beam_id` that is provided. This only works if this beam is public. If it is not, you have to provide the relevant token:
```
logger = watchtower_logging.getLogger(host='my.example.host.com', beam_id='my_beam_id', token='token')
```
You can also easily log to the console and/or to a file. You can do this by setting `console` to `True` and/or setting the `path` parameter to a valid pathname. Note that the file does not have to exist, however its parent directory does. Additionally, you can disable sending messages to WatchTower by setting `send` to `False`. This might be used for debugging purposes.
```
logger = watchtower_logging.getLogger(host='my.example.host.com', beam_id='my_beam_id', token='token', console=True, send=False, path='my_log_file.log')
```
As usual with logging in Python, you can provide a log level to the logger object. Only messages with a level equal to or higher than this level will be emitted. By default this is set to `START`.
```
logger = watchtower_logging.getLogger(host='my.example.host.com', beam_id='my_beam_id', token='token', level=watchtower_logging.ERROR)
```
The available levels are (in order of increasing importance): 
- DEBUG
- INFO
- START
- DONE
- WARNING
- ERROR
- CRITICAL

Note the two custom levels `START` and `DONE`. These are meant to signal the start and successful completion of a unit of code that we want to monitor. 

You can alter the log level by using `setLevel`
```
logger.setLevel(watchtower_logging.DEBUG)
```
Logging messages are send using a diffent thread and a queue, as not to halt the regular flow of the program. This may however cause unexpected ordering in log messages and other print statements that you might have in your code. 
Additionaly, threading is not allowed in Google Cloud Functions. Therefore threading is automatically disabled in this environment (based on the presence of  environment variables `FUNCTION_TARGET` and `K_SERVICE` or `GCP_PROJECT` and `FUNCTION_NAME`, which are automatically set in GCF).
You can manually disable threading by setting `use_threading` to `False`.
```
logger = watchtower_logging.getLogger(host='my.example.host.com', beam_id='my_beam_id', token='token', use_threading=False)
```
The logger also provides an `execution_id` that can be used to group multiple messages together in the resulting logs. By default this `execution_id` is a randomly generated string of 10 digits and lowercase letters. It is generated when the logger object is instantiated. You can set the `execution_id` manually:
```
logger = watchtower_logging.getLogger(host='my.example.host.com', beam_id='my_beam_id', token='token', execution_id='my_unique_id')
```
Setting the `execution_id` to a different value after instantiating the logger object is done by using the `setExecutionId` method:
```
logger.setExecutionId(execution_id='my_different_unique_id')
```
If you call this method without an argument, the `execution_id` will be set to a new random string.

You can attach default data to the logger. This data is send with each subsequent logging request. This can be done in the `.getLogger` method:
```
watchtower_logging.getLogger(..., default_data={'foo': 'bar'})
```
or later on using the `.setDefaultData` method exposed by the logger:
```
logger.setDefaultData(data={'foo': 'bar'})
```
This data will be appended to any default data that might have been set earlier (overwriting conflicting fields). If you want overwrite the current default data completely, you can set the argument `overwrite` to `True` (this can be used to clear default data):
```
logger.setDefaultData(data={'foo': 'bar'}, overwrite=True)
logger.setDefaultData(data={}, overwrite=True) # to clear all default data.
```
When instantiating a logger instance, using `.getLogger`, by default the code adds the watchtower handler to the exception hook. In other words, all uncaught exceptions will be automatically logged to watchtower, even without a `try`-`except` block containing all your code. The log level will be `CRITICAL`. Note: in Google Cloud Functions this is known not to work sometimes. Best to just use a `try`-`except` block there. Note2: adding the exception handler happens from the moment you setup the watchtower logger using `.getLogger`. So a good way to go would be:
```
import watchtower_logging
logger = watchtower_logging.getLogger(...)

# all your other imports and code
```
You can disable the exception hook using the `catch_all` argument:
```
logger = watchtower_logging.getLogger(host='my.example.host.com', beam_id='my_beam_id', token='token', catch_all=False)
```

Finally, you can flag the data when you're developing an application that sends data to watchtower, but you do not want this data to show up (by default) in dashboards or alerts. For this you can use the `dev` argument to get a logger in development mode:
```
logger = watchtower_logging.getLogger(host='my.example.host.com', beam_id='my_beam_id', token='token', dev=True)
```
### Logging
In your code you can easily emit messages with a certain level by using the methods with names corresponding to the levels that are defined above (lowercase).
```
logger.debug('This is a debug message')
logger.info('This is an info message')
logger.start('Emit me at the start')
logger.done('Emit me upon successful completion')
logger.warning('This is a warning')
logger.error('This is an error message`)
logger.critical('This is a critical message')
```
The payload that will be send to WatchTower will look something like this:
```
{
    "asctime": "2021-01-15T19:16:52.429908+0000", 
    "name": "watchtower_logging", 
    "levelname": "INFO", 
    "severity": 20,
    "message": "This is an info message", 
    "execution_id": "8ft05jdq5t",
    "dev": false
}
```
For log messages with a level of `ERROR` or higher, traceback information will be included automatically within a `data` object. So for example:
```
{
    "asctime": "2021-01-15T19:19:17.387699+0000", 
    "name": "watchtower_logging", 
    "levelname": "ERROR", 
    "severity": 40,
    "message": "invalid literal for int() with base 10: 'not a number'", 
    "data": {
        "traceback": "Traceback (most recent call last):\n  File \"C:/Users/jpnoo/PycharmProjects/watch-tower-logging/example.py\", line 10, in <module>\n    int('not a number')\nValueError: invalid literal for int() with base 10: 'not a number'\n" }, 
    "execution_id": "fe6v5p29tx",
    "dev": false
}
```
You can also add additional data to your logging record by providing a dictionary to the `data` parameter. This dictionary has to be convertable to a JSON string (so do not pass `datetime` objects for example, but pass their corresponding string representations).
```
logger.info('This is an info message', data={'foo': 'bar', 'non-personal': 'information'})
```
This will send a payload like this:
```
{
    "asctime": "2021-01-15T11:19:32+0100", 
    "name": "watchtower_logging", 
    "levelname": "INFO", 
    "severity": 20,
    "message": "This is an info message", 
    "data": {
        "foo": "bar", 
        "non-personal": "information" }, 
    "execution_id": "rp0a87s5gm",
    "dev": false
}
```
Be careful not to send personal data to WatchTower.

### Logging in Django
To enable easy logging in Django there is a special `DjangoWatchTowerHandler` class. You can use this by including `watchtower_logging>=0.2.2` in your `requirements.txt` file and the following in you Django settings file :
```
WT_BEAM_ID = 'your_watchtower_beam_id'
WT_HOST = 'the.relevant.hostname'
WT_PROTOCOL = 'https' # when omitted, defaults to https
WT_TOKEN = 'beam_token' # can be omitted if the beam is public
WT_DEV = True # set the False in production. In most cases you can make it equal to the Django DEBUG variable in the settings

# You can adjust different logging levels to suit your needs:
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'watchtower': {
            '()': 'watchtower_logging.watchtower_logging.CustomJsonFormatter',
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(levelno)s - %(exc_info)s - %(filename)s - %(funcName)s - %(lineno)d - %(module)s - %(pathname)s - %(message)s',
            'datefmt': '%Y-%m-%dT%H:%M:%S.%f%z'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
        'watchtower': {
            'class': 'watchtower_logging.django.DjangoWatchTowerHandler',
            'level': 'ERROR',
            'formatter': 'watchtower'
        }
    },
    'root': {
        'handlers': ['console', 'watchtower'],
        'level': 'WARNING',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'watchtower'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
```
