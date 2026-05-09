from flask import jsonify, request
from redis_client import get_redis_client


def register_routes(app):
    @app.post("/inventory/<sku>")
    def set_inventory(sku):
        payload = request.get_json(silent=True) or {}
        quantity = payload.get("quantity")

        if not isinstance(quantity, int) or quantity < 0:
            return jsonify(error="quantity must be a non-negative integer"), 400

        client = get_redis_client()
        client.set(f"inventory:{sku}", quantity)

        return jsonify(sku=sku, quantity=quantity), 200

    @app.get("/healthz")
    def healthz():
        return jsonify(status="ok"), 200