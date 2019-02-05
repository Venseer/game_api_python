import os
import logging.config
from flask import Flask, Blueprint

from game_database.settings import Config
from game_database.api.restplus import my_api
from game_database.api.endpoints.game_detail import ns as game_detail
from game_database.api.endpoints.platform_detail import ns as platform_detail
from game_database.api.endpoints.games import ns as games
from game_database.api.endpoints.platforms import ns as platforms
from game_database.database import db
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)
    logging_conf_path = os.path.normpath(os.path.join(os.path.dirname(__file__), '../logging.conf'))
    logging.config.fileConfig(logging_conf_path)
    log = logging.getLogger(__name__)

    app.config.from_object(Config)

    blueprint = Blueprint('api', __name__, url_prefix="/api")
    my_api.init_app(blueprint)
    my_api.add_namespace(game_detail)
    my_api.add_namespace(platform_detail)
    my_api.add_namespace(games)
    my_api.add_namespace(platforms)
    app.register_blueprint(blueprint)

    db.init_app(app)
    Migrate(app, db)

    return app
