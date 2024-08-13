from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_cors import CORS
import os

# Import blueprints
from .api import api_blueprint

def create_app():
    """Create and configure an instance of the Flask application."""
    app = Flask(__name__)

    # Configuration
    app.config.from_object('config.Config')

    # Enable CORS if needed
    CORS(app)

    # Initialize MongoDB
    mongo = PyMongo(app)

    # Setup JWT Manager
    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(api_blueprint, url_prefix='/api')

    # Error Handling
    @app.errorhandler(404)
    def not_found(error):
        """Error handler for 404 Not Found."""
        return {"error": "Resource not found"}, 404

    @app.errorhandler(500)
    def internal_error(error):
        """Error handler for 500 Internal Server Error."""
        return {"error": "Internal server error"}, 500

    return app