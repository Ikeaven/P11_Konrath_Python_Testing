from flask import Blueprint

public_board = Blueprint('public_board', __name__)
from . import views