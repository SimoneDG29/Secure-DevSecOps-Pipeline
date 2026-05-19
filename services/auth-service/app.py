from db import init_db
from flask import Flask
from routes import register_routes

app = Flask(__name__)
CORS(
    app,
    resources={r"/*": {"origins": ["http://localhost:5173"]}}
)

register_routes(app)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=5001)