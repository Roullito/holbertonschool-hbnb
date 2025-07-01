"""
Defines the repository interface and an in-memory implementation for HBnB.

The Repository ABC declares CRUD and lookup methods. InMemoryRepository
implements these using a simple dict for storage.
"""
from hbnb.app.extensions import db
from abc import ABC, abstractmethod
from hbnb.app.models.user import User
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review
from hbnb.app.models.amenity import Amenity

__all__ = ["User", "Place", "Review", "Amenity"]



class Repository(ABC):
    """
    Abstract base for a repository, defining required data operations.
    """

    @abstractmethod
    def add(self, obj):
        """
        Add an object to the repository.

        Args:
            obj: The object to add.
        """
        pass

    @abstractmethod
    def get(self, obj_id):
        """
        Retrieve an object by its ID.

        Args:
            obj_id (str): The unique identifier of the object.

        Returns:
            The object or None if not found.
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Retrieve all objects in the repository.

        Returns:
            List of all stored objects.
        """
        pass

    @abstractmethod
    def update(self, obj_id, data):
        """
        Update an existing object with new data.

        Args:
            obj_id (str): The ID of the object to update.
            data (dict): Attributes to update.
        """
        pass

    @abstractmethod
    def delete(self, obj_id):
        """
        Remove an object from the repository.

        Args:
            obj_id (str): The ID of the object to delete.
        """
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by a specific attribute value.

        Args:
            attr_name (str): Property name to filter on.
            attr_value: Value that the property must match.

        Returns:
            The first matching object or None.
        """
        pass


class InMemoryRepository(Repository):
    """
    In-memory repository implementation using a dict for storage.
    """

    def __init__(self):
        """
        Initialize the in-memory storage dict.
        """
        self._storage = {}

    def add(self, obj):
        """
        Store an object, keyed by its id.

        Args:
            obj: The object to store; must have `id` attribute.
        """
        self._storage[obj.id] = obj

    def get(self, obj_id):
        """
        Retrieve an object by its ID.

        Args:
            obj_id (str): The key of the object.

        Returns:
            The stored object or None.
        """
        return self._storage.get(obj_id)

    def get_all(self):
        """
        Retrieve all stored objects.

        Returns:
            List of all objects in storage.
        """
        return list(self._storage.values())

    def update(self, obj_id, data):
        """
        Update an object if it exists.

        Args:
            obj_id (str): ID of the object to update.
            data (dict): New attribute values.

        Note:
            Calls the object's own update method for attribute logic.
        """
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        """
        Delete an object by its ID.

        Args:
            obj_id (str): ID of the object to remove.
        """
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        """
        Find first object matching a given attribute value.

        Args:
            attr_name (str): Name of the attribute.
            attr_value: Desired value of the attribute.

        Returns:
            The first matching object or None.
        """
        return next(
            (obj for obj in self._storage.values()
             if getattr(obj, attr_name) == attr_value),
            None
        )
class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        db.session.add(obj)
        db.session.commit()

    def get(self, obj_id):
        return self.model.query.get(obj_id)

    def get_all(self):
        return self.model.query.all()

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()

    def delete(self, obj_id):
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()

    def get_by_attribute(self, attr_name, attr_value):
        return self.model.query.filter(getattr(self.model, attr_name) == attr_value).first()
