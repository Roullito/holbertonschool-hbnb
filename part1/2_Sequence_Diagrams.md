# 🧩 Sequence Diagram - User Registration

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
