# PREUVE BDD RELATIONNELLE - CERTIFICATION RNCP
## Projet HBnB (HolbertonBnB) - Plateforme de location

---

## 📋 TABLE DES MATIÈRES
1. [Schéma Conceptuel (MCD)](#1-schéma-conceptuel-mcd)
2. [Schéma Physique (MLD)](#2-schéma-physique-mld)
3. [Script SQL Complet](#3-script-sql-complet)
4. [Détail des Tables et Contraintes](#4-détail-des-tables-et-contraintes)
5. [Jeux d'Essai et Tests](#5-jeux-dessai-et-tests)

---

## 1. SCHÉMA CONCEPTUEL (MCD)

### Entités et Relations

```
┌─────────────┐
│    USER     │
├─────────────┤
│ id (PK)     │
│ first_name  │
│ last_name   │
│ email       │
│ password    │
│ is_admin    │
│ created_at  │
│ updated_at  │
└──────┬──────┘
       │
       │ 1:N (possède)
       │
       ▼
┌─────────────┐           N:M          ┌──────────────┐
│    PLACE    │◄────────────────────────►│   AMENITY    │
├─────────────┤                         ├──────────────┤
│ id (PK)     │                         │ id (PK)      │
│ title       │                         │ name (UQ)    │
│ description │    (place_amenity)      │ created_at   │
│ price       │                         │ updated_at   │
│ latitude    │                         └──────────────┘
│ longitude   │
│ owner_id(FK)│
│ created_at  │
│ updated_at  │
└──────┬──────┘
       │
       │ 1:N (reçoit)
       │
       ▼
┌─────────────┐
│   REVIEW    │
├─────────────┤
│ id (PK)     │
│ text        │
│ rating      │
│ user_id(FK) │◄─── N:1 (écrit) ─── USER
│ place_id(FK)│
│ created_at  │
│ updated_at  │
└─────────────┘
    UNIQUE (user_id, place_id)
```

### Relations détaillées :
- **USER - PLACE** : Un utilisateur possède 0 ou plusieurs places (1:N)
- **USER - REVIEW** : Un utilisateur écrit 0 ou plusieurs reviews (1:N)
- **PLACE - REVIEW** : Une place reçoit 0 ou plusieurs reviews (1:N)
- **PLACE - AMENITY** : Relation N:M via table associative `place_amenity`
- **Contrainte métier** : Un utilisateur ne peut laisser qu'une seule review par place

---

## 2. SCHÉMA PHYSIQUE (MLD)

### Liste des Tables

| Table          | Type            | Description                                    |
|----------------|-----------------|------------------------------------------------|
| `users`        | Entité          | Utilisateurs de la plateforme                  |
| `places`       | Entité          | Logements/lieux disponibles à la location      |
| `reviews`      | Entité          | Avis laissés par les utilisateurs              |
| `amenities`    | Entité          | Équipements disponibles (WiFi, piscine, etc.)  |
| `place_amenity`| Association N:M | Lie les places à leurs équipements             |

---

## 3. SCRIPT SQL COMPLET

```sql
PRAGMA foreign_keys = ON;

-- =====================================================
-- TABLE: users
-- =====================================================
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLE: places
-- =====================================================
CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) PRIMARY KEY NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL CHECK(price >= 0),
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (owner_id) REFERENCES users(id) ON DELETE CASCADE
);

-- =====================================================
-- TABLE: reviews
-- =====================================================
CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) PRIMARY KEY NOT NULL,
    text TEXT NOT NULL,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id)  REFERENCES users(id)   ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id)  ON DELETE CASCADE,
    CONSTRAINT unique_review UNIQUE (user_id, place_id)
);

-- =====================================================
-- TABLE: amenities
-- =====================================================
CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) PRIMARY KEY NOT NULL,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- TABLE: place_amenity (Many-to-Many)
-- =====================================================
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id CHAR(36)   NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id)   REFERENCES places(id)   ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

-- =====================================================
-- DONNÉES DE TEST / SEED
-- =====================================================

-- Admin par défaut
INSERT OR IGNORE INTO users (
    id, email, first_name, last_name, password, is_admin
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2b$12$txryxzSae2ihpMFhwrpTBu2sF4P0WaDxJ9eY3bbArntgk5nExtn3q',
    TRUE
);

-- Équipements initiaux
INSERT OR IGNORE INTO amenities (id, name) VALUES
    ('26de0779-5dfb-4f77-916d-ed6728e88edd', 'WiFi'),
    ('3493beb7-a2aa-4dd2-95e2-be9b1cca3b06', 'Swimming Pool'),
    ('3b23dec0-54f2-4a9f-bfb0-49a215961d72', 'Air Conditioning');
```

---

## 4. DÉTAIL DES TABLES ET CONTRAINTES

### 📊 Table `users`

| Colonne      | Type         | Contraintes                | Description                          |
|--------------|--------------|----------------------------|--------------------------------------|
| id           | CHAR(36)     | **PK**, NOT NULL           | Identifiant UUID unique              |
| first_name   | VARCHAR(255) | NOT NULL                   | Prénom de l'utilisateur              |
| last_name    | VARCHAR(255) | NOT NULL                   | Nom de famille                       |
| email        | VARCHAR(255) | **UNIQUE**, NOT NULL       | Email (authentification)             |
| password     | VARCHAR(255) | NOT NULL                   | Mot de passe hashé (bcrypt)          |
| is_admin     | BOOLEAN      | DEFAULT FALSE              | Flag administrateur                  |
| created_at   | DATETIME     | DEFAULT CURRENT_TIMESTAMP  | Date de création                     |
| updated_at   | DATETIME     | DEFAULT CURRENT_TIMESTAMP  | Date de dernière modification        |

**Clés :**
- **PK** : `id`
- **UNIQUE** : `email`

---

### 🏠 Table `places`

| Colonne      | Type          | Contraintes                | Description                          |
|--------------|---------------|----------------------------|--------------------------------------|
| id           | CHAR(36)      | **PK**, NOT NULL           | Identifiant UUID unique              |
| title        | VARCHAR(255)  | NOT NULL                   | Titre du logement                    |
| description  | TEXT          | NULL                       | Description détaillée                |
| price        | DECIMAL(10,2) | NOT NULL, **CHECK** ≥ 0    | Prix par nuitée (positif)            |
| latitude     | FLOAT         | NOT NULL                   | Coordonnée GPS (latitude)            |
| longitude    | FLOAT         | NOT NULL                   | Coordonnée GPS (longitude)           |
| owner_id     | CHAR(36)      | **FK**, NOT NULL           | ID du propriétaire (→ users.id)      |
| created_at   | DATETIME      | DEFAULT CURRENT_TIMESTAMP  | Date de création                     |
| updated_at   | DATETIME      | DEFAULT CURRENT_TIMESTAMP  | Date de modification                 |

**Clés :**
- **PK** : `id`
- **FK** : `owner_id` → `users(id)` ON DELETE CASCADE

**Contraintes CHECK :**
- `price >= 0` : Le prix ne peut pas être négatif

---

### ⭐ Table `reviews`

| Colonne      | Type      | Contraintes                | Description                          |
|--------------|-----------|----------------------------|--------------------------------------|
| id           | CHAR(36)  | **PK**, NOT NULL           | Identifiant UUID unique              |
| text         | TEXT      | NOT NULL                   | Contenu de l'avis                    |
| rating       | INT       | **CHECK** (1-5)            | Note de 1 à 5 étoiles                |
| user_id      | CHAR(36)  | **FK**, NOT NULL           | ID auteur (→ users.id)               |
| place_id     | CHAR(36)  | **FK**, NOT NULL           | ID du logement (→ places.id)         |
| created_at   | DATETIME  | DEFAULT CURRENT_TIMESTAMP  | Date de création                     |
| updated_at   | DATETIME  | DEFAULT CURRENT_TIMESTAMP  | Date de modification                 |

**Clés :**
- **PK** : `id`
- **FK** : `user_id` → `users(id)` ON DELETE CASCADE
- **FK** : `place_id` → `places(id)` ON DELETE CASCADE
- **UNIQUE** : `(user_id, place_id)` — Un user = 1 review par place

**Contraintes CHECK :**
- `rating BETWEEN 1 AND 5` : Note obligatoirement entre 1 et 5

---

### 🔧 Table `amenities`

| Colonne      | Type         | Contraintes                | Description                          |
|--------------|--------------|----------------------------|--------------------------------------|
| id           | CHAR(36)     | **PK**, NOT NULL           | Identifiant UUID unique              |
| name         | VARCHAR(255) | **UNIQUE**, NOT NULL       | Nom de l'équipement                  |
| created_at   | DATETIME     | DEFAULT CURRENT_TIMESTAMP  | Date de création                     |
| updated_at   | DATETIME     | DEFAULT CURRENT_TIMESTAMP  | Date de modification                 |

**Clés :**
- **PK** : `id`
- **UNIQUE** : `name` (Pas de doublon d'équipement)

---

### 🔗 Table `place_amenity` (Association N:M)

| Colonne      | Type      | Contraintes                | Description                          |
|--------------|-----------|----------------------------|--------------------------------------|
| place_id     | CHAR(36)  | **PK**, **FK**, NOT NULL   | ID du logement (→ places.id)         |
| amenity_id   | CHAR(36)  | **PK**, **FK**, NOT NULL   | ID de l'équipement (→ amenities.id)  |
| created_at   | DATETIME  | DEFAULT CURRENT_TIMESTAMP  | Date d'association                   |
| updated_at   | DATETIME  | DEFAULT CURRENT_TIMESTAMP  | Date de modification                 |

**Clés :**
- **PK composée** : `(place_id, amenity_id)`
- **FK** : `place_id` → `places(id)` ON DELETE CASCADE
- **FK** : `amenity_id` → `amenities(id)` ON DELETE CASCADE

---

## 5. JEUX D'ESSAI ET TESTS

### 🎯 Stratégie de test BDD

Le projet HBnB implémente plusieurs niveaux de tests pour garantir l'intégrité de la base de données :

#### A) Tests d'intégrité référentielle

```python
# Exemple : Test de cascade DELETE
1. Créer un utilisateur (user_id)
2. Créer une place (place_id) avec owner_id = user_id
3. Supprimer l'utilisateur
4. ✅ Vérifier que la place a été automatiquement supprimée (CASCADE)
```

#### B) Tests de contraintes UNIQUE

```python
# Test : Un utilisateur ne peut faire qu'une review par place
1. User A crée review pour Place X (rating=5)
2. User A tente de créer une 2ème review pour Place X
3. ✅ Erreur : UNIQUE constraint (user_id, place_id)
```

#### C) Tests de contraintes CHECK

```python
# Test : Le prix doit être positif
1. Créer une place avec price = -50
2. ✅ Erreur : CHECK constraint (price >= 0)

# Test : Rating entre 1 et 5
1. Créer une review avec rating = 7
2. ✅ Erreur : CHECK constraint (rating BETWEEN 1 AND 5)
```

### 📊 Jeu de données de test inclus

Le script SQL inclut des données de seed pour valider le fonctionnement :

| Type          | Données                                       |
|---------------|-----------------------------------------------|
| **Admin**     | admin@hbnb.io (mot de passe hashé bcrypt)     |
| **Amenities** | WiFi, Swimming Pool, Air Conditioning         |

### 🔐 Tests d'authentification

Le projet inclut également des tests de flux d'authentification :
- Fichier : `tests/test_auth_flow.py`
- Validation : Login, tokens JWT, permissions admin

---

## 📐 CONFORMITÉ REAC RNCP

### ✅ Compétences démontrées

| Compétence REAC                                      | Preuve HBnB                                  |
|------------------------------------------------------|----------------------------------------------|
| Concevoir un schéma de données relationnel           | MCD complet avec 5 tables + relations        |
| Implémenter un schéma physique de BDD                | MLD avec PK/FK/UNIQUE/CHECK                  |
| Écrire des scripts SQL                               | schema.sql fonctionnel avec seed             |
| Définir des contraintes d'intégrité                  | CASCADE, CHECK, UNIQUE implémentés           |
| Créer des jeux d'essai et tests                      | Seed data + tests unitaires                  |
| Gérer les relations N:M                              | Table place_amenity                          |
| Respecter les normes de nommage                      | snake_case, noms explicites                  |

---

## 📂 FICHIERS SOURCE

- **Script SQL** : `/part3/schema.sql` et `/part4/schema.sql`
- **Tests** : `/part3/tests/test_auth_flow.py`
- **Repositories** : `/part3/hbnb/app/persistence/*.py`
- **Modèles** : `/part3/hbnb/app/models/*.py`

---

## 🔍 NOTES TECHNIQUES

### SGBD utilisé
- **SQLite** (avec support PostgreSQL/MySQL via SQLAlchemy)
- `PRAGMA foreign_keys = ON` : Active l'intégrité référentielle

### Format des ID
- **UUID v4** (36 caractères) : Garantit l'unicité globale

### Sécurité
- Mots de passe hashés avec **bcrypt** (coût=12)
- Intégrité référentielle stricte (CASCADE)
- Contraintes métier via CHECK

---

## 📸 VISUELS COMPLÉMENTAIRES (optionnel)

Pour générer un schéma MCD/MLD visuel, vous pouvez utiliser :
- **dbdiagram.io** : Coller le script SQL
- **MySQL Workbench** : Reverse engineering
- **Draw.io** : Dessiner manuellement le schéma

---

**Document préparé pour la certification RNCP**
**Projet HBnB - HolbertonBnB**
**Date : Février 2026**
