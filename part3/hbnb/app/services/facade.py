"""
Implements the HBnBFacade class for managing core business logic.

The facade provides methods to create, retrieve, update, and delete users,
places, reviews, and amenities via in-memory repositories.
"""

from hbnb.app.persistence.repository import SQLAlchemyRepository
from hbnb.app.persistence.user_repository import UserRepository
from hbnb.app.persistence.place_repository import PlaceRepository
from hbnb.app.persistence.review_repository import ReviewRepository
from hbnb.app.persistence.amenity_repository import AmenityRepository
from hbnb.app.models.user import User
from hbnb.app.extensions import db
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review


class HBnBFacade:
    """
    Facade for HBnB business logic using in-memory repositories.

    Attributes:
        user_repo (SQLAlchemyRepository): Storage for User objects.
        place_repo (SQLAlchemyRepository): Storage for Place objects.
        review_repo (SQLAlchemyRepository): Storage for Review objects.
        amenity_repo (SQLAlchemyRepository): Storage for Amenity objects.
    """

    def __init__(self):
        """
        Initialize all repositories for each entity type.
        """
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.review_repo = ReviewRepository()
        self.amenity_repo = AmenityRepository()

    def create_user(self, user_data):
        """
        Create and store a new User.

        Args:
            user_data (dict): Attributes for User initialization.

        Returns:
            User: The newly created User object.
        """
        user = User(
            first_name=user_data['first_name'],
            last_name=user_data['last_name'],
            email=user_data['email'],
            is_admin=user_data.get('is_admin', False)
        )
        user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user


    def get_user(self, user_id):
        """
        Retrieve a User by ID.

        Args:
            user_id (str): ID of the user to retrieve.

        Returns:
            User or None: The User or None if not found.
        """
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """
        Retrieve a User by their email address.

        Args:
            email (str): Email to search for.

        Returns:
            User or None: The User matching the email or None.
        """
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """
        Retrieve all stored users.

        Returns:
            list: All User objects.
        """
        return self.user_repo.get_all()

    def update_user(self, user_id, new_data):
        """
        Update an existing User's attributes.

        Args:
            user_id (str): ID of the user to update.
            new_data (dict): Attributes to update.

        Returns:
            User or None: Updated User or None if not found.
        """
        user = self.user_repo.get(user_id)
        if not user:
            return None

        for key, value in new_data.items():
            if hasattr(user, key):
                if key == 'password':
                    # Hash the password before storing
                    user.hash_password(value)
                else:
                    setattr(user, key, value)

        db.session.commit()
        return user

    def create_amenity(self, amenity_data):
        """
        Create and store a new Amenity.

        Args:
            amenity_data (dict): Attributes for Amenity init.

        Returns:
            Amenity: The newly created Amenity.
        """
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """
        Retrieve an Amenity by ID.

        Args:
            amenity_id (str): ID of the amenity.

        Returns:
            Amenity or None: The Amenity or None if not found.
        """
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """
        Retrieve all stored amenities.

        Returns:
            list: All Amenity objects.
        """
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """
        Update an existing Amenity's attributes.

        Args:
            amenity_id (str): ID of the amenity to update.
            amenity_data (dict): Attributes to update.

        Returns:
            Amenity or None: Updated Amenity or None if not found.
        """
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        for key, value in amenity_data.items():
            if hasattr(amenity, key):
                setattr(amenity, key, value)
        db.session.commit()
        return amenity

    def create_place(self, place_data):
        """
        Create a new place.

        Args:
            place_data (dict): Dictionary with place details including owner_id.

        Returns:
            Place: The newly created Place.

        Raises:
            ValueError: If specified owner is not found.
        """
        owner_id = place_data.pop('owner_id')
        amenities_data = place_data.pop('amenities', [])

        owner = self.get_user(owner_id)
        if not owner:
            raise ValueError("Owner not found")

        place = Place(owner=owner, **place_data)

        if amenities_data:
            for amenity_name in amenities_data:
                amenity = self.amenity_repo.get_by_attribute('name', amenity_name)
                if not amenity:
                    amenity = Amenity(name=amenity_name)
                    self.amenity_repo.add(amenity)
                place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """
        Retrieve a Place by ID.

        Args:
            place_id (str): ID of the place to retrieve.

        Returns:
            Place or None: The Place or None if not found.
        """
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """
        Retrieve all stored places.

        Returns:
            list: All Place objects.
        """
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """
        Update an existing Place's attributes.

        Args:
            place_id (str): ID of the place to update.
            place_data (dict): Attributes to update.

        Returns:
            Place or None: Updated Place or None if not found.
        """
        place = self.place_repo.get(place_id)
        if not place:
            return None

        if 'amenities' in place_data:
            amenities_data = place_data.pop('amenities')

            place.amenities.clear()

            for amenity_identifier in amenities_data:
                amenity = self.amenity_repo.get(amenity_identifier)

                if not amenity:
                    amenity = self.amenity_repo.get_by_attribute('name', amenity_identifier)

                if not amenity:
                    amenity = Amenity(name=amenity_identifier)
                    self.amenity_repo.add(amenity)

                place.amenities.append(amenity)

        for key, value in place_data.items():
            if hasattr(place, key) and key != 'amenities':
                setattr(place, key, value)

        db.session.commit()
        return place

    def create_review(self, review_data):
        """
        Create and store a new Review linked to User and Place.

        Args:
            review_data (dict): Includes 'user' and 'place' IDs and content.

        Returns:
            Review: The newly created Review.

        Raises:
            ValueError: If specified user or place is not found.
        """
        user_id = review_data.pop('user_id')
        place_id = review_data.pop('place_id')
        user = self.get_user(user_id)
        if not user:
            raise ValueError("User not found")
        place = self.get_place(place_id)
        if not place:
            raise ValueError("Place not found")
        review = Review(user=user, place=place, **review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """
        Retrieve a Review by ID.

        Args:
            review_id (str): ID of the review to retrieve.

        Returns:
            Review or None: The Review or None if not found.
        """
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """
        Retrieve all stored reviews.

        Returns:
            list: All Review objects.
        """
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """
        Retrieve all reviews for a specific place.

        Args:
            place_id (str): ID of the place.

        Returns:
            list: Reviews linked to the given place.
        """
        all_review = self.review_repo.get_all()
        return [review for review in all_review
                if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        """
        Update an existing Review's attributes.

        Args:
            review_id (str): ID of the review to update.
            review_data (dict): Attributes to update.

        Returns:
            Review or None: Updated Review or None if not found.
        """
        review = self.review_repo.get(review_id)
        if not review:
            return None
        for key, value in review_data.items():
            if hasattr(review, key):
                setattr(review, key, value)
        db.session.commit()
        return review

    def delete_review(self, review_id):
        """
        Delete a Review by its ID.

        Args:
            review_id (str): ID of the review to delete.

        Returns:
            bool: True if deleted, False if not found.
        """
        if not self.review_repo.get(review_id):
            return False
        self.review_repo.delete(review_id)
        return True

    def get_review_by_user_and_place(self, user_id, place_id):
        """Get review by user and place to check for duplicates."""
        reviews = self.get_all_reviews()
        for review in reviews:
            if review.user_id == user_id and review.place_id == place_id:
                return review
        return None
