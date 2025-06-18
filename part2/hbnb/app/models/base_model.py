import uuid
from datetime import datetime

class BaseModel:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update the attributes of the object based on the provided dictionary"""
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()  # Update the updated_at timestamp

    def to_dict(self):
        result = {}

        for key, value in self.__dict__.items():
            # Si c'est un datetime, convertir en str ISO
            if isinstance(value, datetime):
                result[key] = value.isoformat()

            # Si c'est un objet avec to_dict, l’appeler (ex: User ou Amenity)
            elif hasattr(value, 'to_dict'):
                result[key] = value.to_dict()

            # Si c'est une liste d'objets (ex: amenities)
            elif isinstance(value, list) and all(hasattr(item, 'to_dict') for item in value):
                result[key] = [item.to_dict() for item in value]

            else:
                result[key] = value

        return result
