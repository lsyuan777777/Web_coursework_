-- CosmicLens API - Database Schema
-- Run this SQL to create the database and tables manually

-- Create database (run as postgres superuser)
-- CREATE DATABASE cosmiclens;

-- Connect to cosmiclens database, then run:

-- Create extension for UUID if needed
-- CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create enum type for media types
CREATE TYPE mediatype AS ENUM ('image', 'video', 'other');

-- Create astronomy_pictures table
CREATE TABLE astronomy_pictures (
    id SERIAL PRIMARY KEY,
    date DATE UNIQUE NOT NULL,
    title VARCHAR(500) NOT NULL,
    explanation TEXT NOT NULL,
    media_url VARCHAR(1000),
    hd_url VARCHAR(1000),
    media_type mediatype DEFAULT 'image' NOT NULL,
    thumbnail_url VARCHAR(1000),
    copyright VARCHAR(500),
    year INTEGER NOT NULL,
    month INTEGER NOT NULL,
    keywords TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes for common queries
CREATE INDEX idx_pictures_date ON astronomy_pictures(date DESC);
CREATE INDEX idx_pictures_year ON astronomy_pictures(year);
CREATE INDEX idx_pictures_month ON astronomy_pictures(month);
CREATE INDEX idx_pictures_media_type ON astronomy_pictures(media_type);
CREATE INDEX idx_pictures_title ON astronomy_pictures(title);
CREATE INDEX idx_pictures_keywords ON astronomy_pictures USING GIN (to_tsvector('english', keywords));

-- Create collections table
CREATE TABLE collections (
    id SERIAL PRIMARY KEY,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    is_public INTEGER DEFAULT 1,  -- 1 = public, 0 = private
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    picture_count INTEGER DEFAULT 0
);

CREATE INDEX idx_collections_name ON collections(name);
CREATE INDEX idx_collections_is_public ON collections(is_public);

-- Create collection_pictures junction table
CREATE TABLE collection_pictures (
    collection_id INTEGER NOT NULL REFERENCES collections(id) ON DELETE CASCADE,
    picture_id INTEGER NOT NULL REFERENCES astronomy_pictures(id) ON DELETE CASCADE,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (collection_id, picture_id)
);

CREATE INDEX idx_collection_pictures_collection ON collection_pictures(collection_id);
CREATE INDEX idx_collection_pictures_picture ON collection_pictures(picture_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for automatic updated_at
CREATE TRIGGER update_astronomy_pictures_updated_at
    BEFORE UPDATE ON astronomy_pictures
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_collections_updated_at
    BEFORE UPDATE ON collections
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- Grant permissions (adjust as needed)
-- GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO your_user;
-- GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO your_user;
