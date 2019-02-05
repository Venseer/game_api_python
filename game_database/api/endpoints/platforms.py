import logging

from flask_restplus import Resource
from game_database.api.restplus import my_api
from game_database.database.models import Platform
from game_database.database import db
from game_database.api.endpoints.platform_detail import PlatformResult

log = logging.getLogger(__name__)
ns = my_api.namespace('platforms', description='Platforms controller')


@ns.route('/')
class PlatformCollection(Resource):

    @my_api.response(200, 'Platform found.')
    def get(self):
        """
        Returns a list of Platforms
        """
        result = []
        for platform in db.session.query(Platform).filter(Platform.deleted == False).all():
            result.append(PlatformResult(platform).__dict__)
        return result
