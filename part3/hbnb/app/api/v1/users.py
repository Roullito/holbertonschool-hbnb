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

user_input_model = api.model('UserInput', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user (min 8 chars)'),
    'is_admin': fields.Boolean(required=False, description='Admin status (admin auth required if true)')
})

user_output_model = api.model('User', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the user'),
    'last_name': fields.String(description='Last name of the user'),
    'email': fields.String(description='Email of the user'),
    'is_admin': fields.Boolean(description='Admin status')
})


@api.route('/')
class UserList(Resource):
    """
    Operations on the collection of users.

    POST: Register a new user.
    GET:  Retrieve a list of all users.
    """
    # POST /api/v1/users/ : Create a new user
    @api.expect(user_input_model, validate=True)
    @api.marshal_with(user_output_model, code=201)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin access required to create admin users')
    @api.doc(security='Bearer')
    @jwt_required(optional=True)
    def post(self):
        """
        Register a new user.
        - Anyone can create a regular user (no auth required)
        - Only admins can create admin users (auth required if is_admin=true)

        Returns:
            tuple: The new user's data and HTTP 201 on success,
                   or an error message and HTTP 400/403 on failure.
        """
        user_data = api.payload

        # Check if trying to create an admin user
        if user_data.get('is_admin', False):
            # Auth required for admin creation
            claims = get_jwt()
            if not claims or not claims.get('is_admin', False):
                return {'error': 'Admin privileges required to create admin users'}, 403

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
    @api.marshal_list_with(user_output_model)
    @api.response(200, 'List of users')
    @api.response(403, 'Admin access required')
    @api.doc(security='Bearer')
    @jwt_required()
    def get(self):
        """
        Retrieve all registered users (Admin only).

        Returns:
            tuple: List of user data dictionaries and HTTP 200.
        """
        # Check if current user is admin
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403

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
    @api.marshal_with(user_output_model)
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
    @api.expect(user_input_model, validate=True)
    @api.marshal_with(user_output_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Unauthorized action')
    @api.doc(security='Bearer')
    @jwt_required()
    def put(self, user_id):
        """
        Update user information.
        - Users can update their own profile (except is_admin field)
        - Admins can update any user including is_admin field
        """
        current_user_id = get_jwt_identity()
        claims = get_jwt()
        is_admin = claims.get('is_admin', False)

        # Check if user exists
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Authorization check: user can edit themselves, admin can edit anyone
        if not is_admin and user_id != current_user_id:
            return {"error": "You can only modify your own profile"}, 403

        user_data = api.payload

        # Only admins can modify is_admin field
        if not is_admin and 'is_admin' in user_data:
            return {"error": "Only admins can modify admin status"}, 403

        # If changing email, check for uniqueness
        if 'email' in user_data:
            existing_user = facade.get_user_by_email(user_data['email'])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        # Update user data and return the updated user
        updated_user = facade.update_user(user_id, user_data)
        return updated_user.to_dict(), 200
