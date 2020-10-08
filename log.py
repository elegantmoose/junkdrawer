
import logging


DEFAULT_LOG_FP = "/var/log/program_name.log"


def get_logger(enabled=True, fp=DEFAULT_LOG_FP, log_level="WARNING"):
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
