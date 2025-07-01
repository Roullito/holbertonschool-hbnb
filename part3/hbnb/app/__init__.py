# Import required Flask and extension libraries
from flask import Flask
from flask_restx import Api  # For organizing API with namespaces and documentation
from flask_bcrypt import Bcrypt  # For hashing passwords securely
from flask_jwt_extended import JWTManager  # For handling JWT-based authentication
from flask_sqlalchemy import SQLAlchemy  # SQLAlchemy ORM for database interaction

# Import all API namespaces (each file handles specific routes)
from hbnb.app.api.v1.users import api as users_ns
from hbnb.app.api.v1.amenities import api as amenities_ns
from hbnb.app.api.v1.places import api as places_ns
from hbnb.app.api.v1.reviews import api as review_ns
from hbnb.app.api.v1.auth import api as auth_ns
from hbnb.app.api.v1.protected import api as protected_ns

# Import the configuration dictionary (e.g., development, testing)
from config import config

# Initialize Flask extensions (they will be bound to the app later)
bcrypt = Bcrypt()  # Used for password encryption
jwt = JWTManager()  # Used for JSON Web Token auth management
db = SQLAlchemy()  # Used for database connection and ORM mapping

# Application factory function
def create_app(config_name="development"):
    # Create the Flask app
    app = Flask(__name__)

    # Load configuration from the selected config class (e.g., DevelopmentConfig)
    app.config.from_object(config[config_name])

    # Initialize all Flask extensions with the app
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)

    # Create all database tables based on defined SQLAlchemy models (if not already created)
    with app.app_context():
        db.create_all()

    # Initialize the API object with metadata
    api = Api(
        app,
        version='1.0',
        title='HBnB API',
        description='HBnB Application API'
    )

    # Register all namespaces (each one handles a group of related routes)
    api.add_namespace(users_ns, path='/api/v1/users')         # Handles user-related endpoints
    api.add_namespace(amenities_ns, path='/api/v1/amenities') # Amenity management
    api.add_namespace(places_ns, path='/api/v1/places')       # Place listings
    api.add_namespace(review_ns, path='/api/v1/reviews')      # Reviews and ratings
    api.add_namespace(auth_ns, path='/api/v1/auth')           # Login, register, etc.
    api.add_namespace(protected_ns, path='/api/v1/protected') # Example of protected routes

    # Return the fully configured Flask app instance
    return app
