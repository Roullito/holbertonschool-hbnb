"""
API endpoints for managing reviews in the HBnB application.

This module defines the endpoints for creating, retrieving, updating,
and deleting reviews, as well as retrieving reviews for a specific place.

Namespace:
    /api/v1/reviews

Models:
    Review: Defines the expected input and output structure for reviews.

Classes:
    - ReviewList: Handles POST and GET for all reviews.
    - ReviewResource: Handles GET, PUT, DELETE for a specific review.
    - PlaceReviewList: Handles GET for reviews related to a specific place.
"""

from flask_restx import Namespace, Resource, fields
from flask import request
from hbnb.app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.doc(security='Bearer')
    @jwt_required()
    def post(self):
        """Create a new review.

        Validates the rating and uses the facade to persist a new review.

        Returns:
            tuple: A dictionary of the new review and status code 201 if success.
                Error message and 400 or 500 on failure.
        """
        current_user_id = get_jwt_identity()
        try:
            review_data = api.payload
            place = facade.get_place(review_data["place_id"])
            if place.owner_id == current_user_id:
                return {"error": "You cannot review your own place."}, 400

            existing_review = facade.get_review_by_user_and_place(
                current_user_id, review_data["place_id"])
            if existing_review:
                return {"error": "You have already reviewed this place."}, 400
            review_data["user_id"] = current_user_id

            # Validate rating range
            if not (1 <= review_data['rating'] <= 5):
                return {'error': 'Rating must be between 1 and 5'}, 400

            # Create the review using facade
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id,
                'created_at': new_review.created_at.isoformat(),
                'updated_at': new_review.updated_at.isoformat()
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'error': 'Internal server error'}, 500

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        try:
            reviews = facade.get_all_reviews()
            return [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id,
                    'place_id': review.place_id,
                    'created_at': review.created_at.isoformat(),
                    'updated_at': review.updated_at.isoformat()
                }
                for review in reviews
            ], 200
        except Exception as e:
            return {'error': 'Internal server error'}, 500


@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Retrieve a review by its ID.

        Args:
            review_id (str): The ID of the review to retrieve.

        Returns:
            tuple: Review data and status code 200, or error and 404 if not found.
        """
        try:
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404

            return {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user_id,
                'place_id': review.place_id,
                'created_at': review.created_at.isoformat(),
                'updated_at': review.updated_at.isoformat()
            }, 200
        except Exception as e:
            return {'error': 'Internal server error'}, 500

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, review_id):
        """
        Update an existing review by its ID.
        Only the author can update their review.
        """
        current_user_id = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Only the author can update their review
        if review.user_id != current_user_id:
            return {"error": "You can only update your own reviews"}, 403

        try:
            review_data = api.payload

            # Validate rating range if provided
            if 'rating' in review_data and not (1 <= review_data['rating'] <= 5):
                return {'error': 'Rating must be between 1 and 5'}, 400

            updated_review = facade.update_review(review_id, review_data)
            if not updated_review:
                return {'error': 'Review not found'}, 404

            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user_id,
                'place_id': updated_review.place_id,
                'created_at': updated_review.created_at.isoformat(),
                'updated_at': updated_review.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
        except Exception as e:
            return {'error': 'Internal server error'}, 500

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """
        Delete a review by its ID.
        Only the author can delete their review.
        """
        current_user_id = get_jwt_identity()

        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404

        # Only the author can delete their review
        if review.user_id != current_user_id:
            return {"error": "You can only delete your own reviews"}, 403

        try:
            success = facade.delete_review(review_id)
            if not success:
                return {'error': 'Review not found'}, 404

            return {'message': 'Review deleted successfully'}, 200
        except Exception:
            return {'error': 'Internal server error'}, 500


@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve all reviews for a specific place.

        Args:
            place_id (str): The ID of the place.

        Returns:
            tuple: List of reviews and 200 if found,
                or error and 404 if place not found.
        """
        try:
            # First check if place exists
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, 404

            reviews = facade.get_reviews_by_place(place_id)
            return [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id,
                    'place_id': review.place_id,
                    'created_at': review.created_at.isoformat(),
                    'updated_at': review.updated_at.isoformat()
                }
                for review in reviews
            ], 200
        except Exception as e:
            return {'error': 'Internal server error'}, 500
