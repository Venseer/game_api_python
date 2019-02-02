import os


class Config(object):
    # Flask settings
    FLASK_SERVER_NAME = 'localhost:2001'
    FLASK_DEBUG = True  # Do not use debug mode in production

    # Flask-Restplus settings
    RESTPLUS_SWAGGER_UI_DOC_EXPANSION = 'list'
    RESTPLUS_VALIDATE = True
    RESTPLUS_MASK_SWAGGER = False
    RESTPLUS_ERROR_404_HELP = False

    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite')
    db_uri = 'sqlite:///{}'.format(db_path)

    # SQLAlchemy settings
    SQLALCHEMY_DATABASE_URI = db_uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
