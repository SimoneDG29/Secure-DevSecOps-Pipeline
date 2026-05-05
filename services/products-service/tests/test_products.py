import routes
from app import app

class FakeCursor:
    def __init__(self, store):
        self.store = store
        self._row = None
        self._rows = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, query, params=None):
        if query.startswith("INSERT INTO products"):
            name, price_cents = params
            new_id = len(self.store) + 1
            self.store.append((new_id, name, price_cents))
            self._row = (new_id,)
            return

        if query.startswith("SELECT id, name, price_cents FROM products WHERE id"):
            product_id = params[0]
            self._row = next((row for row in self.store if row[0] == product_id), None)
            return

        if query.startswith("SELECT id, name, price_cents FROM products ORDER BY id"):
            self._rows = list(self.store)

    def fetchone(self):
        return self._row

    def fetchall(self):
        return self._rows

class FakeConn:
    def __init__(self, store):
        self.store = store

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def cursor(self):
        return FakeCursor(self.store)

    def commit(self):
        return None

def test_products_crud():
    store = []

    def fake_get_db_connection():
        return FakeConn(store)

    routes.get_db_connection = fake_get_db_connection

    client = app.test_client()
    create = client.post(
        "/products",
        json={"name": "Widget", "price_cents": 1999},
    )
    assert create.status_code == 201
    assert create.get_json()["id"] == 1

    listed = client.get("/products")
    assert listed.status_code == 200
    assert listed.get_json()["products"] == [
        {"id": 1, "name": "Widget", "price_cents": 1999}
    ]

    get_one = client.get("/products/1")
    assert get_one.status_code == 200
    assert get_one.get_json() == {"id": 1, "name": "Widget", "price_cents": 1999}

    missing = client.get("/products/999")
    assert missing.status_code == 404