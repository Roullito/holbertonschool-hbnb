"""
API endpoints for managing users in the HBnB application.

This module defines routes to register, list, retrieve, and update users.
All business logic is handled by the HBnBFacade.
"""


from flask_restx import Namespace, Resource, fields
from hbnb.app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

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
    @api.response(403, 'Admin access required')
    @api.doc(security='Bearer')
    @jwt_required()
    def post(self):
        """
        Register a new user.
        Only admins can create users through this endpoint.

        Returns:
            tuple: The new user's data and HTTP 201 on success,
                   or an error message and HTTP 400/403 on failure.
        """
        # Check if current user is admin
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

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
    @api.response(403, 'Unauthorized action')
    @api.doc(security='Bearer')
    @jwt_required()
    def put(self, user_id):
        """
        Update user information.
        Admins can update any user including email/password.
        Regular users can only update their own profile (excluding email/password).
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        # Check if user exists
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Authorization check
        if not is_admin and user_id != current_user_id:
            return {"error": "Unauthorized action"}, 403

        user_data = api.payload

        # Admin can modify email and password, regular users cannot
        if not is_admin and ('email' in user_data or 'password' in user_data):
            return {"error": "You cannot modify email or password."}, 400

        # If admin is changing email, check for uniqueness
        if is_admin and 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        # Update user data and return the updated user
        updated_user = facade.update_user(user_id, user_data)
        return updated_user.to_dict(), 200
