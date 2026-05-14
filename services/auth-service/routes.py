from werkzeug.security import generate_password_hash, check_password_hash
from flask import request, jsonify
from db import get_db_connection


def register_routes(app):

    @app.post("/register")
    def register():
        payload = request.get_json(silent=True) or {}

        username = payload.get("username")
        password = payload.get("password")

        if not username or not password:
            return jsonify(error="username and password required"), 400

        password_hash = generate_password_hash(password)

        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(
                        """
                        INSERT INTO users (username, password_hash)
                        VALUES (%s, %s)
                        RETURNING id;
                        """,
                        (username, password_hash),
                    )
                    user_id = cur.fetchone()[0]
                conn.commit()
        except Exception:
            return jsonify(error="user already exists"), 409

        return jsonify(id=user_id, username=username), 201


    @app.post("/login")
    def login():
        payload = request.get_json(silent=True) or {}

        username = payload.get("username")
        password = payload.get("password")

        if not username or not password:
            return jsonify(error="username and password required"), 400

        with get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    SELECT id, username, password_hash
                    FROM users
                    WHERE username = %s;
                    """,
                    (username,),
                )
                user = cur.fetchone()

        if not user:
            return jsonify(error="invalid credentials"), 401

        user_id, db_username, password_hash = user

        if not check_password_hash(password_hash, password):
            return jsonify(error="invalid credentials"), 401

        return jsonify(id=user_id, username=db_username), 200
    
    @app.get("/healthz")
    def healthz():
        return jsonify(status="ok"), 200