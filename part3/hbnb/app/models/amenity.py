"""
Defines the Amenity model for the HBnB application.

An Amenity represents a feature or service associated with a place,
such as WiFi, Air Conditioning, or Kitchen access.
Each Amenity has a name and inherits base attributes like id and
timestamps from BaseModel.
"""

from hbnb.app.models.base_model import BaseModel
from hbnb.app.extensions import db


class Amenity(BaseModel):
    """
    Represents an amenity available in a place.

    Inherits:
        BaseModel: Provides id, created_at, and updated_at fields.

    Attributes:
        name (str): The name of the amenity, e.g. "WiFi" or "Pool".
    """
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)

    def __init__(self, name):
        """
        Initialize a new Amenity instance.

        Args:
            name (str): Name of the amenity. Must be non-empty and
                        at most 50 characters.

        Raises:
            TypeError: If name is not a string.
            ValueError: If name is empty or exceeds 50 characters.
        """
        super().__init__()
        if not isinstance(name, str):
            raise TypeError("Amenity name must be a string.")
        elif not name.strip():
            raise ValueError("Amenity name cannot be empty.")
        elif len(name) > 50:
            raise ValueError(
                "Amenity name must be at most 50 characters long.")
        self.name = name

    def to_dict(self):
        """
        Serialize the amenity to a dictionary.

        Returns:
            dict: Mapping of Amenity fields (id, name, created_at, updated_at).
        """
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
