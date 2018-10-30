from flask import Flask
from application.v1.resources.views import store_manager
from instance.config import APP_CONFIG
from flask_jwt_extended import JWTManager



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(APP_CONFIG[config_name])

    app.register_blueprint(store_manager)

    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    jwt = JWTManager(app)

    return app






