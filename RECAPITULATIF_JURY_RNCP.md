# 📋 DOSSIER CERTIFICATION RNCP - PREUVE BDD RELATIONNELLE
## Candidat : [Votre Nom]
## Projet : HBnB (HolbertonBnB) - Plateforme de location type Airbnb

---

## 🎯 RÉSUMÉ EXÉCUTIF

**Compétence visée :** Concevoir et implémenter une base de données relationnelle

**Projet présenté :** HBnB - Application web de location de logements avec système d'avis et d'équipements

**Technologies :**
- SGBD : SQLite (compatible PostgreSQL/MySQL via SQLAlchemy)
- Backend : Python + Flask
- ORM : Custom repositories + SQLAlchemy
- Tests : Pytest

---

## 📦 CONTENU DU DOSSIER

### 1️⃣ Schéma Conceptuel de Données (MCD)
**Fichier :** `PREUVE_BDD_RNCP.md` - Section 1

**Entités principales :**
- **USERS** (utilisateurs)
- **PLACES** (logements)
- **REVIEWS** (avis)
- **AMENITIES** (équipements)
- **PLACE_AMENITY** (table d'association N:M)

**Relations :**
- User → Places (1:N) : Un utilisateur possède plusieurs logements
- User → Reviews (1:N) : Un utilisateur écrit plusieurs avis
- Place → Reviews (1:N) : Un logement reçoit plusieurs avis
- Place ↔ Amenities (N:M) : Un logement possède plusieurs équipements

**Contrainte métier :** Un utilisateur ne peut laisser qu'un seul avis par logement

---

### 2️⃣ Schéma Physique de Données (MLD)

**5 tables implémentées :**

| Table | PK | FK | UNIQUE | CHECK |
|-------|----|----|--------|-------|
| `users` | id | - | email | - |
| `places` | id | owner_id → users.id | - | price ≥ 0 |
| `reviews` | id | user_id → users.id<br>place_id → places.id | (user_id, place_id) | rating ∈ [1,5] |
| `amenities` | id | - | name | - |
| `place_amenity` | (place_id, amenity_id) | place_id → places.id<br>amenity_id → amenities.id | - | - |

**Détails dans :** `PREUVE_BDD_RNCP.md` - Section 4

---

### 3️⃣ Script SQL Complet

**Fichier source :** `part3/schema.sql` ou `part4/schema.sql`

**Contenu :**
```sql
✅ 5 tables CREATE TABLE avec contraintes complètes
✅ PRIMARY KEYS (UUID v4)
✅ FOREIGN KEYS avec ON DELETE CASCADE
✅ UNIQUE constraints (email, amenity name, review uniqueness)
✅ CHECK constraints (price ≥ 0, rating 1-5)
✅ DEFAULT values (timestamps, is_admin)
✅ Données de seed (admin + amenities initiaux)
✅ PRAGMA foreign_keys = ON (intégrité référentielle active)
```

**Voir :** `PREUVE_BDD_RNCP.md` - Section 3 (copie complète du script)

---

### 4️⃣ Jeux d'Essai et Tests

**A) Données de test intégrées (seed data) :**
- 1 utilisateur admin (`admin@hbnb.io`)
- 3 équipements de base (WiFi, Swimming Pool, Air Conditioning)

**B) Tests d'intégrité implémentés :**

| Test | Type | Description |
|------|------|-------------|
| **Cascade DELETE** | Intégrité référentielle | Supprimer un user → supprime ses places et reviews |
| **UNIQUE constraint** | Contrainte métier | Un user ne peut faire 2 reviews pour la même place |
| **CHECK price** | Validation données | Prix négatif → erreur SQL |
| **CHECK rating** | Validation données | Note hors [1,5] → erreur SQL |
| **FK validation** | Intégrité | Créer place avec owner_id inexistant → erreur |

