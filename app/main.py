from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from app.rag import ShoppingRAG
from app.seed import SEED_PRODUCTS


app = FastAPI(title="Ecomer AI Shopping Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rag = ShoppingRAG()
rag.ingest(SEED_PRODUCTS)


class ChatRequest(BaseModel):
    message: str = Field(min_length=2, examples=["I need headphones for workouts under $100"])


class SearchRequest(BaseModel):
    query: str = Field(min_length=2, examples=["lightweight running shoes"])
    limit: int = Field(default=4, ge=1, le=10)


@app.get("/")
def home():
    return {
        "message": "Ecomer AI Shopping Assistant API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health():
    return {"status": "ok", "products_indexed": len(rag.products)}


@app.get("/products")
def products():
    return {"products": rag.products}


@app.post("/search")
def search(request: SearchRequest):
    return {"results": rag.retrieve(request.query, request.limit)}


@app.post("/chat")
def chat(request: ChatRequest):
    answer, matches = rag.answer(request.message)
    return {"answer": answer, "products": matches}


@app.post("/ingest/seed")
def ingest_seed():
    rag.ingest(SEED_PRODUCTS)
    return {"message": "Seed products indexed", "products_indexed": len(rag.products)}
