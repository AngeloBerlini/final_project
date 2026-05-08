from flask import Blueprint

circuits_bp = Blueprint('circuits', __name__)

from app.circuits import routes  # noqa: E402, F401
