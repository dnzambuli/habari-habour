import os

from flask import Flask
from dotenv import load_dotenv

def create_app(test_config = None):
    '''
    create_app is an application factory

    - app -> instance of Flask
    - __name__ -> current python module
    '''

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        SQLALCHEMY_DATABASE_URI=f'mysql+mysqlconnector://{os.environ.get("MYSQL_USER")}:{os.environ.get("MYSQL_PASSWORD")}@{os.environ.get("MYSQL_HOST")}/{os.environ.get("MYSQL_DATABASE")}',
        SQLALCHEMY_TRACK_MODIFICATIONS=False  # Optional for performance optimization
        )

    db = SQLAlchemy(app)

    if test_config is None:
        app.config.from_pyfile("config.py", silent = True)
    else:
        app.config.from_mapping(test_config)
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    @app.route('/hello')
    def hello():
        return 'Hello, World!'
    

    return app 