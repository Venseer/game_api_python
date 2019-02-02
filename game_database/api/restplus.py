import logging
from flask_restplus import Api


log = logging.getLogger(__name__)
my_api = Api(version='1.0', title='Game API', description='Game Database API')
