# Ecomer AI Shopping Assistant - UI / Backend Info

## Project Goal

Build a simple ecommerce AI shopping assistant MVP where a user types what they want, the backend retrieves matching products, and the UI displays an assistant answer with product cards.

## UI

Location:

```text
frontend/
```

Tech:

- React
- Vite
- CSS
- lucide-react icons

Main files:

- `frontend/src/main.jsx` - React app and API calls
- `frontend/src/styles.css` - page styling
- `frontend/package.json` - frontend dependencies and scripts

Run:

```powershell
cd frontend
npm install
npm run dev
```

URL:

```text
http://localhost:5173
```

UI flow:

1. User types a shopping request.
2. UI sends `POST /chat` to the FastAPI backend.
3. UI displays the AI-style answer.
4. UI displays matching products as cards.

## Backend

Location:

```text
app/
```

Tech:

- FastAPI
- Pydantic
- Local RAG-style retrieval
- Optional PostgreSQL + pgvector upgrade path

Main files:

- `app/main.py` - API routes
- `app/rag.py` - retrieval and recommendation logic
- `app/seed.py` - sample product data
- `requirements.txt` - Python dependencies

Run:

```powershell
venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

URLs:

```text
API: http://localhost:8000
Docs: http://localhost:8000/docs
Health: http://localhost:8000/health
```

Backend endpoints:

```text
GET  /health
GET  /products
POST /search
POST /chat
POST /ingest/seed
```

Example chat request:

```json
{
  "message": "I need workout earbuds under $100"
}
```

## Database

Current MVP:

- Uses in-memory seed data from `app/seed.py`
- Uses local cosine similarity in `app/rag.py`
- No database required to test the first MVP

Next step:

- Start PostgreSQL with pgvector using `docker-compose.yml`
- Store products in PostgreSQL
- Store embeddings in `vector(1536)`
- Use LangChain to create embeddings and run similarity search

Run PostgreSQL:

```powershell
docker compose up -d
```

Database init file:

```text
sql/init.sql
```

## Simple MVP Checklist

1. Backend runs on port `8000`.
2. Frontend runs on port `5173`.
3. `GET /products` returns seed products.
4. `POST /chat` returns an answer and product matches.
5. React UI displays answer and product cards.
6. PostgreSQL + LangChain can be added after the local MVP works.