**Fichiers de tests :**
- `part3/tests/test_auth_flow.py` (tests d'authentification)
- Tests unitaires dans `part2/tests/` (models)

---

## 🔑 POINTS CLÉS POUR LA SOUTENANCE

### ✅ Conformité REAC

**Le projet démontre :**
1. ✅ **Conception MCD** : Entités, relations, cardinalités documentées
2. ✅ **Modélisation MLD** : Tables, PK, FK, contraintes détaillées
3. ✅ **Script SQL fonctionnel** : Déployable en production
4. ✅ **Intégrité référentielle** : CASCADE, NOT NULL, UNIQUE, CHECK
5. ✅ **Relation N:M** : Table d'association `place_amenity`
6. ✅ **Jeu de données** : Seed data + stratégie de tests
7. ✅ **Normalisation** : 3NF respectée (pas de redondance)

### 💡 Points de démonstration technique

1. **Sécurité :**
   - Mots de passe hashés (bcrypt)
   - UUID pour éviter l'énumération
   - Validation stricte des données (CHECK constraints)

2. **Évolutivité :**
   - SQLite pour dev, migrable vers PostgreSQL/MySQL
   - Timestamps sur toutes les tables
   - Architecture en couches (repository pattern)

3. **Performance :**
   - Index implicites sur PK/FK/UNIQUE
   - Requêtes optimisées dans repositories

---

## 📄 DOCUMENTS À PRÉSENTER AU JURY

### Option 1 : Dossier complet (recommandé)
1. **`PREUVE_BDD_RNCP.md`** (ce fichier) - Document maître
2. **`part3/schema.sql`** ou **`part4/schema.sql`** - Script SQL original
3. **Schéma visuel** (optionnel) :
   - Diagramme Mermaid généré
   - OU screenshot de dbdiagram.io
   - OU export MySQL Workbench

### Option 2 : Version condensée
- **`RECAPITULATIF_JURY_RNCP.md`** (ce document)
- **+ copie du `schema.sql`**

---

## 🗂️ STRUCTURE DÈS FICHIERS PROJET

```
holbertonschool-hbnb/
├── PREUVE_BDD_RNCP.md          ← Document complet BDD
├── RECAPITULATIF_JURY_RNCP.md  ← Ce récapitulatif
│
├── part3/                       ← Version avec authentification
│   ├── schema.sql               ← ⭐ SCRIPT SQL PRINCIPAL
│   ├── hbnb/app/
│   │   ├── models/              ← Classes SQLAlchemy
│   │   └── persistence/         ← Repositories (couche BDD)
│   └── tests/
│       └── test_auth_flow.py    ← Tests d'intégrité
│
└── part4/                       ← Version avec interface web
    ├── schema.sql               ← (identique à part3)
    └── ...
```

---

## 📊 STATISTIQUES PROJET

| Métrique | Valeur |
|----------|--------|
| **Tables** | 5 |
| **Relations 1:N** | 3 (user→places, user→reviews, place→reviews) |
| **Relations N:M** | 1 (place↔amenities) |
| **Clés étrangères** | 5 |
| **Contraintes UNIQUE** | 3 (email, amenity name, review) |
| **Contraintes CHECK** | 2 (price, rating) |
| **Lignes de SQL** | ~80 (hors commentaires) |

---

## 🎤 POINTS À MENTIONNER EN SOUTENANCE

### Question probable : "Pourquoi ces choix de conception ?"

**Réponses préparées :**

1. **UUID au lieu d'INT auto-increment ?**
   - Sécurité : pas d'énumération des IDs
   - Distribution : IDs globalement uniques (futur microservices)

2. **CASCADE sur DELETE ?**
   - Cohérence : supprimer un user supprime automatiquement ses données
   - Évite les orphelins (reviews sans auteur)

3. **UNIQUE(user_id, place_id) sur reviews ?**
   - Règle métier : un user ne peut spammer les avis
   - Intégrité : pas de doublon dans les reviews

4. **CHECK(price >= 0) ?**
   - Validation au niveau BDD (défense en profondeur)
   - Empêche les incohérences même si bug applicatif

---

## ✅ CHECKLIST FINALE

Avant la soutenance, vérifiez que vous avez :

- [ ] **MCD lisible** (diagramme + explications)
- [ ] **MLD détaillé** (toutes les contraintes listées)
- [ ] **Script SQL complet** (copié-collé du fichier original)
- [ ] **Liste exhaustive PK/FK/UNIQUE/CHECK**
- [ ] **Exemples de jeux d'essai**
- [ ] **Explication des choix techniques**
- [ ] **Démo possible** (base SQLite générée par le script)

---

## 🚀 DÉMO RAPIDE (optionnel)

Si le jury demande une démonstration :

```bash
# 1. Se placer dans part3
cd part3

# 2. Créer la base de données
sqlite3 instance/development.db < schema.sql

# 3. Vérifier les tables
sqlite3 instance/development.db ".tables"

# 4. Afficher les contraintes d'une table
sqlite3 instance/development.db ".schema reviews"

# 5. Tester une contrainte CHECK
sqlite3 instance/development.db "INSERT INTO reviews (id, text, rating, user_id, place_id) VALUES ('test', 'test', 10, 'a', 'b');"
# → Erreur attendue : CHECK constraint failed: rating BETWEEN 1 AND 5
```

---

## 📞 CONTACT

**Candidat :** [Votre Nom]
**Projet :** HBnB - HolbertonBnB
**Date :** Février 2026
**Référentiel :** RNCP [Numéro]

---

**🎯 Ce dossier prouve la maîtrise complète de la conception et implémentation d'une base de données relationnelle conforme au REAC.**
