"""
Defines the Place model for the HBnB application.

A Place represents a rental property and includes details such as title,
description, price, geographic coordinates, owner, reviews, and amenities.
"""

from hbnb.app.models.base_model import BaseModel
from hbnb.app.extensions import db

place_amenity = db.Table(
    'place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), nullable=False),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), nullable=False)
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
    __tablename__ = 'places'

    title = db.Column(db.String(126), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    owner = db.relationship('User', backref='user_places')
    amenities = db.relationship('Amenity', secondary=place_amenity, backref='amenity_places')


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

        from hbnb.app.models.user import User
        if not isinstance(owner, User):
            raise TypeError("Owner must be an instance of User")
        self.owner = owner

    def add_amenity(self, amenity):
        """Add an amenity to this place."""
        from hbnb.app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise TypeError("Amenity must be an instance of Amenity")
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def remove_amenity(self, amenity):
        """Remove an amenity from this place."""
        from hbnb.app.models.amenity import Amenity
        if not isinstance(amenity, Amenity):
            raise TypeError("Amenity must be an instance of Amenity")
        if amenity in self.amenities:
            self.amenities.remove(amenity)

    def to_dict(self):
        """
        Serialize the place to a dictionary.

        Returns:
            dict: Mapping of Place fields including owner and amenities.
        """
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
            "amenities": [amenity.to_dict() for amenity in self.amenities] if hasattr(self, 'amenities') else []
        }


