import React, { useEffect, useState } from "react";
import { createRoot } from "react-dom/client";
import { Search, Send, ShoppingBag, Sparkles } from "lucide-react";
import "./styles.css";

const API_URL = "http://127.0.0.1:8000";

function App() {
  const [message, setMessage] = useState("I need workout earbuds under $100");
  const [answer, setAnswer] = useState("");
  const [products, setProducts] = useState([]);
  const [catalog, setCatalog] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${API_URL}/products`)
      .then((response) => response.json())
      .then((data) => setCatalog(data.products ?? []))
      .catch(() => setCatalog([]));
  }, []);

  async function askAssistant(event) {
    event.preventDefault();
    setLoading(true);
    setAnswer("");

    try {
      const response = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message }),
      });
      const data = await response.json();
      setAnswer(data.answer);
      setProducts(data.products ?? []);
    } catch {
      setAnswer("The assistant API is not reachable. Start FastAPI on port 8000.");
      setProducts([]);
    } finally {
      setLoading(false);
    }
  }

  const visibleProducts = products.length > 0 ? products : catalog;

  return (
    <main className="shell">
      <section className="assistant">
        <div className="brand">
          <span className="mark">
            <ShoppingBag size={24} />
          </span>
          <div>
            <h1>Ecomer AI Shopping Assistant</h1>
            <p>Ask for a use case, budget, or product type and get ranked recommendations.</p>
          </div>
        </div>

        <form className="composer" onSubmit={askAssistant}>
          <Search size={20} />
          <input
            value={message}
            onChange={(event) => setMessage(event.target.value)}
            placeholder="What are you shopping for?"
          />
          <button type="submit" disabled={loading || message.trim().length < 2} title="Ask assistant">
            <Send size={18} />
          </button>
        </form>

        <div className="answer">
          <Sparkles size={20} />
          <p>{loading ? "Searching the product catalog..." : answer || "Recommendations will appear here."}</p>
        </div>
      </section>

      <section className="grid" aria-label="Products">
        {visibleProducts.map((product) => (
          <article className="product" key={product.id}>
            <div className="productTop">
              <span>{product.category}</span>
              <strong>${product.price}</strong>
            </div>
            <h2>{product.name}</h2>
            <p>{product.description}</p>
            <div className="meta">
              <span>{product.rating} rating</span>
              {product.score !== undefined && <span>{product.score} match</span>}
            </div>
          </article>
        ))}
      </section>
    </main>
  );
}

createRoot(document.getElementById("root")).render(<App />);
