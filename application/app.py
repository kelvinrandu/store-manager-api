from flask import Flask
from application.v1.resources.views import store_manager
from instance.config import app_config
from flask_jwt_extended import JWTManager

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(app_config[config])

    app.register_blueprint(store_manager)

    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    jwt = JWTManager(app)

    return app






