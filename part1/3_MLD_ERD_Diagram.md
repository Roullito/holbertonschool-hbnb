# Diagramme MLD/ERD - HBnB

## Figure 8 : Diagramme MLD/ERD (Schéma Relationnel)

Ce diagramme représente le **Modèle Logique de Données (MLD)** / **Entity-Relationship Diagram (ERD)** du projet HBnB avec toutes les tables, clés primaires/étrangères, cardinalités et contraintes.

```mermaid
eerDiagram
    users ||--o{ places : "owns (1..N)"
    users ||--o{ reviews : "writes (1..N)"
    places ||--o{ reviews : "has (1..N)"
    places }o--o{ amenities : "has (N..N)"

    users {
        char(36) id PK "Primary Key"
        varchar(255) first_name "NOT NULL"
        varchar(255) last_name "NOT NULL"
        varchar(255) email UK "UNIQUE, NOT NULL"
        varchar(255) password "NOT NULL"
        boolean is_admin "DEFAULT FALSE"
        datetime created_at
        datetime updated_at
    }

    places {
        char(36) id PK "Primary Key"
        varchar(255) title "NOT NULL"
        text description
        decimal(10_2) price "NOT NULL, CHECK >= 0"
        float latitude "NOT NULL"
        float longitude "NOT NULL"
        char(36) owner_id FK "Foreign Key to users"
        datetime created_at
        datetime updated_at
    }

    reviews {
        char(36) id PK "Primary Key"
        text text "NOT NULL"
        int rating "CHECK 1-5"
        char(36) user_id FK "Foreign Key to users"
        char(36) place_id FK "Foreign Key to places"
        datetime created_at
        datetime updated_at
    }

    amenities {
        char(36) id PK "Primary Key"
        varchar(255) name UK "UNIQUE, NOT NULL"
        datetime created_at
        datetime updated_at
    }

    place_amenity {
        char(36) place_id FK "FK to places, part of PK"
        char(36) amenity_id FK "FK to amenities, part of PK"
        datetime created_at
        datetime updated_at
    }
```

---

## 📊 Détails du Schéma

### 🗂️ Tables (5)

1. **`users`** - Utilisateurs de la plateforme
2. **`places`** - Locations/propriétés
3. **`reviews`** - Avis sur les places
4. **`amenities`** - Équipements/commodités
5. **`place_amenity`** - Table de jointure (N..N)

---

### 🔑 Clés Primaires (PK)

| Table | Clé Primaire | Type |
|-------|-------------|------|
| `users` | `id` | CHAR(36) - UUID |
| `places` | `id` | CHAR(36) - UUID |
| `reviews` | `id` | CHAR(36) - UUID |
| `amenities` | `id` | CHAR(36) - UUID |
| `place_amenity` | `(place_id, amenity_id)` | Clé composite |

---

### 🔗 Clés Étrangères (FK)

| Table | Colonne FK | Référence | Cardinalité | Action |
|-------|-----------|-----------|-------------|--------|
| `places` | `owner_id` | `users(id)` | 1..N | CASCADE |
| `reviews` | `user_id` | `users(id)` | 1..N | CASCADE |
| `reviews` | `place_id` | `places(id)` | 1..N | CASCADE |
| `place_amenity` | `place_id` | `places(id)` | N..N | CASCADE |
| `place_amenity` | `amenity_id` | `amenities(id)` | N..N | CASCADE |

---

### 📐 Cardinalités

| Relation | Cardinalité | Description |
|----------|-------------|-------------|
| `users` → `places` | **1..N** | Un utilisateur possède 0 ou plusieurs places |
| `users` → `reviews` | **1..N** | Un utilisateur écrit 0 ou plusieurs avis |
| `places` → `reviews` | **1..N** | Une place reçoit 0 ou plusieurs avis |
| `places` ↔ `amenities` | **N..N** | Une place a 0 ou plusieurs amenities, une amenity est dans 0 ou plusieurs places |

---

### ⚙️ Contraintes d'Intégrité

#### Contraintes UNIQUE
| Table | Colonne | Description |
|-------|---------|-------------|
| `users` | `email` | Un email ne peut être utilisé qu'une fois |
| `amenities` | `name` | Un nom d'équipement doit être unique |
| `reviews` | `(user_id, place_id)` | Un utilisateur ne peut laisser qu'un avis par place |

#### Contraintes CHECK
| Table | Colonne | Contrainte | Description |
|-------|---------|-----------|-------------|
| `places` | `price` | `price >= 0` | Le prix doit être positif ou nul |
| `reviews` | `rating` | `rating BETWEEN 1 AND 5` | La note doit être entre 1 et 5 |

#### Contraintes NOT NULL
Toutes les colonnes sont `NOT NULL` sauf :
- `places.description` (optionnel)

---

## 🎯 Relations Détaillées

### 1️⃣ User → Place (1..N)
- Un **utilisateur** peut posséder **plusieurs places**
- Une **place** appartient à **un seul utilisateur** (propriétaire)
- FK : `places.owner_id` → `users.id`
- Suppression : CASCADE (si user supprimé → places supprimées)

### 2️⃣ User → Review (1..N)
- Un **utilisateur** peut écrire **plusieurs reviews**
- Une **review** est écrite par **un seul utilisateur**
- FK : `reviews.user_id` → `users.id`
- Suppression : CASCADE

### 3️⃣ Place → Review (1..N)
- Une **place** peut avoir **plusieurs reviews**
- Une **review** concerne **une seule place**
- FK : `reviews.place_id` → `places.id`
- Suppression : CASCADE
- Contrainte : Un user ne peut laisser qu'un avis par place

### 4️⃣ Place ↔ Amenity (N..N)
- Une **place** peut avoir **plusieurs amenities**
- Une **amenity** peut être dans **plusieurs places**
- Table de jointure : `place_amenity`
- FK1 : `place_amenity.place_id` → `places.id`
- FK2 : `place_amenity.amenity_id` → `amenities.id`
- Clé primaire composite : `(place_id, amenity_id)`
- Suppression : CASCADE des deux côtés

---

## 📋 Conformité REAC

✅ **Schéma conceptuel (MCD)** : 5 entités, 4 relations
✅ **Schéma physique (MLD)** : 5 tables avec PK/FK/UNIQUE/CHECK
✅ **Cardinalités** : 1..N et N..N correctement implémentées
✅ **Contraintes d'intégrité** : 5 FK + 3 UNIQUE + 2 CHECK
✅ **Normalisation** : 3ème forme normale (3NF)
✅ **Script SQL** : Voir [part3/schema.sql](../part3/schema.sql)

---

## 🔍 Voir Aussi

- [Package Diagram](0_Package_Diagram.md) - Architecture générale
- [Class Diagram](1_Class_Diagram.md) - Modèle objet
- [Sequence Diagrams](2_Sequence_Diagrams.md) - Flux d'interactions
- [Schema SQL](../part3/schema.sql) - Implémentation SQL complète
- [DOSSIER_CERTIFICATION_BDD_RNCP.md](../DOSSIER_CERTIFICATION_BDD_RNCP.md) - Document RNCP complet
