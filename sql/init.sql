CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS products (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  price NUMERIC NOT NULL,
  rating NUMERIC NOT NULL,
  description TEXT NOT NULL,
  tags TEXT[] NOT NULL,
  embedding vector(1536)
);
