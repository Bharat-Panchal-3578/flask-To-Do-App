import os
from app import create_app

config_path = os.getenv( "FLASK_CONFIG", "app.config.DevelopmentConfig")
app = create_app(config_path)

if __name__ == "__main__":
    app.run()
