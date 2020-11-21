"""

-- Purpose

- I frequently just need to initialize a logger with a handler to a file.
I didnt like having to rewrite all the handler init and config every time.
- Additionally, I made this utility able to also return "fangless" loggers in that
it will return a logger with no filehandler, e.g. no logs will be produced
other than possible terminal output. I found this really useful as many customers
wanted scripts with the ability to toggle logging.

-- Usage

# Create default logger.
#   - Default log level is found at log.DEFAULT_LOG_LEVEL.
#   - Default log file is found at log.DEFAULT_LOG_FP
>>> from log import get_logger
>>> log = get_file_logger()
>>> log.warning("Terminus")    # Will log to default log filepath with default log level mask.

# Create logger with arguments.
>>> log = get_file_logger(fp="path_to_log.log", log_level="DEBUG")
>>> log.info("It pays to be obvious when you are known for subtlety.")

# Create "fangless" logger. (see notes above on purpose)
>>> from log import get_logger
>>> log = get_file_logger(enabled=False)

# To change get_logger() defaults, just edit these global vars in log.py
DEFAULT_LOG_FP = "<program_name>.log"
DEFAULT_LOG_LEVEL = "WARNING"
"""


import logging


DEFAULT_LOG_FP = "<program_name>.log"
DEFAULT_LOG_LEVEL = "WARNING"


def get_file_logger(enabled=True, fp=DEFAULT_LOG_FP, log_level=DEFAULT_LOG_LEVEL):
    """Create a logger that outputs to supplied filepath

    Args:
        enabled (bool): Whether logging is enabled. This function is called
            in scripts that call it with suppied arguments, and allows the
            scripts this utility blindly.
        fp (str): filename of the log
        log_level (str): Python logging level to set
        
    Returns:
        (logging.logger) logging handle
    """
    # no matter what a fangless logger is created (for cleaner code)
    logger = logging.getLogger(fp.split("/")[-1].split(".")[0])
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s \n',
                                  datefmt="%Y-%m-%d %H:%M:%S")
    
    if enabled:
        # set filehandler
        fh = logging.FileHandler(fp, mode='w')
        fh.setFormatter(formatter)
        fh.setLevel(getattr(logging, log_level.upper()))
        logger.addHandler(fh)

    return logger
