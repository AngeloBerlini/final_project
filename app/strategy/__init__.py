from flask import Blueprint

strategy_bp = Blueprint('strategy', __name__)

from app.strategy import routes  # noqa: E402, F401
