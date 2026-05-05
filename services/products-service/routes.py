from flask import jsonify, request
from db import get_db_connection


def register_routes(app):

    @app.post("/products")
    def create_product():
        payload = request.get_json(silent=True) or {}
        name = payload.get("name")
        price_cents = payload.get("price_cents")

        if not name or not isinstance(price_cents, int):
            return jsonify(error="name and price_cents are required"), 400

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO products (name, price_cents) VALUES (%s, %s) RETURNING id;",
                    (name, price_cents),
                )
                product_id = cur.fetchone()[0]
            conn.commit()

        return jsonify(
            id=product_id,
            name=name,
            price_cents=price_cents
        ), 201

    @app.get("/products")
    def list_products():
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, name, price_cents FROM products ORDER BY id;"
                )
                rows = cur.fetchall()

        products = [
            {"id": row[0], "name": row[1], "price_cents": row[2]}
            for row in rows
        ]
        return jsonify(products=products), 200

    @app.get("/products/<int:product_id>")
    def get_product(product_id):
        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, name, price_cents FROM products WHERE id = %s;",
                    (product_id,),
                )
                row = cur.fetchone()

        if not row:
            return jsonify(error="not found"), 404

        return jsonify(
            id=row[0],
            name=row[1],
            price_cents=row[2]
        ), 200

    @app.get("/healthz")
    def healthz():
        return jsonify(status="ok"), 200