from game_database import create_app
from game_database.database import db
from game_database.giantbomb import platforms
from game_database.giantbomb import games

import click

application = create_app()


@application.cli.command()
def clean_database():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        click.echo('Clearing table %s' % table)
        db.session.execute(table.delete())
    db.session.commit()
    click.echo('Database cleared.')


@application.cli.command()
def populate_database():
    meta = db.metadata
    for table in reversed(meta.sorted_tables):
        db.session.execute(table.delete())
    db.session.commit()

    click.echo('Platform table...')
    has_error = platforms.populate_platforms()
    if not has_error:
        click.echo('Ok!')
        click.echo('Games table...')

    has_error = has_error or games.populate_games()
    
    if not has_error:
        click.echo('Ok!')
        click.echo('Database cleared and populated.')

