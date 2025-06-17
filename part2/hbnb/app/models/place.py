#!/usr/bin/python3

from hbnb.app.models.base_model import BaseModel
from models.user import User
from hbnb.app.models.review import Review
from hbnb.app.models.amenity import Amenity


class Place(BaseModel):
    def __init__(self, title, description, price:float, latitude:float, longitude:float, owner):
        super().__init__()
        if len(title) > 100:
            raise ValueError("Your title must be less than 100 characters")
        else:
            self.title = title

        if len(description) > 500:
            raise ValueError("Your description must be less than 500 characters")
        else:
            self.description = description

        if not isinstance(price,(float, int)):
            raise TypeError("Your price must be a number")
        elif price <= 0:
            raise ValueError("Your price must be than 0€")
        else:
            self.price = float(price)

        if not isinstance(latitude,(int, float)):
            raise TypeError("Your latitude must be number")
        elif not -90 <= latitude <= 90:
            raise ValueError("Your latitude must be between -90 and 90")
        else:
            self.latitude = float(latitude)

        if not isinstance(longitude,(float, int)):
            raise TypeError("Your longitude must be number")
        elif not -180 <= longitude <= 180:
            raise ValueError("Your longitude must be between -180 and 180")
        else:
            self.longitude = float(longitude)

        if not isinstance(owner, User):
            raise TypeError("Owner must be an instance of User")
        else:
            self.owner = owner

        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        """Add a review to the place."""
        if not isinstance(review, Review):
            raise TypeError("Review must be an instance of the Review class.")
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if not isinstance(amenity, Amenity):
            raise TypeError("Amenity must be an instance of the Amenity class.")
        if amenity not in self.amenities:
            self.amenities.append(amenity)
