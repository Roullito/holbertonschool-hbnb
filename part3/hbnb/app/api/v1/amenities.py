from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from hbnb.app.services import facade
"""
This module defines RESTful API endpoints for managing amenities in  HBnB app.

It includes routes to create, retrieve, and update amenities, using Flask-RESTx
for request validation and response formatting. All business logic interactions
are delegated to the HBnBFacade.

Routes:
    POST   /api/v1/amenities/           -> Create a new amenity
    GET    /api/v1/amenities/           -> List all amenities
    GET    /api/v1/amenities/<id>       -> Retrieve amenity by ID
    PUT    /api/v1/amenities/<id>       -> Update an existing amenity

Raises:
    400 Bad Request: If input data is invalid
    404 Not Found: If amenity with the given ID does not exist
"""


api = Namespace('amenities', description='Amenity operations')

# Define the amenity model for input validation and documentation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})


@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """
        Register a new amenity
        """
        amenity_data = api.payload
        try:
            new_amenity = facade.create_amenity(amenity_data)
            return new_amenity.to_dict(), 201
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """
        Get a list of all amenities.

        Returns:
            tuple: List of amenities and HTTP status code.
        """
        amenities = facade.get_all_amenities()
        return [a.to_dict() for a in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """
        Get a specific amenity by ID.

        Args:
            amenity_id (str): The ID of the amenity.

        Returns:
            tuple: Amenity data or error message and HTTP status code.
        """
        get_amenity = facade.get_amenity(amenity_id)
        if not get_amenity:
            return {"error": "Amenity not found"}, 404
        return get_amenity.to_dict(), 200

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """
        Update an amenity
        """
        amenity_data = api.payload
        updated_amenity = facade.update_amenity(amenity_id, amenity_data)

        if not updated_amenity:
            return {"error": "Amenity not found"}, 404
        return updated_amenity.to_dict(), 200
