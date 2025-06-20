# HBnB – Technical Documentation

This document serves as the foundation for the development of the HBnB Evolution project. It compiles all technical diagrams and design decisions made during the first part of the project, helping developers and collaborators understand the overall architecture, business logic, and flow of interactions within the system.

---

## 📘 Introduction

**HBnB Evolution** is a simplified AirBnB-like application. It allows users to:

* Register and manage user profiles
* Create and list properties (places)
* Submit reviews for visited places
* Associate places with amenities (features)

This document presents the full architectural overview, including:

* The layered system design using the facade pattern
* Business entities and their relationships
* The interaction flow for core API operations

---

## 🧱 High-Level Architecture – Package Diagram

```mermaid
classDiagram
class User {
  +UUID id
  +str first_name
  +str last_name
  +str email
  +str password
  +bool is_admin
  +datetime created_at
  +datetime updated_at
  +register()
  +update_profile()
  +delete()
}
class Place {
  +UUID id
  +str title
  +str description
  +float price
  +float latitude
  +float longitude
  +str owner
  +datetime created_at
  +datetime updated_at
  +create()
  +update()
  +delete()
}
class Review {
  +UUID id
  +int rating
  +str comment
  +str place
  +str user
  +datetime created_at
  +datetime updated_at
  +submit()
  +update()
  +delete()
}
class Amenity {
  +UUID id
  +str name
  +str description
  +datetime created_at
  +datetime updated_at
  +create()
  +update()
  +delete()
}
User --> Place : owns
User --> Review : writes
Place --> Review : receives
Place --> Amenity : has >*

```

### ✅ Entity Descriptions

* **User**: A person using the platform. Can register, update profile, and own places.
* **Place**: A property listed by a user. Linked to reviews and amenities.
* **Review**: Feedback from a user for a place, with rating and comment.
* **Amenity**: Features linked to places (WiFi, pool, etc.)

---

## 🔁 Sequence Diagrams – API Interaction Flow

### 1. User Registration

```mermaid
sequenceDiagram
    autonumber
    participant Client as User (Frontend)
    participant API as API (Presentation Layer)
    participant Logic as Business Logic Layer
    participant DB as Persistence Layer (Database)

    Note over Client: The user fills out the registration form
    Client->>API: POST /api/users {first_name, last_name, email, password}

    Note over API: Validate input data (presence, format, email uniqueness)
    API->>Logic: register_user(data: dict)

    Note over Logic: Hash password, generate UUID, timestamps
    Logic->>DB: INSERT INTO users (uuid, first_name, last_name, email, hashed_password, is_admin, created_at, updated_at)

    DB-->>Logic: Return new user ID and confirmation
    Logic-->>API: Return user object (without password)
    API-->>Client: 201 Created + JSON {id, first_name, last_name, email, is_admin, created_at}
```

**Description**: User sends registration data → API → Service → Repository → Confirmation response.

---

### 2. Place Creation

```mermaid
sequenceDiagram
    autonumber
    participant Client as User (Frontend)
    participant API as API (Presentation Layer)
    participant Logic as Business Logic Layer
    participant DB as Persistence Layer (Database)

    Note over Client: User submits a new place listing form
    Client->>API: POST /api/places {title, description, price, lat, long}

    Note right of API: Validates input data (types, required fields)
    API->>Logic: create_place(data)

    Note right of Logic: Validate data, associate current user as owner<br>Generate UUID, set created_at/updated_at<br>Sanitize fields if necessary
    Logic->>DB: INSERT INTO places (id, user_id, title, description, price, latitude, longitude, created_at, updated_at)

    Note right of DB: Save the new place entry<br>Return newly created place ID
    DB-->>Logic: Return place_id
    Logic-->>API: Return created place object (JSON, no internal fields)
    API-->>Client: 201 Created + JSON {id, title, description, price, lat, long}

    Note right of Client: Displays success message and new place

```

**Description**: User submits place info → API → PlaceService → DB → response

---

### 3. Review Submission

```mermaid
sequenceDiagram
    autonumber
    participant Client as User (Frontend)
    participant API as API (Presentation Layer)
    participant Logic as Business Logic Layer
    participant DB as Persistence Layer (Database)

    Client->>API: POST /api/reviews {place_id, rating, comment}
    Note right of Client: Authenticated user

    API->>Logic: create_review(data: dict, user_id: str)
    Note right of API: Extract user ID from auth token

    Logic->>DB: INSERT INTO reviews (user_id, place_id, rating, comment, created_at, updated_at)
    Note right of Logic: Business logic validates data and creates review

    DB-->>Logic: Return review ID and confirmation
    Logic-->>API: Return review object as dict
    API-->>Client: 201 Created + JSON {id, user_id, place_id, rating, comment, created_at, updated_at}

```

**Description**: Review submission goes through API and is saved after validation.

---

### 4. Fetching a List of Places

```mermaid
sequenceDiagram
    autonumber
    participant Client as User (Frontend)
    participant API as API (Presentation Layer)
    participant Logic as Business Logic Layer
    participant DB as Persistence Layer (Database)
    Client->>API: GET /api/places?min_price=50&max_price=200&lat=45.5&long=3.2
    API->>Logic: fetch_places(filters: dict)
    Logic->>DB: SELECT * FROM places WHERE price BETWEEN 50 AND 200 AND location NEAR (lat, long)
    DB-->>Logic: Return matching places
    loop For each place
        Logic->>DB: SELECT * FROM reviews WHERE place_id = place.id
        Logic->>DB: SELECT * FROM amenities WHERE place_id = place.id
    end
    Logic-->>API: Return list of place objects with reviews and amenities
    API-->>Client: 200 OK + JSON [\n  {id, title, price, lat, long, reviews[], amenities[]},\n  {...}\n]

```

**Description**: User asks for places → filters applied → DB queried → results returned

---

## ✅ Final Notes

This document covers the full technical blueprint of the HBnB application's architecture. It includes:

* A layered structure using the facade pattern
* Clear responsibilities between models, services, and data access
* Visual sequence flows for major use cases

This file should be kept updated as development progresses in the next phases.
