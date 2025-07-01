from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from hbnb.app.services import facade

api = Namespace('auth', description='Authentication operations')

# Model for input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/login')
class Login(Resource):
    @api.expect(login_model, validate=True)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload

        # Retrieve user
        user = facade.get_user_by_email(credentials['email'])

        # Verify password
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Create token: identity as string (user id), add claims (is_admin)
        additional_claims = {"is_admin": user.is_admin}
        access_token = create_access_token(identity=str(user.id), additional_claims=additional_claims)

        return {'access_token': access_token}, 200
