import React, { useState } from "react";
import { getInventory, setInventory } from "../api";

export default function InventoryPage() {
  const [sku, setSku] = useState("");
  const [quantity, setQuantity] = useState("");
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function handleGet(e) {
    e.preventDefault();
    setError("");
    setResult(null);
    try {
      const data = await getInventory(sku);
      setResult(data);
      setQuantity(data.quantity);
    } catch (e) {
      setError(e.message);
    }
  }

  async function handleSet(e) {
    e.preventDefault();
    setError("");
    try {
      const data = await setInventory(sku, Number(quantity));
      setResult(data);
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div style={{ maxWidth: 400, margin: "2rem auto" }}>
      <h2>Inventory</h2>
      <form onSubmit={handleGet}>
        <input
          type="text"
          placeholder="SKU"
          value={sku}
          onChange={e => setSku(e.target.value)}
          required
          style={{ width: "100%", marginBottom: 8 }}
        />
        <button type="submit" style={{ width: "100%" }}>
          Get Inventory
        </button>
      </form>
      {result && (
        <div style={{ marginTop: 16 }}>
          <div>SKU: {result.sku}</div>
          <div>
            Quantity:{" "}
            <input
              type="number"
              value={quantity}
              onChange={e => setQuantity(e.target.value)}
              style={{ width: 80 }}
            />
            <button onClick={handleSet} style={{ marginLeft: 8 }}>
              Update
            </button>
          </div>
        </div>
      )}
      {error && <div style={{ color: "red", marginTop: 16 }}>{error}</div>}
    </div>
  );
}