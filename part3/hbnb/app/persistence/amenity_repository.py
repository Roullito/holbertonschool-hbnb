from hbnb.app.models.amenity import Amenity
from hbnb.app.persistence.repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)

    def get_amenity_by_name(self, name):
        return self.model.query.filter_by(name=name).first()
