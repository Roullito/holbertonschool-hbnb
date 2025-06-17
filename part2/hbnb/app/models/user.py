#!/usr/bin/python3

from hbnb.app.models.base_model import BaseModel

class User(BaseModel):

    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()

        if len(first_name) > 50:
            raise ValueError("Your first name must have less than 50 character")
        else:
            self.first_name = first_name

        if len(last_name) > 50:
            raise ValueError("Your last name must have less than 50 character")
        else:
            self.last_name = last_name

        if not '@' in email:
            raise TypeError("enter a valid adress ex: exemple@gmail.com")
        else:
            self.email = email

        self.is_admin = is_admin

    def to_dict(self):
        return {
        "id": self.id,
        "first_name": self.first_name,
        "last_name": self.last_name,
        "email": self.email }
