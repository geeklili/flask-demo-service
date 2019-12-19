from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_sqlalchemy import SQLAlchemy
from config import config

mongo = PyMongo()
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    CORS(app)
    db.init_app(app)

    mongo.init_app(app)

    from . import api
    app.register_blueprint(api.bp)

    return app
