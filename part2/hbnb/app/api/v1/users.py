from flask_restx import Namespace, Resource, fields
from app.services import HBnBFacade

# Create an instance of the business logic facade
facade = HBnBFacade()

# Define the users namespace for the API
api = Namespace('users', description='User operations')

# Define the user input/output schema for Swagger and validation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user')
})

@api.route('/')
class UserList(Resource):
    # POST /api/v1/users/ : Create a new user
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Check if email is already registered
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        # Create and return the new user
        new_user = facade.create_user(user_data)
        return new_user.to_dict()

    # GET /api/v1/users/ : Return all users
    @api.marshal_list_with(user_model)
    @api.response(200, 'List of users')
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [u.to_dict() for u in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    # GET /api/v1/users/<user_id> : Return a user by ID
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict()

    # PUT /api/v1/users/<user_id> : Update a user by ID
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    def put(self, user_id):
        """Update user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        # Update user data and return the updated user
        updated_user = facade.update_user(user_id, api.payload)
        return updated_user.to_dict(), 200
