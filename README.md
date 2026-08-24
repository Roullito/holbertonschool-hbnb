# HBnB — Airbnb-Style REST API

Team project (3 developers) building an Airbnb-style backend across four phases: UML technical design (`part1`), an in-memory Business Logic Layer and Flask-RESTx API (`part2`), a full REST API with JWT authentication and SQLAlchemy/database persistence (`part3`), and a simple web frontend consuming the API (`part4`). `part3` is the most complete and production-relevant version of the API.

## Overview

HBnB models the core of an Airbnb-style platform: users, place listings, amenities and reviews, exposed through a documented REST API with authentication and role-based authorization.

## Features

- User, Place, Amenity and Review resources with full CRUD operations
- Password hashing (bcrypt) — passwords are never stored in plaintext
- JWT-based authentication (Flask-JWT-Extended)
- Authorization checks: a user can only modify resources they own, unless they hold admin rights
- Facade pattern decoupling the API layer from business logic
- Repository pattern for persistence, migrated from in-memory storage to SQLAlchemy with a relational schema (`schema.sql`)
- Auto-generated Swagger/OpenAPI documentation (Flask-RESTx)

## Tech Stack

Python 3, Flask, Flask-RESTx, Flask-JWT-Extended, Flask-Bcrypt, SQLAlchemy, Flask-SQLAlchemy, SQL

## Architecture

Three-layer architecture, documented with UML diagrams in `part1`: a Presentation layer (API endpoints), a Business Logic layer (models and validation rules), and a Persistence layer (repository pattern, backed by SQLAlchemy from `part3` onward). A Facade layer sits between the API and business logic to keep the two decoupled.

## Security Considerations

- Passwords are hashed with bcrypt before storage, never kept in plaintext
- Authentication is handled via signed JWTs, with dedicated protected/admin-only endpoints (`app/api/v1/auth.py`, `app/api/v1/protected.py` in `part3`)
- Authorization is enforced per-resource: ownership checks (e.g. `owner_id` on places) gate updates and deletes unless the requester is an admin
- Data-integrity rules are enforced at the database schema level in addition to application-level validation, as a defense-in-depth measure

## Installation

From `part3`, the most complete version:

```
cd part3
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python run.py
```

Swagger UI is available at `http://localhost:5000/api/v1/`.

## Usage

Use the Swagger UI (or a client such as curl/Postman) to register a user, authenticate to obtain a JWT, then pass it as a Bearer token to create and manage places, amenities and reviews.

## What I Learned

Building the authentication and access-control logic myself — deciding where to enforce ownership checks, when to require admin rights, and how to combine framework-level validation with database constraints — is what makes it easier to recognize and test for the same bug classes (broken authentication, IDOR, privilege escalation) in applications I don't control.

## Authors

Jules Moleins, Alexis Cornillon, Benoît Maingon
