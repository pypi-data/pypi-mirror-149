import logging
import logging.config
import os

from .runtime_config import RuntimeConfig


def init_logger(verbose):
    """Init logger with config from either RuntimeConfig or a default."""
    levels = [logging.WARNING, logging.INFO, logging.DEBUG]
    log_level = levels[verbose if verbose < len(levels) else len(levels) - 1]

    try:
        logging.config.dictConfig(RuntimeConfig().logging)
        logging.debug(
            "Initialized logging from RuntimeConfig(%s)",
            RuntimeConfig(),
        )
    except (KeyError, ValueError) as err:
        logging.basicConfig(level=log_level)
        logging.warning(
            "Could not load logging config (%s), continuing with defaults.",
            err,
        )

    if verbose != 0:
        for name in logging.root.manager.loggerDict:
            logging.getLogger(name).setLevel(log_level)
            RuntimeConfig().logging["loggers"].update(
                {name: {"level": str(logging._levelToName[log_level])}}
            )


def set_and_init_logger(
    verbose: int,
    name: str,
    filename: str,
    level: str = "DEBUG",
    formatter: str = "debug",
    replace: bool = False,
):

    RuntimeConfig().logging["handlers"][name] = {
        "class": "logging.FileHandler",
        "formatter": formatter,
        "level": level,
        "mode": "w",
        "filename": os.path.join(os.getcwd(), filename),
    }
    if replace:
        RuntimeConfig().logging["root"]["handlers"] = [name]
    else:
        RuntimeConfig().logging["root"]["handlers"].append(name)

    init_logger(verbose)
