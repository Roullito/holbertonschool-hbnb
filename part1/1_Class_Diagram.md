# Class Diagram – Business Logic Layer

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
Place --> Amenity : has >*

```

## Business Logic Layer – Entities Description

### 👤 User
Represents a person using the platform.
Can be a regular user or an admin.
Handles account information and owns places and reviews.

### 🏠 Place
Represents a property listed by a user.
Includes details like title, description, price, and location.
Linked to its owner and associated with amenities and reviews.

### 📝 Review
Represents feedback left by a user about a place.
Contains a rating and a comment.
Linked to both a user (author) and a place (target).

### 🪑 Amenity
Represents a feature available in a place (e.g., WiFi, pool).
Can be associated with multiple places.
Used to describe and filter place offerings.
