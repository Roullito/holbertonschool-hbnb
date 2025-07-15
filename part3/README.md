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

### 📦 Entities and Responsibilities

Below is the ER diagram representing the core entities and their relationships in the HBnB system, created using Mermaid.js:

```mermaid

erDiagram
    USERS {
        uuid id PK
        string first_name
        string last_name
        string email UK
        string password
        boolean is_admin
        datetime created_at
        datetime updated_at
    }

    PLACES {
        uuid id PK
        string title
        string description
        decimal price
        float latitude
        float longitude
        uuid owner_id FK
        datetime created_at
        datetime updated_at
    }

    REVIEWS {
        uuid id PK
        string text
        int rating
        uuid user_id FK
        uuid place_id FK
        datetime created_at
        datetime updated_at
    }

    AMENITIES {
        uuid id PK
        string name UK
        datetime created_at
        datetime updated_at
    }

    PLACE_AMENITY {
        uuid place_id PK,FK
        uuid amenity_id PK,FK
        datetime created_at
        datetime updated_at
    }

    USERS ||--o{ PLACES : "owns"
    USERS ||--o{ REVIEWS : "writes"
    PLACES ||--o{ REVIEWS : "has"
    PLACES ||--o{ PLACE_AMENITY : ""
    AMENITIES ||--o{ PLACE_AMENITY : ""

```

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

## 🧑‍💻 Authors

* Jules Moleins
* Alexis Cornillon
* Benoît Maingon

## 📚 References

* [Flask Documentation](https://flask.palletsprojects.com/)
* [Flask-RESTx Docs](https://flask-restx.readthedocs.io/)
* [Python Project Structure Best Practices](https://docs.python-guide.org/writing/structure/)
* [Facade Design Pattern](https://refactoring.guru/design-patterns/facade/python/example)
