import logging

from flask_restplus import Resource, reqparse
from game_database.api.restplus import my_api
from game_database.database.models import Platform
from game_database.database import db

log = logging.getLogger(__name__)
ns = my_api.namespace('platforms', description='Platform List')

insert_parser = reqparse.RequestParser()
insert_parser.add_argument('platform_name', type=str)
insert_parser.add_argument('platform_abbreviation', type=str)

update_parser = reqparse.RequestParser()
update_parser.add_argument('platform_name', type=str)
update_parser.add_argument('platform_abbreviation', type=str)
update_parser.add_argument('platform_id', type=int)

delete_parser = reqparse.RequestParser()
delete_parser.add_argument('platform_id', type=int)


@ns.route('/')
class PlatformCollection(Resource):

    def get(self):
        """
        Returns a list of Platforms in the DB
        """
        result = []
        for platform in db.session.query(Platform).filter(Platform.deleted == False).all():
            result.append(PlatformResult(platform).__dict__)
        return result

    @my_api.expect(insert_parser, validate=True)
    @my_api.response(200, 'Platform successfully created.')
    def post(self):
        """
        Adds a new Platform
        """
        arguments = insert_parser.parse_args()
        platform = Platform(name=arguments['platform_name'], abbreviation=arguments['platform_abbreviation'], deleted=False)
        db.session.add(platform)
        db.session.commit()
        return PlatformResult(platform).__dict__

    @my_api.expect(update_parser, validate=True)
    @my_api.response(200, 'Platform successfully updated.')
    def put(self):
        """
        Updates a new Platform
        """
        arguments = update_parser.parse_args()
        platform = Platform.query.get(arguments['platform_id'])
        if platform is None:
            return 400, 'Platform not found.'
        platform.name = arguments['platform_name']
        platform.abbreviation = arguments['platform_abbreviation']
        db.session.commit()

        return PlatformResult(platform).__dict__

    @my_api.expect(delete_parser, validate=True)
    @my_api.response(200, 'Platform deleted.')
    @my_api.response(204, 'Platform not found.')
    def delete(self):
        """
        Delete a Platform
        """
        arguments = delete_parser.parse_args()
        platform = Platform.query.filter(Platform.deleted == False).filter(Platform.id == arguments['platform_id']).first()
        if platform is not None:
            platform.deleted = True
            db.session.commit()
            return PlatformResult(platform).__dict__
        else:
            return 'Platform not found.', 400


class PlatformResult:
    def __init__(self, platform):
        self.id = platform.id
        self.name = platform.name
        self.abbreviation = platform.abbreviation
