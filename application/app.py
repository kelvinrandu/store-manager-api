from flask import Flask
from application.v1.resources.views import store_manager
from instance.config import app_config

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(app_config[config])

    app.register_blueprint(store_manager)

    return app






