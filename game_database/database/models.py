from game_database.database import db
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Platform(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    abbreviation = db.Column(db.String)
    deleted = db.Column(db.Boolean, nullable=False)


class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    deck = db.Column(db.String)
    platform_id = db.Column(db.Integer, ForeignKey('platform.id'))
    platform = relationship("Platform")
    deleted = db.Column(db.Boolean, nullable=False)
