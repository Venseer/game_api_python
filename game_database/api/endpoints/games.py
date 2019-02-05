import logging

from flask_restplus import Resource
from game_database.api.restplus import my_api
from game_database.database.models import Game
from game_database.database import db
from game_database.api.endpoints.game_detail import GameResult

log = logging.getLogger(__name__)
ns = my_api.namespace('games', description='Games controller')



@ns.route('/')
class GamesCollections(Resource):

    @my_api.response(200, 'Game list.')
    def get(self):
        """
        Returns a list of games
        """
        result = []

        query = db.session.query(Game).\
                filter(Game.deleted == False)

        result_list = query.all()
        for res in result_list:
            result.append(GameResult(res).__dict__)
        return result, 200
