import argparse
from importlib import import_module
import multiprocessing as mp
import os
import signal
from yaml import safe_load
import sys
import subprocess
from time import sleep

from flask_skeleton.rest_api import CONFIG_FP_EV, DEFAULT_CONFIG_FP


def _get_argparser():
    """ """
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-c",
        "--config",
        action="store",
        dest="config_fp",
        default=DEFAULT_CONFIG_FP,
    )

    return parser


def main():
    #mp.set_start_method('spawn')   # May need to do this on MacOS to work on python<=3.7

    parser = _get_argparser()
    args = vars(parser.parse_args())
    args["config_fp"] = os.path.abspath(args["config_fp"])
    CONFIG = safe_load(open(args["config_fp"], 'r'))

    # Declare process handlers so can define sigint hander w/o
    # Python complaining
    flask_app_server = None

    #sigint handler (i.e. kill server if ctrl-c the script in terminal)
    def signal_handler(sig, frame):
        flask_app_server.terminate()
        if flask_app_server.poll() is None:
            sleep(2)
            flask_app_server.kill()
        exit()
    signal.signal(signal.SIGINT, signal_handler)  # Interuption
    signal.signal(signal.SIGTERM, signal_handler) # Termination

    # Flask app needs the config, so set environment variable
    # to where the config is found
    os.environ[CONFIG_FP_EV] = args["config_fp"]

    # Start Flask server
    flask_app_server = subprocess.Popen([
        "gunicorn",
        "-b",
        ":".join([str(CONFIG["rest_api"]["host"]), str(CONFIG["rest_api"]["host"])]),
        "--log-file",
        CONFIG["rest_api"]["log_fp"],
        "--log-level",
        CONFIG["rest_api"]["log_level"],
        "flask_skeleton.rest_api.create_app()"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    while True:
        sleep(1)


if __name__ == "__main__":
    main()
