# 🎯 FICHE SYNTHÈSE BDD - CERTIFICATION RNCP
## Projet HBnB - Vue d'ensemble rapide

---

## 📊 TABLES ET CONTRAINTES

### **USERS**
```
PK: id (UUID)
UNIQUE: email
FK: aucune
CHECK: aucun
Colonnes: id, first_name, last_name, email, password, is_admin, created_at, updated_at
```

### **PLACES**
```
PK: id (UUID)
UNIQUE: aucune
FK: owner_id → users.id (CASCADE)
CHECK: price >= 0
Colonnes: id, title, description, price, latitude, longitude, owner_id, created_at, updated_at
```

### **REVIEWS**
```
PK: id (UUID)
UNIQUE: (user_id, place_id)
FK: user_id → users.id (CASCADE)
    place_id → places.id (CASCADE)
CHECK: rating BETWEEN 1 AND 5
Colonnes: id, text, rating, user_id, place_id, created_at, updated_at
```

### **AMENITIES**
```
PK: id (UUID)
UNIQUE: name
FK: aucune
CHECK: aucun
Colonnes: id, name, created_at, updated_at
```

### **PLACE_AMENITY** (N:M)
```
PK: (place_id, amenity_id)
UNIQUE: clé primaire
FK: place_id → places.id (CASCADE)
    amenity_id → amenities.id (CASCADE)
CHECK: aucun
Colonnes: place_id, amenity_id, created_at, updated_at
```

---

## 🔗 RELATIONS

| De | Vers | Type | Cardinalité |
|----|------|------|-------------|
| USER | PLACE | 1:N | 1 user possède 0..* places |
| USER | REVIEW | 1:N | 1 user écrit 0..* reviews |
| PLACE | REVIEW | 1:N | 1 place reçoit 0..* reviews |
| PLACE | AMENITY | N:M | Via table `place_amenity` |

---

## ✅ CONFORMITÉ REAC

| Exigence | ✅ | Preuve |
|----------|---|--------|
| MCD complet | ✅ | 5 entités, 4 relations |
| MLD détaillé | ✅ | PK/FK/UNIQUE/CHECK documentés |
| Script SQL | ✅ | `schema.sql` (80 lignes) |
| Intégrité référentielle | ✅ | CASCADE sur toutes les FK |
| Contraintes métier | ✅ | UNIQUE(user,place), CHECK(rating), CHECK(price) |
| Relation N:M | ✅ | `place_amenity` avec PK composite |
| Jeu de données | ✅ | Seed: 1 admin + 3 amenities |
| Tests | ✅ | Tests d'intégrité + auth |

---

## 📁 FICHIERS À PRÉSENTER

1. **`PREUVE_BDD_RNCP.md`** - Document complet (MCD/MLD/SQL)
2. **`RECAPITULATIF_JURY_RNCP.md`** - Guide pour la soutenance
3. **`part3/schema.sql`** - Script SQL source
4. **Cette fiche** - Référence rapide

---

## 💬 PHRASE CLÉ POUR LE JURY

> *"J'ai conçu une base de données relationnelle de 5 tables avec 5 clés étrangères, 3 contraintes UNIQUE, 2 contraintes CHECK, et une relation many-to-many via table d'association. L'intégrité est garantie par des CASCADE et des contraintes métier comme l'unicité des reviews par utilisateur et par logement."*

---

## 📊 CHIFFRES CLÉS

- **5** tables
- **5** clés étrangères
- **5** clés primaires
- **3** contraintes UNIQUE
- **2** contraintes CHECK
- **1** relation N:M
- **3** relations 1:N
- **80+** lignes SQL

---

## 🗂️ SEED DATA

```sql
-- Admin par défaut
admin@hbnb.io (mot de passe hashé bcrypt)

-- Équipements
- WiFi
- Swimming Pool
- Air Conditioning
```

---

## 🎤 QUESTIONS JURY - RÉPONSES ÉCLAIR

**Q: Pourquoi UUID au lieu d'INT ?**
R: Sécurité (pas d'énumération) + distribution (IDs globalement uniques)

**Q: Pourquoi CASCADE sur DELETE ?**
R: Éviter les orphelins (ex: review sans auteur si user supprimé)

**Q: Comment éviter les doublons de reviews ?**
R: Contrainte UNIQUE(user_id, place_id)

**Q: Comment valider les données ?**
R: CHECK constraints (price≥0, rating∈[1,5]) + validation applicative

**Q: Normalisation ?**
R: 3NF respectée, pas de redondance, table N:M pour amenities

---

**Document créé pour : Certification RNCP**
**Projet : HBnB (HolbertonBnB)**
**Date : Février 2026**
