from functools import wraps, total_ordering, partial
from enum import Enum
from abc import ABC, abstractmethod
from datetime import datetime
import sys

from lightweb4py.singleton import Singleton
from lightweb4py import settings


# Logger levels enumeration class
@total_ordering                 # implements all the other comparisons (Enum implements __eq__, we implement __lt__)
class LoggerLevel(Enum):
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented

    def __str__(self):
        return {0:'DEBUG', 1:'INFO', 2:'WARNING', 3:'ERROR', 4:'CRITICAL'}.get(self.value, f'Unknown({self.value})')


# Default logger level for the logging system
LOGGER_DEFAULT_LEVEL = LoggerLevel.DEBUG


# Abstract class implementing logger handler skeleton.
# Logger handler has similar function to that of the Python standard library:
# it implements formatting and writing log message to specific media and is called by Logger to do the job.
# This abstract class implements:
# - __init__() - turning handler on and off,
# setup of the minimum logging level for handler and default logging level for messages,
# - compose_message() - composing log message string,
# - validate_message() - deciding whether to write a log entry depending on the state of handler and message level.
# ATTRS:
# level - the minimum message logging level for the handler to log the message
# defaultLevel - default logging level for messages with no logging level specified
# isOn - flag showing whether the handler is on (logging messages)
class LoggerHandler(ABC):

    def __init__(self, name: str, level: LoggerLevel = None, default_level: LoggerLevel = None, is_on: bool = True):
        self.name = name
        self.level = level if level else LoggerFabric().defaultLevel
        self.defaultLevel = default_level if default_level else LoggerFabric().defaultLevel
        self.isOn = is_on

    @staticmethod
    def compose_message(message: str, level: LoggerLevel, logger_name: str = None, source: str = None) -> str:
        return "{}, {}, {}, {}, {}".format(datetime.now().isoformat(timespec='microseconds'),
                                           level,
                                           logger_name if logger_name else "",
                                           source if source else "",
                                           message)

    def validate_message(self, message: str, level: LoggerLevel = None, logger_name: str = None, source: str = None):
        message_level = level if level else self.defaultLevel
        if self.isOn and message_level >= self.level:
            return self.compose_message(message=message, level=message_level, logger_name=logger_name, source=source)
        else:
            return None

    # should be defined to implement the actual logging functionality
    # returns a tuple: flag indicating whether to log the message and the message itself
    @abstractmethod
    def log(self, message: str, level: LoggerLevel = None, logger_name: str = None, source: str = None) -> (bool, str):
        rendered_message = self.validate_message(message=message, level=level, logger_name=logger_name, source=source)
        return rendered_message is not None, rendered_message


# Concrete class of console logger handler. Implements actual writing to the console.
class LoggerConsoleHandler(LoggerHandler):

    def log(self, message: str, level: LoggerLevel = None, logger_name: str = None, source: str = None) -> bool:
        do_log, rendered_message = super().log(message=message, level=level, logger_name=logger_name, source=source)
        if do_log:
            print(rendered_message)
            return True
        else:
            return False


# Concrete class of file logger handler. Implements actual writing to a file.
# ATTRS:
# fileName - full path and file name of the log file to log messages to
class LoggerFileHandler(LoggerHandler):

    def __init__(self, name: str, file_name: str, level: LoggerLevel = None, default_level: LoggerLevel = None,
                 is_on: bool = True):
        self.fileName = file_name
        super().__init__(name=name, level=level, default_level=default_level, is_on=is_on)

    def log(self, message: str, level: LoggerLevel = None, logger_name: str = None, source: str = None) -> bool:
        do_log, rendered_message = super().log(message=message, level=level, logger_name=logger_name, source=source)
        if do_log:
            try:
                with open(self.fileName, 'a', encoding=settings.HTML_ENCODING) as f:
                    f.write(rendered_message + "\n")
                return True
            except IOError as e:
                print("LoggerFileHandler: I/O error({}): {}".format(e.errno, e.strerror))
            except:
                print("LoggerFileHandler: Unexpected error: ()".format(sys.exc_info()[0]))
            return False
        else:
            return False


# The Logger class dispatches log requests to the logger handlers configured for this logger instance.
# __init__() - initializes the logger by storing its handlers and default properties
# log() - check if should log the message by checking whether the logger is on and
# message logging level is not below the minimum logger logging level,
# then call all the handlers to actually log the message
# ATTRS:
# handlers - array of 0 or more handlers (function pointers) to dispatch messages to
# level - the minimum message logging level for the logger to log the message
# defaultLevel - default logging level for messages with no logging level specified
# isOn - flag showing whether the logger is on (logging messages)
class Logger:

    def __init__(self, name: str, handlers: [],
                 level: LoggerLevel = None, default_level: LoggerLevel = None,
                 success_on_any_log: bool = False, is_on: bool = True):
        # init handlers
        self.handlers = []
        for handler in handlers:        # Append all handlers that actually exist
            handler_ref = LoggerFabric().handlers.get(handler, None)
            if handler_ref:
                self.handlers.append(handler_ref)
        # init other parameters
        self.name = name
        self.level = level if level else LoggerFabric().defaultLevel
        self.defaultLevel = default_level if default_level else LoggerFabric().defaultLevel
        self.success_on_any_log = success_on_any_log
        self.isOn = is_on

    def log(self, message: str, level: LoggerLevel = None, source: str = None) -> bool:
        message_level = level if level else self.defaultLevel
        if self.isOn and message_level >= self.level:
            success = False if self.success_on_any_log else True
            for handler in self.handlers:
                success_this_log = handler.log(message=message, level=level, logger_name=self.name, source=source)
                if self.success_on_any_log:
                    success = success or success_this_log
                else:
                    success = success and success_this_log
            return success
        else:
            return False


