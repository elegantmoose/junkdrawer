from importlib import import_module
import logging, logging.handlers
import os

from flask import Flask
from yaml import safe_load


DEFAULT_CONFIG_FP = "/etc/flask_skeleton/config.yml"
CONFIG_FP_EV = "FLASK_SKELETON_CONFIG"   # environment variable that has config filepath
TEST_FLAG_EV = "TEST_FLAG"    # environment variable that is the test flag
TEST_ENDPOINTS_MODULE_EV = "TEST_BLUEPRINT_MODULE"  # environment variable that holds test Blueprint/endpoints full module name


def create_app(config=None):
    app = Flask("Flask Skeleton")

    # Use gunicorn logging mechanism
    # (REF: https://medium.com/@trstringer/logging-flask-and-gunicorn-the-manageable-way-2e6f0b8beb2f)
    if __name__ != "__main__":
        gunicorn_logger = logging.getLogger("gunicorn.error")
        app.logger.handlers = gunicorn_logger.handlers
        app.logger.setLevel(gunicorn_logger.level)

    # --- Initialize App ---
    CONFIG_FILE = os.environ.get(CONFIG_FP_EV)

    if os.environ.get(TEST_FLAG_EV, default="False") != "True":
        # -- production mode --
        app.logger.critical("Production mode set.")
        app.config["config"] = safe_load(open(CONFIG_FILE, 'r'))

        # Initialize database/backend
        db_module = import_module(app.config["database"]["module"])
        app.config["database"] = getattr(db_module, "DatabaseHandler")(
            logger=app.logger,
            *app.config["module_config"]
        )

        # (any further initialization, maybe components/objects that REST
        # API will use.)
        #
        #

        # Load REST API
        endpoint_modules = []
        for module_name in app.config["endpoints"]:
            module_path = "flask_skeleton.rest_api." + module_name
            endpoint_modules.append(module_path)
            module = import_module(module_path)
            blueprint = getattr(module, module_name)   # Blueprint has same name as module
            app.register_blueprint(blueprint)

        app.logger.critical(f"Endpoints loaded: {endpoint_modules}")

    else:
        # -- test mode --
        app.logger.critical("Test mode set.")

        # Add endpoints from module supplied through env variable
        module = import_module(os.environ[TEST_ENDPOINTS_MODULE_EV])
        module_name = os.environ[TEST_ENDPOINTS_MODULE_EV].split(".")[-1]
        blueprint = getattr(module, module_name)   # Blueprint has same name as module
        app.register_blueprint(blueprint)

    return app
