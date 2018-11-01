import os
from application.app import create_app
from application.database import conn,create_tables




config_name = os.environ['APP_SETTINGS']
app = create_app(config_name)
create_tables()

if __name__ == '__main__':
    app.run(debug=True)