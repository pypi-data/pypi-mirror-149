import os
import os.path
import logging.config
import logging
import logging.handlers
import sys

import traceback

import yaml
import logging_tree
from pyfakeuse import fake_use


def setup_scrapy():
    """ This is not needed as we pass 'LOG_ENABLED':False to scrapy at init time """

    def replace_configure_logging(install_root_handler=False, settings=None):
        fake_use(install_root_handler)
        fake_use(settings)

    def replace_log_scrapy_info(settings=None):
        fake_use(settings)

    # scrapy stuff
    # pylint: disable=import-outside-toplevel
    import scrapy.utils.log
    import scrapy.crawler
    logging_settings = {
        'LOG_ENABLED': False,
        'LOG_LEVEL': logging.WARN,
    }
    scrapy.utils.log.configure_logging(install_root_handler=False, settings=logging_settings)
    # are you watching closely?!?
    scrapy.crawler.configure_logging = replace_configure_logging
    scrapy.crawler.log_scrapy_info = replace_log_scrapy_info
    # print(scrapy.utils.log.log_scrapy_info)


# these control how to exception hook works
# these are also their default values (unless overridden by environment variables)
_print_traceback = False
_drill = True


def _excepthook(etype, value, tb):
    logger = logging.getLogger(__name__)
    # print the traceback but only if configured to do so
    if _print_traceback:
        # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
        if sys.version_info >= (3, 10):
            traceback.print_exception(value)
        else:
            traceback.print_exception(
                etype=etype,
                value=value,
                tb=tb,
            )
    # this loop will drill to the core of the problem
    # use only if this is what you want to show...
    # note that exception chaining is only a python 3 feature.
    if _drill:
        while value.__cause__:
            value = value.__cause__
    logger.exception(f"Exception occurred, type [{etype}], value [{value}]")


def _str2bool(s):
    """ convert a string to a boolean value """
    return s in {"True", "T", "true", "t", "yes", "y", "1"}


def setup_exceptions():
    """ Only print the heart of the exception and not the stack trace """
    # first set up the variables needed by the _excepthook function
    # pylint: disable=global-statement
    global _print_traceback, _drill
    local_print_traceback = os.getenv("PYLOGCONF_PRINT_TRACEBACK")
    if local_print_traceback is not None:
        _print_traceback = _str2bool(local_print_traceback)
    local_drill = os.getenv("PYLOGCONF_DRILL")
    if local_drill is not None:
        _drill = _str2bool(local_drill)
    # now that everything is ready attach the hook
    sys.excepthook = _excepthook


def setup_logging(level=None) -> None:
    """ setup the logging system """
    default_path_yaml = os.path.expanduser('~/.pylogconf.yaml')
    default_path_conf = os.path.expanduser('~/.pylogconf.conf')
    # this matches the default logging level of the logging
    # library and makes sense...

    dbg = os.getenv("PYLOGCONF_DEBUG", "False")
    if dbg == "False":
        dbg = False
    else:
        dbg = True

    # try YAML config file first
    value = os.getenv('PYLOGCONF_YAML', None)
    if value is None:
        path = default_path_yaml
    else:
        path = value
    if os.path.isfile(path):
        _debug(f'found logging configuration file [{path}]...', dbg)
        with open(path) as f:
            config = yaml.safe_load(f)
            logging.config.dictConfig(config)
            return

    # Now try regular config file
    value = os.getenv('PYLOGCONF_CONF', None)
    if value is None:
        path = default_path_conf
    else:
        path = value
    if os.path.isfile(path):
        _debug(f'found logging configuration file [{path}]...', dbg)
        logging.config.fileConfig(path)
        return

    _debug(f'logging with level [{level}]...', dbg)
    if level is None:
        env_level = os.getenv("PYLOGCONF_LEVEL")
        if env_level is None:
            level = logging.WARNING
        else:
            level = env_level

    logging.basicConfig(level=level)


def setup(level=None):
    """
    This is the main API that this module exposes. It sets up logging and exception handling
    :return:
    """
    setup_logging(level=level)
    setup_exceptions()


def show_tree():
    """ Show the logging tree """
    logging_tree.printout()


def _debug(msg, dbg):
    """
    debugging method for this module. Why do we need this? Why not use logging? Because we are setting up logging!
    The regular chicken and egg problem...
    :param msg:
    :param dbg:
    :return:
    """
    if dbg:
        print(msg)


file_data = """
---
# see http://victorlin.me/posts/2012/08/26/good-logging-practice-in-python
# values for level are: NOTSET, DEBUG, INFO, WARN, WARNING
version: 1
# if the next one is True then modules which do logger=logging.getLogger(__name__)
# out of any function will not see their logging.
disable_existing_loggers: True
formatters:
        simple:
                format: "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
handlers:
        console:
                class: logging.StreamHandler
                level: DEBUG
                formatter: simple
                stream: ext://sys.stdout
root:
        level: INFO
        handlers: [console]
        propagate: no
loggers:
        simple:
                level: INFO
"""


def create_pylogconf_file():
    with open(os.path.expanduser("~/.pylogconf.yaml"), "wt") as f:
        f.write(file_data)


def setup_syslog(name: str, level: int) -> None:
    """
    Configure systemd daemon type logging
    :param name:
    :param level:
    :return:
    """
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    handler = logging.handlers.SysLogHandler(address='/dev/log')
    root_logger.addHandler(handler)
    formatter = logging.Formatter(fmt=f'{name}[%(process)d]: %(levelname)s: %(message)s')
    handler.setFormatter(formatter)


# def setup_systemd(name: str, level: int) -> None:
#    root_logger = logging.getLogger()
#    root_logger.setLevel(level)
#    root_logger.addHandler(systemd.journal.JournaldLogHandler(
#        identifier=name,
#    ))


def remove_all_root_handlers():
    """
    This function can be used to reverse the effects of basicConfig
    :return:
    """
    root_logger = logging.getLogger()
    for x in root_logger.handlers:
        root_logger.removeHandler(x)
