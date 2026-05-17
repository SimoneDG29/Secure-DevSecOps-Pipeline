import React, { useEffect, useState } from "react";
import { getProducts, getProduct } from "../api";

export default function ProductsPage() {
  const [products, setProducts] = useState([]);
  const [selected, setSelected] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getProducts()
      .then(setProducts)
      .catch(e => setError(e.message));
  }, []);

  async function handleSelect(sku) {
    setError("");
    try {
      const prod = await getProduct(sku);
      setSelected(prod);
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div style={{ maxWidth: 600, margin: "2rem auto" }}>
      <h2>Products</h2>
      {error && <div style={{ color: "red" }}>{error}</div>}
      <ul>
        {products.map(p => (
          <li key={p.sku}>
            <button onClick={() => handleSelect(p.sku)}>{p.name || p.sku}</button>
          </li>
        ))}
      </ul>
      {selected && (
        <div style={{ marginTop: 24 }}>
          <h3>Product Details</h3>
          <pre>{JSON.stringify(selected, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}