# This class should be actually called by any app to reference a logger and then log a message
# __init__() - sets the actual logger, default logging level and message source reference
# for subsequent calls to the Log instance object
# __call__() - logs the message (calls a logger instance) filling in omitted parameters
# ATTRS:
# logger - the actual logger function
# default_level - default level for any message with no level specified
# default_source - default message source for any message with no source specified
class Log:

    def __init__(self, logger=None, default_level: LoggerLevel = None, default_source: str = None):
        # Get the specified logger reference, if none specified - the default logger, if set.
        self.logger = LoggerFabric().loggers.get(logger if logger else LoggerFabric().defaultLogger, None)
        # Set default log level if specified, if not - set default for the logger if exists or the system default
        self.default_level = default_level if default_level else \
            self.logger.defaultLevel if self.logger else LoggerFabric().defaultLevel
        # Set default source name if specified or blank otherwise
        self.default_source = default_source if default_source else ""

    def __call__(self, message: str, level: LoggerLevel = None, source: str = None) -> bool:
        if not self.logger or not LoggerFabric().isOn:      # exit if logger subsystem not yet init or is turned off
            return False
        return self.logger.log(message=message,
                               level=level if level else self.default_level,
                               source=source if source else self.default_source)


# Use this class to initialize the logging subsystem:
# turn in on and off, set handlers and loggers and the default message level
# ATTRIBUTES:
# isOn - logging is on flag
# loggers - dictionary of loggers - id and the respective Logger
# handlers - dictionary of handlers - id and the respective LoggerHandler
# defaultLogger - default logger if none specified
# defaultLevel - default logging level if not specified in individual messages
# (default is the first logger in the loggers dict)
class LoggerFabric(Singleton):

    # Pass a dictionary of logger files if you want to use multiple.
    # Every time __init__() is called, the logger list is updated
    def __init__(self, turn_on: bool = None,
                 handlers: dict = None, loggers: dict = None,
                 default_logger=None,  default_level: LoggerLevel = None):

        if not hasattr(self, 'isOn'):
            self.isOn = turn_on if turn_on is not None else True
        if turn_on is not None:
            self.isOn = turn_on

        # This should be called before initializing loggers and handlers - they use this default level at init
        if default_level:
            self.defaultLevel = default_level
        elif not hasattr(self, 'defaultLevel'):
            self.defaultLevel = LOGGER_DEFAULT_LEVEL

        # Init the handlers dictionary and set handlers if any passed
        if not hasattr(self, 'handlers'):       # initialize handlers dictionary if none yet
            self.handlers = {}
        if handlers:
            # first item in a given handler's dictionary is its class name, the rest are the initializer parameters
            for handler, parameters in handlers.items():
                self.handlers[handler] = globals()[parameters['handler']](**dict(list(parameters.items())[1:]))

        # Init the loggers dictionary and set loggers if any passed
        if not hasattr(self, 'loggers'):       # initialize loggers dictionary if none yet
            self.loggers = {}
        if loggers:
            # first item in a given handler's dictionary is its class name, the rest are the initializer parameters
            for logger, parameters in loggers.items():
                self.loggers[logger] = globals()[parameters['logger']](**dict(list(parameters.items())[1:]))

        # Init default logger
        if default_logger:
            self.defaultLogger = default_logger
        elif not hasattr(self, 'defaultLogger'):
            if self.loggers != {}:
                self.defaultLogger = next(iter(self.loggers))
            else:
                self.defaultLogger = None


# Decorator to enable logging for a function
# May be called in two ways:
# @debug - without parameters
# @debug(logger=logger, level=level) - specifying any or both of the keyword parameters: logger and level
# IDEA: https://pythonguide.readthedocs.io/en/latest/python/decorator.html
def debug(func=None, *, logger: str = None, level: LoggerLevel = LoggerLevel.DEBUG,
          message_before: str = None, message_after: str = None):
    if func is None:            # Function called with parameters - no function passed at the first argument position
        # prepend the function parameter
        return partial(debug, logger=logger, level=level,
                       message_before=message_before, message_after=message_after)

    @wraps(func)                # Pass this function's metadata into the nested function
    def logged_function(*args, **kwargs):
        log = Log(logger=logger if logger else LoggerFabric().defaultLogger,
                  default_level=level, default_source=func.__name__)
        log(message_before if message_before else "Execution started")
        func_result = func(*args, **kwargs)
        log(message_after if message_after else "Execution finished")
        return func_result
    return logged_function
