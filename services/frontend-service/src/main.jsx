import React from "react";
import ReactDOM from "react-dom/client";

function App() {
  return (
    <div>
      <h1>Secure DevSecOps Pipeline Frontend</h1>
      <p>Welcome! This frontend will connect to all backend services.</p>
      <ul>
        <li>Auth: login/register</li>
        <li>Products: list, details, CRUD</li>
        <li>Inventory: view/set quantity</li>
      </ul>
    </div>
  );
}

ReactDOM.createRoot(document.getElementById("root")).render(<App />);