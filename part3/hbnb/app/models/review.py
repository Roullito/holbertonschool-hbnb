"""
Defines the Review model for the HBnB application.

A Review captures user feedback on a Place, including text, rating,
and links to the Place and User instances.
"""

from hbnb.app.models.base_model import BaseModel
from sqlalchemy.orm import validates
from hbnb.app.extensions import db


class Review(BaseModel):
    """
    Represents a user review on a place.

    Inherits:
        BaseModel: Provides id, created_at, and updated_at.

    Attributes:
        text (str): The content of the review comment.
        rating (int): An integer rating between 1 and 5.
        place (Place): The Place instance being reviewed.
        user (User): The User instance who wrote the review.
    """
    __tablename__ = 'reviews'

    text = db.Column(db.String(256), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    user = db.relationship('User', backref='user_reviews')
    place = db.relationship('Place', backref='place_reviews')

    @validates('rating')
    def validate_rating(self, key, value):
        if not 1 <= value <= 5:
            raise ValueError("Rating must be between 1 and 5")
        return value

    def __init__(self, text, rating, place, user):
        """
        Initialize a new Review instance with validation.

        Args:
            text (str): Review comment; must be non-empty.
            rating (int): Rating value (1–5).
            place (Place): Instance of Place being reviewed.
            user (User): Instance of User who writes the review.

        Raises:
            TypeError: If types of text, rating, place, or user are invalid.
            ValueError: If text is empty or rating not in 1–5 range.
        """
        super().__init__()

        if not isinstance(text, str):
            raise TypeError("Review comment must be a string.")
        if not text.strip():
            raise ValueError("Review comment must be non-empty.")
        self.text = text

        if not isinstance(rating, int):
            raise TypeError("Rating must be an integer.")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5.")
        self.rating = rating

        from hbnb.app.models.place import Place
        if not isinstance(place, Place):
            raise TypeError("Place must be a Place instance.")
        self.place = place

        from hbnb.app.models.user import User
        if not isinstance(user, User):
            raise TypeError("User must be a User instance.")
        self.user = user

    def to_dict(self):
        """
        Serialize the review to a dictionary.

        Returns:
            dict: Mapping of Review fields.
        """
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user_id": self.user_id,
            "place_id": self.place_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
