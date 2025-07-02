"""
Defines the Place model for the HBnB application.

A Place represents a rental property and includes details such as title,
description, price, geographic coordinates, owner, reviews, and amenities.
"""

from hbnb.app.models.base_model import BaseModel
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity
from hbnb.app.extensions import db

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(60), db.ForeignKey('place.id'), nullable=False),
    db.Column('amenity_id', db.String(60), db.ForeignKey('amenity.id'), nullable=False)
)
class Place(BaseModel):
    """
    Represents a rental place in the HBnB application.

    Inherits:
        BaseModel: Provides id, created_at, updated_at.

    Attributes:
        title (str): Title of the place (max 100 chars).
        description (str): Description (max 500 chars).
        price (float): Price per night in euros (> 0).
        latitude (float): Latitude between -90 and 90.
        longitude (float): Longitude between -180 and 180.
        owner (User): The User who owns this place.
        reviews (list): List of Review instances.
        amenities (list): List of Amenity instances.
    """
    __tablename__ = 'place'

    id = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    title = db.Column(db.String(126), nullable=False)
    description = db.Column(db.String(256), nullable=False, unique=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    amenities = db.relationship('Amenity', secondary=place_amenity, backref='places', viewonly=False)


    def __init__(
        self,
        title,
        description,
        price: float,
        latitude: float,
        longitude: float,
        owner
    ):
        """
        Initialize a new Place instance with validation.

        Args:
            title (str): Title of the place.
            description (str): Description of the place.
            price (float|int): Price per night in euros.
            latitude (float|int): Latitude coordinate.
            longitude (float|int): Longitude coordinate.
            owner (User): Instance of User as owner.

        Raises:
            ValueError: For invalid length or numeric ranges.
            TypeError: For incorrect types.
        """
        super().__init__()
        if len(title) > 100:
            raise ValueError("Your title must be less than 100 characters")
        self.title = title

        if len(description) > 500:
            raise ValueError("Your description must be less than 500 characters")
        self.description = description

        if not isinstance(price, (float, int)):
            raise TypeError("Your price must be a number")
        if price <= 0:
            raise ValueError("Your price must be than 0€")
        self.price = float(price)

        if not isinstance(latitude, (int, float)):
            raise TypeError("Your latitude must be number")
        if not -90 <= latitude <= 90:
            raise ValueError("Your latitude must be between -90 and 90")
        self.latitude = float(latitude)

        if not isinstance(longitude, (float, int)):
            raise TypeError("Your longitude must be number")
        if not -180 <= longitude <= 180:
            raise ValueError("Your longitude must be between -180 and 180")
        self.longitude = float(longitude)

        if not isinstance(owner, User):
            raise TypeError("Owner must be an instance of User")
        self.owner = owner


