from flask import Flask
from config import config
from .load_data_from_json import load_competitions, load_clubs

competitions = load_competitions()
clubs = load_clubs()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .public_board import public_board as public_board_blueprint
    app.register_blueprint(public_board_blueprint)

    return app
