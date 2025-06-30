"""
API endpoints for managing users in the HBnB application.

This module defines routes to register, list, retrieve, and update users.
All business logic is handled by the HBnBFacade.
"""


from flask_restx import Namespace, Resource, fields
from hbnb.app.services import HBnBFacade

# Create an instance of the business logic facade
facade = HBnBFacade()

# Define the users namespace for the API
api = Namespace('users', description='User operations')

# Define the user input/output schema for Swagger and validation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user (min 8 chars)')
})


@api.route('/')
class UserList(Resource):
    """
    Operations on the collection of users.

    POST: Register a new user.
    GET:  Retrieve a list of all users.
    """
    # POST /api/v1/users/ : Create a new user
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new user.

        Returns:
            tuple: The new user's data and HTTP 201 on success,
                   or an error message and HTTP 400 on failure.
        """
        user_data = api.payload

        # Check if email is already registered
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        if 'password' not in user_data or not user_data['password']:
            return {'error': 'Password is required'}, 400

        # Create and return the new user
        try:
            new_user = facade.create_user(user_data)
        except (TypeError, ValueError) as e:
            return {"error": str(e)}, 400
        return new_user.to_dict(), 201

    # GET /api/v1/users/ : Return all users
    @api.marshal_list_with(user_model)
    @api.response(200, 'List of users')
    def get(self):
        """
        Retrieve all registered users.

        Returns:
            tuple: List of user data dictionaries and HTTP 200.
        """
        users = facade.get_all_users()
        return [u.to_dict() for u in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    """
    Operations on a single user item.

    GET: Retrieve user details by ID.
    PUT: Update an existing user by ID.
    """
    # GET /api/v1/users/<user_id> : Return a user by ID
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """
        Retrieve a user by ID.

        Args:
            user_id (str): Unique identifier of the user.

        Returns:
            tuple: User data dictionary and HTTP 200 on success,
                   or error message and HTTP 404 if not found.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict()

    # PUT /api/v1/users/<user_id> : Update a user by ID
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """
        Update an existing user by ID.

        Args:
            user_id (str): Unique identifier of the user.

        Returns:
            tuple: Updated user data dictionary and HTTP 200 on success,
                   or error message and HTTP 404 if not found.
        """
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Update user data and return the updated user
        updated_user = facade.update_user(user_id, api.payload)
        return updated_user.to_dict(), 200
