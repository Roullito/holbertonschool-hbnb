-- Table users
CREATE TABLE IF NOT EXISTS users (
    id CHAR(36) PRIMARY KEY NOT NULL,
    first_name VARCHAR(255) NOT NULL,
    last_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    is_admin BOOLEAN DEFAULT FALSE
);

-- Table places
CREATE TABLE IF NOT EXISTS places (
    id CHAR(36) PRIMARY KEY NOT NULL,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    owner_id CHAR(36) NOT NULL,
    FOREIGN KEY (owner_id) REFERENCES users(id)
);

-- Table reviews
CREATE TABLE IF NOT EXISTS reviews (
    id CHAR(36) PRIMARY KEY NOT NULL,
    text TEXT,
    rating INT CHECK (rating BETWEEN 1 AND 5),
    user_id CHAR(36) NOT NULL,
    place_id CHAR(36) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    CONSTRAINT unique_review UNIQUE (user_id, place_id)
);

-- Table amenities
CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) PRIMARY KEY NOT NULL,
    name VARCHAR(255) UNIQUE NOT NULL
);

-- Table place_amenity (many-to-many)
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id CHAR(36) NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id) REFERENCES places(id),
    FOREIGN KEY (amenity_id) REFERENCES amenities(id)
);

-- Insert admin to users tables
INSERT INTO users (
    id, email, first_name, last_name, password, is_admin
) VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'admin@hbnb.io',
    'Admin',
    'HBnB',
    '$2b$12$txryxzSae2ihpMFhwrpTBu2sF4P0WaDxJ9eY3bbArntgk5nExtn3q',
    TRUE
);

-- Insert Initial Amenities
INSERT INTO amenities (id, name) VALUES ('26de0779-5dfb-4f77-916d-ed6728e88edd', 'WiFi');
INSERT INTO amenities (id, name) VALUES ('3493beb7-a2aa-4dd2-95e2-be9b1cca3b06', 'Swimming Pool');
INSERT INTO amenities (id, name) VALUES ('3b23dec0-54f2-4a9f-bfb0-49a215961d72', 'Air Conditioning');

