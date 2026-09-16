import os
from typing import Any

from dotenv import load_dotenv


load_dotenv()


def get_chroma_client() -> Any:
    import chromadb

    api_key = os.getenv("CHROMA_API_KEY")
    tenant = os.getenv("CHROMA_TENANT")
    database = os.getenv("CHROMA_DATABASE")

    missing = [
        name
        for name, value in {
            "CHROMA_API_KEY": api_key,
            "CHROMA_TENANT": tenant,
            "CHROMA_DATABASE": database,
        }.items()
        if not value
    ]
    if missing:
        raise RuntimeError(f"Missing Chroma settings: {', '.join(missing)}")

    return chromadb.CloudClient(
        api_key=api_key,
        tenant=tenant,
        database=database,
    )


def get_products_collection() -> Any:
    client = get_chroma_client()
    collection_name = os.getenv("CHROMA_COLLECTION", "products")
    return client.get_or_create_collection(name=collection_name)
