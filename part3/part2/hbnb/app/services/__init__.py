"""
Create a singleton HBnBFacade instance for accessing business logic.

This module imports the HBnBFacade class and initializes a single
facade object that can be used across the application to perform
user, place, review, and amenity operations.
"""

from hbnb.app.services.facade import HBnBFacade

# Single facade instance for the HBnB business logic layer
facade = HBnBFacade()
