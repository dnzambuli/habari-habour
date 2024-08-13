import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from . import db

def create_app(test_config=None):
    '''
    Create and configure an instance of the Flask application.

    Args:
    - test_config (dict, optional): Configuration settings to use for testing.

    Returns:
    - app: Instance of Flask configured with database and routes.
    '''
    # Load environment variables
    load_dotenv()

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI=f'mysql+mysqlconnector://{os.environ["MYSQL_USER"]}:{os.environ["MYSQL_PASSWORD"]}@{os.environ["MYSQL_HOST"]}/{os.environ["MYSQL_DATABASE"]}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False
    )

    db.init_app(app)

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.update(test_config)
    
    try:
        os.makedirs(app.instance_path, exist_ok=True)  # exist_ok=True makes the OSError handling redundant
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
