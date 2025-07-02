from hbnb.app.models.review import Review
from hbnb.app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)

    def get_review_by_id(self, id):
        return self.model.query.filter_by(id=id).first()
