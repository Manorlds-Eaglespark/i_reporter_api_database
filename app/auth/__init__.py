# auth/__init__.py

from . import views
from flask import Blueprint

auth_blueprint = Blueprint('auth', __name__)
