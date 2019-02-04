import requests
import json
import click
from game_database.settings import Config
from game_database.database.models import Game
from game_database.database.models import Platform
from game_database.database import db
from sqlalchemy import or_
from game_database.giantbomb import headers


def populate_games():
    params = {'api_key': Config.GIANT_BOMB_API_KEY,
              'format': 'json',
              'limit': '100',
              'field_list': 'name,deck,platforms'}

    total_elements = 0
    error = False

    database_platforms = db.session.query(Platform).filter(or_(Platform.abbreviation.in_ (['PS1', 'PS2', 'PS3', 'PS4', 'NES', 'SNES','N64', 'GB','GBA', 'PC']))).all()

    for platform in database_platforms:
        params['filter'] = 'platform:' + platform.id.__str__()
        games_request = requests.get('https://www.giantbomb.com/api/games/', params=params, headers=headers)
        if games_request.status_code == 200:
            response = json.loads(games_request.content)

            for responseObject in response['results']:
                game = Game(name=responseObject['name'],
                    deck=responseObject['deck'], platform_id=platform.id, deleted=False)
                db.session.add(game)
                db.session.commit()
            total_elements = total_elements + response['number_of_page_results']
            click.echo('At - ' + total_elements.__str__())

        else:
            error = True
            click.echo('Error - ' + games_request.status_code.__str__())
            break

    return error
