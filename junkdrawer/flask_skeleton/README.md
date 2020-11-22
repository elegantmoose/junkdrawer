# Flask Skeleton

A useful Flask skeleton to jumpstart a Flask web/REST API framework.

### Neat components/tips of the skeleton:

1. Using a configuration file and env variables to control app startup and configuration.
  - Initializing Flask app for production mode or testing mode.
  - Using blueprints and having ability to dynamically load blueprints 
    (sets of endpoints) based on runtime configuration file.

  See files for implementation:
    - [flask_skeleton.rest_api.__init__.py](flask_skeleton/rest_api/__init__.py)
    - [flask_skeleton.rest_api.endpoints_1.py](flask_skeleton/rest_api/endpoints_1.py)
    - [config.yml](config.yml)

2. Loading a database module/backend and attaching to Flask app for access from any endpoints module.

  See files for implementation:
    - [flask_skeleton.rest_api.__init__.py](flask_skeleton/rest_api/__init__.py)
    - [flask_skeleton.database.db.py](flask_skeleton/database/db.py)
    - [config.yml](config.yml)

3. Attaching Flask app to gunicorn logging mechanism.

  See files for implementation:
    - [flask_skeleton.rest_api.__init__.py](flask_skeleton/rest_api/__init__.py)

4. Starting Flask app with script, where runtime config can be supplied to script via command line.

  See files for implemenation:
    - [flask_skeleton.scripts.start_flask_app.py](flask_skeleton/scripts/start_flask_app.py)

5. Utilizing Flask's test client (https://flask.palletsprojects.com/en/1.1.x/testing/) fixture for testing endpoints; as well with the ability to dynamically configure and load in different Blueprints (endpoints) for testing.

  See files for implementation:
    - [flask_skeleton.tests.rest_api.test_rest_endpoints_1.py](flask_skeleton/tests/rest_api/test_rest_api_endpoints_1.py)
    - [flask_skeleton.tests.conftest.py](flask_skeleton/tests/conftest.py)
    - [flask_skeleton.tests.test_config.yml](flask_skeleton/tests/test_config.py)

