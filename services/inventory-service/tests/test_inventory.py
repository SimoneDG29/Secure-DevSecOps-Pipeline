import app as inventory_app


class FakeRedis:
    def __init__(self):
        self.store = {}

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