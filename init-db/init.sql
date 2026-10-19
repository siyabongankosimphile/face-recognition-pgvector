-- Initialize the database: create pgvector extension and persons table
CREATE EXTENSION IF NOT EXISTS pgvector;

CREATE TABLE IF NOT EXISTS persons (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  metadata JSONB,
  embedding vector(128),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
