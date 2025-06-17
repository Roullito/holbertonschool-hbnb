from hbnb.app.models.base_model import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        if not isinstance(name, str):
            raise TypeError("Amenity name must be a string.")
        elif not name.strip():
            raise ValueError("Amenity name cannot be empty.")
        elif len(name) > 50:
            raise ValueError("Amenity name must be at most 50 characters long.")
        self.name = name
