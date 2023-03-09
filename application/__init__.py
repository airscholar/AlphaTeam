from importlib import import_module

from flask import Flask


def register_blueprints(app):
    app.register_blueprint(import_module('application.home.routes').blueprint)


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)
    register_blueprints(app)
    return app
