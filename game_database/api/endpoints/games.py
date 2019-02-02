import logging

from flask_restplus import Resource, reqparse
from game_database.api.restplus import my_api
from game_database.database.models import Game

log = logging.getLogger(__name__)
ns = my_api.namespace('game', description='Games list')

parser = reqparse.RequestParser()
parser.add_argument('game_name', type=str)
parser.add_argument('game_deck', type=str)
parser.add_argument('platform_id', type=int)


@ns.route('/')
class GamesCollections(Resource):

    def get(self):
        """
        Returns a list of games
        """
        return Game.query.all()

    @my_api.expect(parser, validate=True)
    def post(self):
        arguments = parser.parse_args()
        test = arguments['game_name']

