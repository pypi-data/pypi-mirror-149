# -*- coding: utf-8 -*-
import pprint
import logging
import sys
from pathlib import Path

from .utils import get_caller_module_name, load_yaml_to_dict, update_dict_recursively
from .decorators import cache_return

C = None
HANDY_LOG_KEY = "handy-log"
DEFAULT_STYLE = "{"
DEFAULT_CONFIG_PATH = Path(Path(sys.modules[__name__].__file__).parent, "{}.yaml".format(HANDY_LOG_KEY)).absolute()
SAMPLE_CONFIG_PATH = Path(Path(sys.modules[__name__].__file__).parent, "{}-sample.yaml".format(HANDY_LOG_KEY)).absolute()
USER_CONFIG_PATH = Path(Path(), "{}.yaml".format(HANDY_LOG_KEY)).absolute()


def init(config_path=None, encoding="utf-8"):
    global C
    C = load_yaml_to_dict(DEFAULT_CONFIG_PATH, encoding="utf-8")

    if config_path is None:
        if USER_CONFIG_PATH.exists():
            config_path = USER_CONFIG_PATH
    else:
        config_path = Path(config_path).absolute()
        assert config_path.exists(), "The specified log config file does not exist: {}".format(config_path)

    if config_path is not None:
        user_config = load_yaml_to_dict(config_path, encoding=encoding)
        update_dict_recursively(C, user_config)

    import logging.config
    logging.config.dictConfig(C)
    info("{} initialized! Configured by:", HANDY_LOG_KEY)
    info("Default config file: {}", DEFAULT_CONFIG_PATH)
    if config_path is not None:
        info("And user config file: {}", config_path)
    else:
        info("Refer here as a sample config: {}", SAMPLE_CONFIG_PATH)
    debug("CONFIG DETAIL start:\n{}", pprint.pformat(C))
    debug("CONFIG DETAIL end here.")


def _init_if_necessary():
    if isinstance(C, dict):
        return
    init()


@cache_return
def _get_style():
    _init_if_necessary()
    style = C.get(HANDY_LOG_KEY, {}).get("style", DEFAULT_STYLE)
    assert style in ["{", "%"], "Message format style can only be '{' or '%', " \
                                "now it's: {}".format(style)
    return style


def _pre_format_msg(msg, *args):
    style = _get_style()
    if style == "{":
        return msg.format(*args)
    # Can leave this condition to the built-in logger?
    if style == "%":
        return msg % args


def _log(level, msg, *args, **kwargs):
    """
    Log 'msg % args' or 'msg.format(*args)'
    with the integer severity 'level' on the logger of current module.

    Difficult to support: 'msg.format(*args, **kwargs)'.
    This requires to pop all the keys from kwargs which have been exhausted by msg.
    """
    _init_if_necessary()
    module_name, _ = get_caller_module_name(stacklevel=2)
    logger = logging.getLogger(module_name)
    msg = _pre_format_msg(msg, *args)
    if "stacklevel" not in kwargs:
        kwargs["stacklevel"] = 3
    logger.log(level, msg, **kwargs)


def critical(msg, *args, **kwargs):
    """
    Log a message with severity 'CRITICAL' on the logger of current module.
    """
    _log(logging.CRITICAL, msg, *args, **kwargs)


def error(msg, *args, **kwargs):
    """
    Log a message with severity 'ERROR' on the logger of current module.
    """
    _log(logging.ERROR, msg, *args, **kwargs)


def exception(msg, *args, exc_info=True, **kwargs):
    """
    Log a message with severity 'ERROR' on the logger of current module,
    with exception information.
    """
    error(msg, *args, exc_info=exc_info, **kwargs)


def warning(msg, *args, **kwargs):
    """
    Log a message with severity 'WARNING' on the logger of current module.
    """
    _log(logging.WARNING, msg, *args, **kwargs)


def info(msg, *args, **kwargs):
    """
    Log a message with severity 'INFO' on the logger of current module.
    """
    _log(logging.INFO, msg, *args, **kwargs)


def debug(msg, *args, **kwargs):
    """
    Log a message with severity 'DEBUG' on the logger of current module.
    """
    _log(logging.DEBUG, msg, *args, **kwargs)
