# HBnB – Technical Documentation (Part 1)

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

class PresentationLayer {
    <<Interface>>
    +API
    +UserService
}

class BusinessLogicLayer {
    +User
    +Place
    +Review
    +Amenity
}

class PersistenceLayer {
    +DataBaseAccess
}

PresentationLayer --> BusinessLogicLayer : uses (via Facade Services)
BusinessLogicLayer --> PersistenceLayer : accesses (via Repositories)
```

### ✅ Layer Descriptions

* **Presentation Layer**: Entry point for client/API interactions via services.
* **Business Logic Layer**: Core domain models with rules and logic.
* **Persistence Layer**: Handles data storage/retrieval via repositories.

### ✅ Facade Pattern

Used to centralize business logic inside services and prevent direct access to data layers from the API.

---

## 🧩 Business Logic Layer – Class Diagram

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
Place --> "*" Amenity : has
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
participant User
participant API
participant UserService
participant UserRepository

User ->> API: Submit registration data
API ->> UserService: Validate input and create User
UserService ->> UserRepository: Save new User to DB
UserRepository -->> UserService: Return save confirmation
UserService -->> API: Send success message
API -->> User: Respond with success or error
```

**Description**: User sends registration data → API → Service → Repository → Confirmation response.

---

### 2. Place Creation

```mermaid
sequenceDiagram
participant User
participant API
participant PlaceService
participant Database

User ->> API: Submit new place datas (e.g., title, location, price)
API ->> PlaceService: Validate and create Place
PlaceService ->> Database: Save new place to DB
Database -->> PlaceService: Confirm Save
PlaceService -->> API: Return Response
API -->> User: Return Success/Failure
```

**Description**: User submits place info → API → PlaceService → DB → response

---

### 3. Review Submission

```mermaid
sequenceDiagram
participant User
participant API
participant ReviewService
participant Database

User ->> API: Submit review (e.g., rating, comment, place_id)
API ->> ReviewService: Validate and create Review
ReviewService ->> Database: Save review to DB
Database -->> ReviewService: Confirm Save
ReviewService -->> API: Return Response
API -->> User: Return Success/Failure
```

**Description**: Review submission goes through API and is saved after validation.

---

### 4. Fetching a List of Places

```mermaid
sequenceDiagram
participant User
participant API
participant PlaceService
participant Database

User ->> API: Request list of places (with filters)
API ->> PlaceService: Apply filters and fetch places
PlaceService ->> Database: Query matching places
Database -->> PlaceService: Return place list
PlaceService -->> API: Return data
API -->> User: Send list of places
```

**Description**: User asks for places → filters applied → DB queried → results returned

---

## ✅ Final Notes

This document covers the full technical blueprint of the HBnB application's architecture. It includes:

* A layered structure using the facade pattern
* Clear responsibilities between models, services, and data access
* Visual sequence flows for major use cases

This file should be kept updated as development progresses in the next phases.
