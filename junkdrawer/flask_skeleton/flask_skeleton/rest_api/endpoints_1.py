from flask import (Blueprint, make_response, json, redirect, request,
    url_for, abort, current_app)

endpoints_1 = Blueprint("endpoints_1", __name__)

# NOTE: Flask logging is supressed when not in 'debug' mode,
# unless log at the 'error' level

# NOTE: 'current_app' will give us access to the Flask app object


# -- Endpoints --

@endpoints_1.route("/")
def index():
    return redirect(url_for("endpoints_1.flask_skeleton"))


@endpoints_1.route("/flask_skeleton")
def flask_skeleton():
    """Index root/landing endpoint."""
    
    # Can access 'current_app' in order to get app logger.
    current_app.logger.info("Root Endpoint hit.")
    
    # Access database if desired
    data = _get_db().query()

    text_banner = "BLAH"
    resp = make_response(text_banner, 200)
    resp.mimetype = "text/plain"
    return resp

# (Further endpoints)
#       .
#       .
#       .


# -- Internal --


def _get_db():
    """Return handler to database. Can do so because the database
    was attached to the app's config in 
    flask_skeleton.rest_api.__init__.create_app()
    """
    return current_app.config["database"]
