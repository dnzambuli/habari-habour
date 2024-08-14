from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy
import click

db = SQLAlchemy()  # Create a global SQLAlchemy instance

def get_db():
    if 'db' not in g:
        # Create a new SQLAlchemy session if not already in g
        g.db = db.session
    return g.db

def close_db(e=None):
    db_session = g.pop('db', None)

    if db_session is not None:
        db_session.close()

def init_db():
    db_session = get_db()

    with current_app.open_resource('schema.sql') as f:
        sql_commands = f.read().decode('utf8')
        db_session.execute(sql_commands)  # Executes the SQL commands read from the file
        db_session.commit()  # Commit the changes

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
