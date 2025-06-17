from hbnb.app.models.base_model import BaseModel
from hbnb.app.models.place import Place
from hbnb.app.models.user import User


class Review(BaseModel):
    def __init__(self, comment, rating, place, user):
        super().__init__()
        if not isinstance(comment, str):
            raise TypeError("Review comment must be a string.")
        self.comment = comment

        if not isinstance(rating, int):
            raise TypeError("Your rating must be an integer")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be an integer between 1 and 5.")
        self.rating = rating

        if not isinstance(place, Place):
            raise TypeError("Place must be an instance of the Place class.")
        self.place = place

        if not isinstance(user, User):
            raise TypeError("User must be an instance of the User class.")
        self.user = user
