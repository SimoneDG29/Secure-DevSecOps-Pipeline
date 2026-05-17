import React, { useState } from "react";
import AuthPage from "./pages/AuthPage";
import ProductsPage from "./pages/ProductsPage";

function App() {
  const [page, setPage] = useState("auth");

  return (
    <div>
      <nav style={{ margin: 16 }}>
        <button onClick={() => setPage("auth")}>Auth</button>
        <button onClick={() => setPage("products")}>Products</button>
        <button onClick={() => setPage("inventory")}>Inventory</button>
      </nav>
      {page === "auth" && <AuthPage />}
      {page === "products" && <ProductsPage />}
      {page === "inventory" && <div>Inventory page coming soon…</div>}
    </div>
  );
}

export default App;