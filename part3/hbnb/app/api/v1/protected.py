from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('protected', description='Protected operations')

@api.route('/')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
        """A protected endpoint that requires JWT token"""
        current_user_id = get_jwt_identity()
        claims = get_jwt()

        return {
            "message": f"Hello, user {current_user_id}",
            "is_admin": claims["is_admin"]
        }, 200
