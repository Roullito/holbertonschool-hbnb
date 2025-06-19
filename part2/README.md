# 🏠 HBnB – Part 2: Business Logic & API

## 📆 Project Structure

This project follows a modular structure to ensure maintainability and scalability. The current setup implements the foundation for the Business Logic Layer (BLL), the API, and the in-memory persistence layer.

```
hbnb/
├── app/
│   ├── __init__.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py
│   │       ├── places.py
│   │       ├── reviews.py
│   │       └── amenities.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── place.py
│   │   ├── review.py
│   │   └── amenity.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── facade.py
│   └── persistence/
│       ├── __init__.py
│       └── repository.py
├── config.py
├── requirements.txt
├── run.py
└── README.md
```

## 🧠 Key Concepts Implemented

* ✅ Modular application structure
* ✅ Flask app factory pattern (`create_app`)
* ✅ flask-restx setup with Swagger UI (`/api/v1/`)
* ✅ In-memory repository following the Repository Pattern
* ✅ Facade layer to decouple API and logic
* ✅ Project ready for future integration with SQLAlchemy

## ⚙️ Getting Started

### 🔹 Install dependencies

We recommend using a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 🔹 Run the application

```bash
python run.py
```

Access the Swagger UI at:
[http://localhost:5000/api/v1/](http://localhost:5000/api/v1/)

## 🔧 Technologies Used

* Python 3.x
* Flask
* Flask-RESTx
* Repository Pattern
* Facade Pattern

## 🔮 Next Steps

* Add API endpoints for Users, Places, Reviews, Amenities
* Implement business logic classes in `models/`
* Replace in-memory repository with SQLAlchemy in Part 3
* Add authentication and RBAC

## 🧑‍💻 Authors

* Jules Moleins
* Alexis Cornillon
* Benoît Maingon

## 📚 References

* [Flask Documentation](https://flask.palletsprojects.com/)
* [Flask-RESTx Docs](https://flask-restx.readthedocs.io/)
* [Python Project Structure Best Practices](https://docs.python-guide.org/writing/structure/)
* [Facade Design Pattern](https://refactoring.guru/design-patterns/facade/python/example)
