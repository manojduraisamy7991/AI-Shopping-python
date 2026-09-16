import math
import re
from collections import Counter
from typing import Iterable


STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "for",
    "i",
    "in",
    "is",
    "me",
    "need",
    "of",
    "on",
    "or",
    "the",
    "to",
    "under",
    "with",
}


def tokenize(text: str) -> list[str]:
    return [
        token
        for token in re.findall(r"[a-z0-9]+", text.lower())
        if token not in STOP_WORDS
    ]


def vectorize(text: str) -> Counter:
    return Counter(tokenize(text))


def cosine_similarity(left: Counter, right: Counter) -> float:
    shared = set(left) & set(right)
    numerator = sum(left[token] * right[token] for token in shared)
    left_norm = math.sqrt(sum(value * value for value in left.values()))
    right_norm = math.sqrt(sum(value * value for value in right.values()))
    if left_norm == 0 or right_norm == 0:
        return 0.0
    return numerator / (left_norm * right_norm)


class ShoppingRAG:
    def __init__(self) -> None:
        self.products: list[dict] = []
        self._vectors: dict[str, Counter] = {}

    def ingest(self, products: Iterable[dict]) -> None:
        self.products = list(products)
        self._vectors = {
            product["id"]: vectorize(self._product_document(product))
            for product in self.products
        }

    def retrieve(self, query: str, limit: int = 4) -> list[dict]:
        query_vector = vectorize(query)
        ranked = []
        for product in self.products:
            score = cosine_similarity(query_vector, self._vectors[product["id"]])
            if self._price_requested(query) and product["price"] > self._max_price(query):
                score *= 0.55
            ranked.append({**product, "score": round(score, 3)})

        return sorted(ranked, key=lambda item: item["score"], reverse=True)[:limit]

    def answer(self, query: str) -> tuple[str, list[dict]]:
        matches = self.retrieve(query)
        useful_matches = [product for product in matches if product["score"] > 0]
        if not useful_matches:
            useful_matches = matches[:2]

        top = useful_matches[0]
        answer = (
            f"My top pick is {top['name']} at ${top['price']}. "
            f"It fits because {top['short_reason']} "
            f"Also compare {', '.join(product['name'] for product in useful_matches[1:3])}."
        )
        return answer, useful_matches

    def _product_document(self, product: dict) -> str:
        return " ".join(
            [
                product["name"],
                product["category"],
                product["description"],
                " ".join(product["tags"]),
            ]
        )

    def _price_requested(self, query: str) -> bool:
        return self._max_price(query) > 0

    def _max_price(self, query: str) -> int:
        prices = [int(match) for match in re.findall(r"\$?(\d{2,5})", query)]
        return max(prices) if prices else 0
