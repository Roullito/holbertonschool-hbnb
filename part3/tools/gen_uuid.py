import uuid

amenities = ["WiFi", "Swimming Pool", "Air Conditioning"]

for amenity in amenities:
    print(f"{amenity}: {uuid.uuid4()}")
