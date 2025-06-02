<div align="center">

# 🏠 HBnB - UML Documentation

**Simplified AirBnB-like Application Design**
Team: Alexis Cornillon, Jules Moleins
Project by: Javier Valenzani

</div>

---

## 📚 Project Overview

This project is the **first phase** of the HBnB Evolution application. The goal is to produce a **complete UML-based technical documentation** that will serve as the foundation for the system’s development.

We are designing an **AirBnB-like system** with support for user management, place listings, amenities, and reviews.

---

## 🧱 Application Architecture

The HBnB system follows a **three-layer architecture**:

- **Presentation Layer**: Handles user interaction through APIs and services.
- **Business Logic Layer**: Contains core models and domain logic.
- **Persistence Layer**: Manages data storage and retrieval from the database.

All data is persisted in a database (to be specified in Part 3).

---

## 🧩 Entities & Business Rules

### 👤 User
- Attributes: `first_name`, `last_name`, `email`, `password`, `is_admin`
- Can: Register, update, delete
- Identified by unique ID and tracked with creation/update timestamps

### 🏠 Place
- Attributes: `title`, `description`, `price`, `latitude`, `longitude`
- Linked to a user (owner)
- Can: Create, update, delete, list
- Can be associated with multiple amenities

### 🧼 Amenity
- Attributes: `name`, `description`
- Can: Create, update, delete, list

### 📝 Review
- Attributes: `rating`, `comment`
- Linked to a specific user and place
- Can: Create, update, delete, list by place

All entities are timestamped and uniquely identified.

---

## 🗂️ Tasks

### 1. 📦 High-Level Package Diagram
- Diagram showing the 3-layer architecture
- Communication via **Facade Pattern**

### 2. 📐 Detailed Class Diagram (Business Logic Layer)
- Covers: `User`, `Place`, `Review`, `Amenity`
- Includes:
  - Attributes
  - Methods
  - Relationships (1:many, many:many, etc.)

### 3. 🔄 Sequence Diagrams for API Calls
- At least 4 use cases, such as:
  - User Registration
  - Place Creation
  - Review Submission
  - Fetching Place List

### 4. 📄 Documentation Compilation
- All diagrams + explanations gathered into a structured document
- UML notation must be consistent and complete

---

## 🧭 Constraints

- Use standard **UML notation**
- Ensure clarity and accuracy across all diagrams
- Business rules **must be reflected** in the class and sequence diagrams
- Diagrams must be detailed enough to guide implementation

---

## 🛠️ Resources & Tools

### UML Concepts
- [Intro to UML (Holberton)](https://intranet.hbtn.io/concepts/130)

### 📦 Package Diagrams
- [Package Diagram Overview](https://www.uml-diagrams.org/package-diagrams-overview.html)

### 📐 Class Diagrams
- [UML Class Diagram Tutorial](https://www.visual-paradigm.com/guide/uml-unified-modeling-language/uml-class-diagram-tutorial/)
- [Draw.io](https://app.diagrams.net)

### 🔁 Sequence Diagrams
- [UML Sequence Diagram Guide](https://www.uml-diagrams.org/sequence-diagrams.html)
- [Mermaid.js Docs](https://mermaid.js.org)

---

## ✅ Expected Outcome

By the end of this project, you will have:

- A **clear architectural vision**
- Detailed **class and sequence diagrams**
- Full **technical documentation**
- A blueprint ready for the next development phase

---

## 👥 Authors

- [Alexis Cornillon](https://github.com/Alexiscnl)
- [Jules Moleins](https://github.com/Roullito)

---

## 📝 License

This project is part of the Holberton School curriculum. All rights reserved.
