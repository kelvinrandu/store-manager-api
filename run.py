import os
from application.app import create_app

config_name = os.environ['APP_SETTINGS']
app = create_app(config_name)



if __name__ == '__main__':
    app.run(debug=True)