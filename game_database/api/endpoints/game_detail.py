import logging

from flask_restplus import Resource, reqparse
from game_database.api.restplus import my_api
from game_database.database.models import Game
from game_database.database import db
from game_database.api.endpoints.platform_detail import Platform, PlatformResult

log = logging.getLogger(__name__)
ns = my_api.namespace('game', description='Game Controller')

get_parser = reqparse.RequestParser()
get_parser.add_argument('game_id', type=int)


insert_parser = reqparse.RequestParser()
insert_parser.add_argument('game_name', type=str)
insert_parser.add_argument('game_deck', type=str)
insert_parser.add_argument('platform_id', type=int)

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('game_id', type=int)

update_parser = reqparse.RequestParser()
update_parser.add_argument('game_id', type=int)
update_parser.add_argument('game_name', type=str)
update_parser.add_argument('game_deck', type=str)
update_parser.add_argument('platform_id', type=int)


@ns.route('/')
class GamesCollections(Resource):

    @my_api.response(200, 'Game found.')
    @my_api.response(400, 'Request error.')
    @my_api.response(201, 'Game not found.')
    @my_api.expect(get_parser, validate=True)
    def get(self):
        """
        Returns a game.
        """
        game_id = get_parser.parse_args()['game_id']
        if game_id is None:
            return 'Game id can not be empty.', 400
        query = db.session.query(Game, Platform). \
                filter(Game.deleted == False). \
                filter(Game.id == game_id). \
                join(Game.platform)

        game_result = query.one_or_none()
        if game_result is None:
            return 'Game not found', 201
        return GameResult(game_result[0], game_result[1]).__dict__, 200

    @my_api.expect(insert_parser, validate=True)
    @my_api.response(200, 'Platform successfully created.')
    @my_api.response(400, 'Request Error.')
    def post(self):
        """
        Adds a new Game
        """
        arguments = insert_parser.parse_args()
        exists = db.session().query(Platform).filter(Platform.id == arguments['platform_id']).scalar()
        if exists is None:
            return 'Platform does not exist', 400
        if exists.deleted:
            return 'Platform is deleted', 400
        game = Game(name=arguments['game_name'], deck=arguments['game_deck'], platform_id=arguments['platform_id'],
                    deleted=False)
        db.session.add(game)
        db.session.commit()
        return GameResult(game).__dict__, 200

    @my_api.expect(delete_parser, validate=True)
    @my_api.response(200, 'Game deleted.')
    @my_api.response(400, 'Game not found.')
    def delete(self):
        """
        Deletes a game
        """
        arguments = delete_parser.parse_args()
        game = Game.query.filter(Game.deleted == False).filter(Game.id == arguments['game_id']).first()
        if game is not None:
            game.deleted = True
            db.session.commit()
            return GameResult(game).__dict__
        else:
            return 'Game not found.', 400

    @my_api.expect(update_parser, validate=True)
    @my_api.response(200, 'Game successfully updated.')
    def put(self):
        """
        Updates a Game
        """
        arguments = update_parser.parse_args()
        game = Game.query.get(arguments['game_id'])
        if game is None:
            return 'Game does not exist', 400
        game.platform_id = arguments['platform_id']
        game.name = arguments['game_name']
        game.deck = arguments['game_deck']
        db.session.commit()
        return GameResult(game).__dict__, 200


class GameResult:
    def __init__(self, game=None, platform=None):
        if game is not None:
            self.id = game.id
            self.name = game.name
            self.deck = game.deck
        if platform is not None:
            self.platform_id = game.platform_id
            self.platform = PlatformResult(platform).__dict__
