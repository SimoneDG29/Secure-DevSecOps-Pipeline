import app as inventory_app


class FakeRedis:
    def __init__(self):
        self.store = {}

    def get(self, key):
        return self.store.get(key)

    def set(self, key, value):
        self.store[key] = str(value)


def test_inventory_crud():
    fake_redis = FakeRedis()

    def fake_get_redis_client():
        return fake_redis

    inventory_app.get_redis_client = fake_get_redis_client

    client = inventory_app.app.test_client()

    create = client.post("/inventory/sku-123", json={"quantity": 7})
    assert create.status_code == 200
    assert create.get_json() == {"sku": "sku-123", "quantity": 7}

    get_existing = client.get("/inventory/sku-123")
    assert get_existing.status_code == 200
    assert get_existing.get_json() == {"sku": "sku-123", "quantity": 7}

    missing = client.get("/inventory/missing")
    assert missing.status_code == 404