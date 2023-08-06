from io import TextIOWrapper
import json
import logging
import logging.config
import os
import sys
from typing import Union

_DEFAULT_LOG_DIRS = ('./logs/info/', './logs/error/')
_DEFAULT_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "info": {
            "format": "%(asctime)s[%(levelname)s]%(pathname)s:%(funcName)s:%(message)s"
        },
        "error": {
            "format": "%(asctime)s[%(levelname)s]%(pathname)s:%(funcName)s:%(lineno)d:%(process)d-%(thread)d:%(message)s"
        }
    },
    "filters": {
        "cinfo": {
            "()": "al_utils.filter.RangeLevelFilter",
            "level": [
                10,
                20
            ]
        },
        "info": {
            "()": "al_utils.filter.RangeLevelFilter",
            "level": [
                20
            ]
        },
        "error": {
            "()": "al_utils.filter.RangeLevelFilter",
            "level": [
                30,
                40,
                50
            ]
        }
    },
    "handlers": {
        "console-info": {
            "class": "logging.StreamHandler",
            "level": "DEBUG",
            "formatter": "info",
            "stream": "ext://sys.stdout",
            "filters": [
                "cinfo"
            ]
        },
        "console-error": {
            "class": "logging.StreamHandler",
            "level": "WARNING",
            "formatter": "error",
            "stream": "ext://sys.stderr",
            "filters": [
                "error"
            ]
        },
        "info_file_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "INFO",
            "formatter": "info",
            "filename": os.path.join(_DEFAULT_LOG_DIRS[0],"info.log"),
            "when": "W0",
            "backupCount": 14,
            "encoding": "utf8",
            "filters": [
                "info"
            ]
        },
        "error_file_handler": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "level": "WARNING",
            "formatter": "error",
            "filename": os.path.join(_DEFAULT_LOG_DIRS[1],"error.log"),
            "when": "W0",
            "backupCount": 14,
            "encoding": "utf8",
            "filters": [
                "error"
            ]
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "console-info",
            "console-error",
            "info_file_handler",
            "error_file_handler"
        ]
    }
}


def _package_name(path: str, project_name: str = None) -> str:
    """
    Get package name

    :param path:
        Relative path from :param:``project_name`` to file.
        Should contain :param:``project_name`` at first, such as: ``<project_name>/a/b/c.py``.
    :param project_name: Project's name. Current project folder by default.
    :return: package_name.file_name_without_ext. If :param:`path` not contain :param:`project_name`, it return `<project_name>.default`

    Example
    ------
    >>> _package_name('al_utils/a/b/c.py','al_utils') # 'a.b.c'
    >>> _package_name('/others/a/b/c.py','al_utils') # 'al_utils.default'
    """
    project_name = project_name or os.path.basename(
        os.getcwd())
    path = path.replace('\\', '/')[:path.rfind('.')]
    p = path.split('/')
    if project_name in p:
        return '.'.join(p[p.index(project_name) + 1:])
    return f'{project_name}.default'


class Logger:
    """
    Logger wrapper.
    """
    DEFAULT_LOGGING_CONFIG = _DEFAULT_LOGGING_CONFIG

    def __init__(self, class_name: str = '', config: Union[str, TextIOWrapper, dict] = _DEFAULT_LOGGING_CONFIG):
        """
        Create a logger using :param:`config_file`.

        Set <package>.<file>.<class_name> as logger name.

        :param class_name: 类名
        :param config: Json logging configuration file path, or readable file, or a dict config.
        """
        dict_config: dict = {}
        # check log dirs
        if config == _DEFAULT_LOGGING_CONFIG:
            os.makedirs('./logs/info', exist_ok=True)
            os.makedirs('./logs/error', exist_ok=True)
        # load config
        if isinstance(config, dict):
            dict_config = config
        elif isinstance(config, TextIOWrapper):
            dict_config = json.load(config)
        elif isinstance(config, str):
            with open(config, 'r') as f:
                dict_config = json.load(f)
        else:
            raise TypeError(
                'config must be one of str, file or dict, but got %s' % type(config))
        logging.config.dictConfig(dict_config)
        # get caller file's path
        log_path: str = _package_name(sys._getframe(1).f_code.co_filename)
        # logger name: <package>.<file>.<class_name>
        self.logger = logging.getLogger(f'{log_path}.{class_name}')
