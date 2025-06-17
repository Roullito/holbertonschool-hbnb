from hbnb.app.persistence.repository import InMemoryRepository
from hbnb.app.models.user import User
class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, new_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        for key, value in new_data.items():
            if hasattr(user, key):
                setattr(user, key, value)
        return user
