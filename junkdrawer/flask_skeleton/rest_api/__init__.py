from importlib import import_module
import logging, logging.handlers
import os

from flask import flask
from yaml import safe_load


CONFIG_FP_EV = "<CONFIG_FP_EV>"   # Name of environment variable that has config filepath
TEST_FLAG_EV = "<TEST_FLAG_EV>"    # Name of environment variable that is the test flag
TEST_ENDPOINTS_MODULE_EV = "<TEST_ENDPOINTS_MODULE_EV>"  #


def create_app(config=None):
    app = Flask("<app_name>")

    # Use gunicorn logging mechanism
    # (REF: https://medium.com/@trstringer/logging-flask-and-gunicorn-the-manageable-way-2e6f0b8beb2f)
    if __name__ != "__main__":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    # --- Initialize App ---
    CONFIG_FILE = os.environ.get(CONFIG_FP_EV)

    return app
