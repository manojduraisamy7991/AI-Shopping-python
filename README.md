# Ecomer AI Shopping Assistant MVP
<img width="1897" height="872" alt="image" src="https://github.com/user-attachments/assets/3a289d3d-ff63-4577-8f86-42408f5f5339" />


Simple React + FastAPI shopping assistant with a RAG-style retrieval flow.

## What This MVP Includes

1. FastAPI backend
2. React frontend
3. Product catalog seed data
4. Local vector-style retrieval using cosine similarity
5. Chat endpoint that recommends products from retrieved context
6. PostgreSQL + pgvector upgrade path

## Step By Step

### 1. Run The Backend

```powershell
venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Open:

- API: http://localhost:8000
- Swagger docs: http://localhost:8000/docs

### 2. Run The React Frontend

```powershell
cd frontend
npm install
npm run dev
```

Open http://localhost:5173.

### 3. Test The Assistant

Try:

- `I need workout earbuds under $100`
- `best lightweight running shoes`
- `something compact for coffee in a dorm`
- `noise cancelling headphones for travel`

## MVP Architecture

```text
React UI
  -> POST /chat
FastAPI
  -> retrieve matching products
  -> generate recommendation from product context
Product data
  -> seeded in app/seed.py
Vector layer
  -> local cosine similarity in app/rag.py
```

## PostgreSQL + Vector Database Step

For the next step, use PostgreSQL with pgvector:

```sql
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE products (
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  category TEXT NOT NULL,
  price NUMERIC NOT NULL,
  rating NUMERIC NOT NULL,
  description TEXT NOT NULL,
  tags TEXT[] NOT NULL,
  embedding vector(1536)
);
```

Then replace `app/rag.py` with:

1. an embedding model from LangChain,
2. writes to PostgreSQL,
3. similarity search using pgvector,
4. an LLM call that receives the retrieved product rows as context.
