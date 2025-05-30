# 🧩 Sequence Diagram - User Registration

This sequence diagram shows how a new user is register in the HBnB application.
It demonstrates the flow of data through the API, service, and database layers.

---

```mermaid
sequenceDiagram
    participant User
    participant API
    participant UserService
    participant Database

    User->>API: POST /users (email, password, name)
    API->>UserService: validate(email, password, name)
    UserService->>Database: Save new User to DB
    Database-->>UserService: Comfirm Save
    UserService-->>API: Return Response
	API-->>User: Return Success/Failure

```

### 👤 User Registration – Sequence Description

This diagram illustrates the process when a user registers on the HBnB platform.
The API receives the user's data and delegates the operation to the `UserService`,
which validates the input and creates a new `User` object. The `UserRepository`
then persists the data to the database. A success or error response is returned to the client.

# 🧩 Sequence Diagram – Place Creation

This sequence diagram shows how a new place is created in the HBnB application.
It demonstrates the flow of data through the API, service, and database layers.

---

```mermaid
sequenceDiagram
title Place Creation Flow

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

# 🏠 Place Creation - Sequence Description

User sends place information like title, location, and price. The API forwards the request to the PlaceService. PlaceService checks the data and builds a new Place object. The Database saves the new place entry. A confirmation is sent back up through the layers. The User receives a message indicating if the place creation succeeded or failed.

# 🧩 Sequence Diagram – Review Submission

This sequence diagram explains how a user submits a review for a place in the HBnB platform.
It highlights the interaction between the user, API, service logic, and data storage.

---

```mermaid
sequenceDiagram
title Review Submission Flow

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

# 📝 Review Creation - Sequence Description

User fills and submits a review form including comment and rating. The API captures the request and sends it to the ReviewService. ReviewService validates the input and builds a Review object. The Database stores the new review. A confirmation goes back up through the service and API. The User receives a success or error message.

# 🧩 Sequence Diagram – Fetching a List of Places

This sequence diagram shows how the HBnB system handles a request to fetch a filtered list of available places.
It outlines how the request travels through the API, is processed by the business logic, and retrieves data from the database.

---

```mermaid
sequenceDiagram
title Fetching Places Flow

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

# 📝 Fetching a List of Places - Sequence Description

User sends a request to retrieve places, possibly with filters (e.g., location, price, amenities). The API layer receives and forwards the request to the PlaceService. PlaceService applies the filters and queries the Database. The Database returns the list of places that match the criteria. The list is passed back through the Service and API layers. The User receives the final filtered list of places.
