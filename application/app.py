from flask import Flask
from application.v1.resources.views import store_manager
from instance.config import APP_CONFIG
from flask_jwt_extended import JWTManager
from application.database import conn, create_tables



def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(APP_CONFIG[config_name])

    app.register_blueprint(store_manager)
    

    app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
    jwt = JWTManager(app)

    create_tables()

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        return jti in blacklist


    return app






