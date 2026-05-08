from flask import Blueprint

telemetry_bp = Blueprint('telemetry', __name__)

from app.telemetry import routes
