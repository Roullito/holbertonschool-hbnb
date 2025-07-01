from hbnb.app import create_app
from hbnb.app.extensions import db

app = create_app("config.DevelopmentConfig")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
