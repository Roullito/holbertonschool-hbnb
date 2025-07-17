#!/usr/bin/python3

"""
This module provides API endpoints for managing places in the HBnB app.

It includes creation, retrieval (list and by ID), and update of place records.
Each place is linked to a user (owner) and a list of amenities.
"""

from hbnb.app.models.base_model import BaseModel
from flask_restx import Namespace, Resource, fields
from hbnb.app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt


api = Namespace('places', description='Place operations')

# Define the models for related entities
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

# Define the place model for input validation and documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=False, description='ID of the owner (automatically set to current user)'),
    'amenities': fields.List(fields.String, required=True, description="List of amenities ID's")
})


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc(security='Bearer')
    @jwt_required()
    def post(self):
        """
        Create a new place.

        Returns:
            tuple: JSON response with new place or error, and HTTP status code.
        """
        current_user_id = get_jwt_identity()
        current_user = facade.get_user(current_user_id)

        if not current_user:
            return {"error": "Unauthorized"}, 403

        data = api.payload
        # Set the current user as owner
        data["owner_id"] = current_user_id

        try:
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """
        Get a list of all places.

        Returns:
            tuple: JSON response with list of places or error, and status code.
        """
        try:
            all_place = facade.get_all_places()
            return [place.to_dict() for place in all_place], 200
        except Exception:
            return {"error": "An unexpected error occurred"}, 500


@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """
        Retrieve a place by ID.
        Args:
            place_id (str): The ID of the place to retrieve.

        Returns:
            tuple: Place data with owner and amenities, or error, and status code.
        """
        try:
            place = facade.get_place(place_id)
            if not place:
                return {"error": "Place not found"}, 404
            result = place.to_dict()
            result["owner"] = place.owner.to_dict()
            result["amenities"] = [amenities.to_dict() for amenities in place.amenities]
            return result, 200
        except Exception as e:
            return {"error": str(e)}, 500

    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.doc(security='Bearer')
    @jwt_required()
    def put(self, place_id):
        """
        Update an existing place.
        Only the owner can update their place.

        Args:
            place_id (str): The ID of the place to update.

        Returns:
            tuple: Updated place data or error, and HTTP status code.
        """
        data = api.payload
        current_user_id = get_jwt_identity()

        if not current_user_id:
            return {"error": "Unauthorized"}, 403

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        if 'owner_id' in data and data['owner_id'] != place.owner_id:
            return {"error": "You cannot modify the owner of a place"}, 400

        # Check access: only owner can update
        if place.owner_id != current_user_id:
            return {"error": "You can only update your own places"}, 403

        update_place = facade.update_place(place_id, data)
        return update_place.to_dict(), 200
