from flask import current_app, g
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()  # Create a global SQLAlchemy instance

def get_db():
    if 'db' not in g:
        g.db = db.engine
    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.dispose()