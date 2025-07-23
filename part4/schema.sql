PRAGMA foreign_keys = ON;

-- Table users
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

-- Table places
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

-- Table reviews
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

-- Table amenities
CREATE TABLE IF NOT EXISTS amenities (
    id CHAR(36) PRIMARY KEY NOT NULL,
    name VARCHAR(255) UNIQUE NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Table place_amenity (many-to-many)
CREATE TABLE IF NOT EXISTS place_amenity (
    place_id CHAR(36)   NOT NULL,
    amenity_id CHAR(36) NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (place_id, amenity_id),
    FOREIGN KEY (place_id)   REFERENCES places(id)   ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES amenities(id) ON DELETE CASCADE
);

-- Insert admin user (ignore si déjà présent)
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

-- Insert initial amenities (ignore si déjà présents)
INSERT OR IGNORE INTO amenities (id, name) VALUES
    ('26de0779-5dfb-4f77-916d-ed6728e88edd', 'WiFi'),
    ('3493beb7-a2aa-4dd2-95e2-be9b1cca3b06', 'Swimming Pool'),
    ('3b23dec0-54f2-4a9f-bfb0-49a215961d72', 'Air Conditioning');

