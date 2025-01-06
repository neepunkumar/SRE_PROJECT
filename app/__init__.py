from flask import Flask
from app.api import api_blueprint
from app.prometheus_metrics import setup_metrics
from app.logger import setup_logger
from app.config import Config  # Import the Config class

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Load the configuration from Config class
    app.register_blueprint(api_blueprint)
    setup_metrics(app)
    setup_logger(app)
    return app