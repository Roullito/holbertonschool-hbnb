"""
Defines the User model for the HBnB application.

A User represents an account with personal details and admin flag.
Inherits from BaseModel, providing id and timestamp fields.
"""

from hbnb.app.models.base_model import BaseModel
from hbnb.app.extensions import db


class User(BaseModel):
    """
    Represents a user in the HBnB application.

    Inherits:
        BaseModel: Provides id, created_at, and updated_at.

    Attributes:
        first_name (str): User's first name (max 50 chars).
        last_name (str): User's last name (max 50 chars).
        email (str): User's email address (must contain '@').
        password (str): Hashed password.
        is_admin (bool): Flag indicating admin privileges.
    """

    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)

    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        """
        Initialize a new User instance with validation.

        Args:
            first_name (str): First name (max 50 characters).
            last_name (str): Last name (max 50 characters).
            email (str): Email address (must contain '@').
            password (str, optional): Raw password to be hashed.
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

        if password:
            self.hash_password(password)

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
            "email": self.email,
            "is_admin": self.is_admin
        }

    def hash_password(self, password):
        """Hashes the password before storing it."""
        from hbnb.app import bcrypt
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        from hbnb.app import bcrypt
        return bcrypt.check_password_hash(self.password.encode('utf-8'), password)
