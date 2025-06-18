from flask import Flask
from flask_restx import Api
from hbnb.app.api.v1.users import api as users_ns
from hbnb.app.api.v1.amenities import api as amenities_ns
from hbnb.app.api.v1.places import api as places_ns

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API')

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')

    return app
