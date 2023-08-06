from flask import Flask
from dms_app.config import Config
from flask_cors import CORS
from dms_app.router import register_routes
from .namespace import api, ns


class App:
    config = Config()

    def create_app(self):
        flask_app = Flask(__name__)
        flask_app.config.from_object(self.config)
        CORS(flask_app, resources={r"*": {"origins": ["*"]}})
        flask_app.config["CORS_HEADERS"] = "Content-Type"
        flask_app.config["CORS_ORIGINS"] = "*"
        api.init_app(flask_app)
        register_routes(ns)
        return flask_app
