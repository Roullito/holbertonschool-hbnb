"""
Defines the BaseModel class for HBnB, providing core attributes and methods.

BaseModel supplies a unique ID, creation and update timestamps, and
utility methods for saving, updating attributes, and serializing to dict.
"""

import uuid
from datetime import datetime

class BaseModel:
    """
    Core model class with common attributes and methods.

    Attributes:
        id (str): Unique identifier (UUID4).
        created_at (datetime): Timestamp of creation.
        updated_at (datetime): Timestamp of last update.
    """

    def __init__(self):
        """
        Initialize a new BaseModel instance.

        Sets id to a new UUID4 string and timestamps to current datetime.
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Mark the object as modified by updating its updated_at timestamp.

        Should be called whenever the object is changed.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Update object attributes from a data dictionary and save changes.

        Args:
            data (dict): Keys and values to set on this object.

        Only existing attributes are updated; others are ignored.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        """
        Serialize this object to a dictionary, converting nested models.

        Returns:
            dict: A mapping of attribute names to their JSON-serializable values.
        """
        result = {}
        for key, value in self.__dict__.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif hasattr(value, 'to_dict'):
                result[key] = value.to_dict()
            elif (isinstance(value, list)
                  and all(hasattr(item, 'to_dict') for item in value)):
                result[key] = [item.to_dict() for item in value]
            else:
                result[key] = value
        return result
