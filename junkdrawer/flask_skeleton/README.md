# Flask Skeleton

A useful Flask skeleton to jumpstart a Flask web/REST API framework

Neat components/tips in skeleton:
- Using a configuration file and env variables to control app startup and configuration.
    - Initializing Flask app for production mode or testing mode.
    - Using blueprints and having ability to dynamically load blueprints 
    - (sets of endpoints) based on runtime configuration file.
- Attaching Flask app to gunicorn logging mechanism.
- Loading a database module/backend and attaching to Flask app for access from any Blueprints (endpoints).
- Starting flask app with script, where runtime config can be supplied.
- Utilizing Flask's test client (https://flask.palletsprojects.com/en/1.1.x/testing/) fixture for testing endpoints.
