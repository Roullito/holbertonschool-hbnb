from hbnb.app.models.place import Place
from hbnb.app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def get_place_by_id(self, id):
        return self.model.query.filter_by(id=id).first()
