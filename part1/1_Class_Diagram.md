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
