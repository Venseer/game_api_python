import requests
import json
import click
from game_database.settings import Config
from game_database.database.models import Platform
from game_database.database import db
from game_database.giantbomb import headers


def populate_platforms():
    params = {'api_key': Config.GIANT_BOMB_API_KEY,
              'format': 'json',
              'field_list': 'id,name,abbreviation'}

    elements_received = 0
    total_elements = 0
    first_run = True
    error = False

    while first_run or total_elements > elements_received:
        params['offset'] = elements_received
        platform_request = requests.get('https://www.giantbomb.com/api/platforms/', params=params, headers=headers)
        if platform_request.status_code == 200:
            response = json.loads(platform_request.content)

            if first_run:
                total_elements = response['number_of_total_results']
                first_run = False

            for responseObject in response['results']:
                platform = Platform(id=responseObject['id'], name=responseObject['name'],
                                    abbreviation=responseObject['abbreviation'], deleted=False)
                db.session.add(platform)
            db.session.commit()
            elements_received = elements_received + response['number_of_page_results']
            click.echo('At - ' + elements_received.__str__())

        else:
            error = True
            click.echo('Error - ' + platform_request.status_code.__str__())
            break

    return error
