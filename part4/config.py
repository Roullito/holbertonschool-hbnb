import os
"""
Configuration module for the HBnB Flask application.

This module defines configuration classes used to manage different
environments for the application, such as development and production.
Each class sets specific settings like DEBUG mode or secret keys.

Classes:
    - Config: Base configuration class with default settings.
    - DevelopmentConfig: Configuration for development environment.

Dictionary:
    - config: A mapping of configuration names to their corresponding classes,
              used to easily select a config in the application factory.

Usage:
    from config import config
    app.config.from_object(config['development'])
"""

class Config:
    """Base configuration class with default settings."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    """Configuration for development environment."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    """Configuration for testing environment."""
    TESTING = True
    DEBUG = True

class ProductionConfig(Config):
    """Configuration for production environment."""
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
