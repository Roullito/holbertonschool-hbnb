"""
Defines the User model for the HBnB application.

A User represents an account with personal details and admin flag.
Inherits from BaseModel, providing id and timestamp fields.
"""

from hbnb.app.models.base_model import BaseModel


class User(BaseModel):
    """
    Represents a user in the HBnB application.

    Inherits:
        BaseModel: Provides id, created_at, and updated_at.

    Attributes:
        first_name (str): User's first name (max 50 chars).
        last_name (str): User's last name (max 50 chars).
        email (str): User's email address (must contain '@').
        is_admin (bool): Flag indicating admin privileges.
    """

    def __init__(self, first_name, last_name, email, is_admin=False):
        """
        Initialize a new User instance with validation.

        Args:
            first_name (str): First name (max 50 characters).
            last_name (str): Last name (max 50 characters).
            email (str): Email address (must contain '@').
            is_admin (bool, optional): Admin flag. Defaults to False.

        Raises:
            ValueError: If first_name or last_name exceed length limits.
            TypeError: If email does not contain an '@' symbol.
        """
        super().__init__()

        if len(first_name) > 50:
            raise ValueError(
                "Your first name must have less than 50 characters"
            )
        self.first_name = first_name

        if len(last_name) > 50:
            raise ValueError(
                "Your last name must have less than 50 characters"
            )
        self.last_name = last_name

        if '@' not in email:
            raise TypeError(
                "Enter a valid address, e.g. example@gmail.com"
            )
        self.email = email

        self.is_admin = is_admin

    def to_dict(self):
        """
        Serialize the user to a dictionary, excluding sensitive fields.

        Returns:
            dict: Mapping of User fields (id, first_name, last_name, email).
        """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email
        }
