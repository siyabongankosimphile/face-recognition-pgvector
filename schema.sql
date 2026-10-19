-- Run this once in your database (as a superuser or a role that can create extensions)
CREATE EXTENSION IF NOT EXISTS pgvector;

-- persons table: stores a 128-d face embedding (vector)
CREATE TABLE IF NOT EXISTS persons (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  metadata JSONB,
  embedding vector(128),
  created_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);

-- Optional: create an ivfflat index for faster approximate nearest neighbors (create AFTER you have inserted rows)
-- CREATE INDEX ON persons USING ivfflat (embedding vector_l2_ops) WITH (lists = 100);
