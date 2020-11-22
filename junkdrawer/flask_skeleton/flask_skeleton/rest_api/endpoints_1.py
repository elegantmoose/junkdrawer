from flask import (Blueprint, make_response, json, redirect, request,
    url_for, abort, current_app)

endpoints_1 = Blueprint("endpoints_1", __name__)


# -- Endpoints --

# NOTE: Flask logging is supressed when not in 'debug' mode,
# unless log at the 'error' level

@endpoints_1.route("/")
def index():
    return redirect(url_for("endpoints_1.flask_skeleton"))


@endpoints_1.route("/flask_skeleton")
def flask_skeleton():
    """Index root/landing endpoint."""
    text_banner = "BLAH"
    resp = make_response(text_banner, 200)
    resp.mimetype = "text/plain"
    return resp

# (Further endpoints)
#       .
#       .
#       .