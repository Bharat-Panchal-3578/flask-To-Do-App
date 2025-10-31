import os
from app import create_app

<<<<<<< HEAD
config_path = os.getenv( "FLASK_CONFIG", "app.config.ProductionConfig")
=======
config_path = os.getenv("FLASK_CONFIG", "app.config.ProductionConfig")
>>>>>>> 33a87e0 (Refactor: updated footer links, added some styling for responsiveness in small screen sizes and minor tweaks before Azure deployment)
app = create_app(config_path)

if __name__ == "__main__":
    app.run()
