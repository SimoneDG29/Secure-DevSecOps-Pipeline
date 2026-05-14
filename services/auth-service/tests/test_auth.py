import routes
from app import app


class FakeCursor:
    def __init__(self, store):
        self.store = store
        self.result = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def execute(self, query, params=None):
        if query.strip().startswith("INSERT INTO users"):
            username, password_hash = params

            for user in self.store:
                if user["username"] == username:
                    raise Exception("duplicate")

            user = {
                "id": len(self.store) + 1,
                "username": username,
                "password_hash": password_hash,
            }
            self.store.append(user)
            self.result = (user["id"],)

        elif query.strip().startswith("SELECT id, username, password_hash"):
            username = params[0]

            for user in self.store:
                if user["username"] == username:
                    self.result = (
                        user["id"],
                        user["username"],
                        user["password_hash"],
                    )
                    return

            self.result = None

    def fetchone(self):
        return self.result


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


def test_register_and_login(monkeypatch):
    store = []

    def fake_get_db_connection():
        return FakeConn(store)

    monkeypatch.setattr(
        routes,
        "get_db_connection",
        fake_get_db_connection,
        raising=False,
    )

    client = app.test_client()

    register = client.post(
        "/register",
        json={"username": "alice", "password": "secret123"},
    )
    assert register.status_code == 201

    login = client.post(
        "/login",
        json={"username": "alice", "password": "secret123"},
    )
    assert login.status_code == 200

    wrong = client.post(
        "/login",
        json={"username": "alice", "password": "wrong"},
    )
    assert wrong.status_code == 401