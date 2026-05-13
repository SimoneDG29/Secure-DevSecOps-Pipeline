const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:5002";
const AUTH_URL = import.meta.env.VITE_AUTH_URL || "http://localhost:5001";
const PRODUCTS_URL = import.meta.env.VITE_PRODUCTS_URL || "http://localhost:5003";
const INVENTORY_URL = import.meta.env.VITE_INVENTORY_URL || "http://localhost:5004";

// Auth API
export async function login(username, password) {
  const res = await fetch(`${AUTH_URL}/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
    credentials: "include",
  });
  if (!res.ok) throw new Error("Login failed");
  return res.json();
}

export async function register(username, password) {
  const res = await fetch(`${AUTH_URL}/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  if (!res.ok) throw new Error("Register failed");
  return res.json();
}

// Products API
export async function getProducts() {
  const res = await fetch(`${PRODUCTS_URL}/products`);
  if (!res.ok) throw new Error("Failed to fetch products");
  return res.json();
}

export async function getProduct(sku) {
  const res = await fetch(`${PRODUCTS_URL}/products/${sku}`);
  if (!res.ok) throw new Error("Failed to fetch product");
  return res.json();
}

// Inventory API
export async function getInventory(sku) {
  const res = await fetch(`${INVENTORY_URL}/inventory/${sku}`);
  if (!res.ok) throw new Error("Failed to fetch inventory");
  return res.json();
}

export async function setInventory(sku, quantity) {
  const res = await fetch(`${INVENTORY_URL}/inventory/${sku}`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ quantity }),
  });
  if (!res.ok) throw new Error("Failed to set inventory");
  return res.json();
}