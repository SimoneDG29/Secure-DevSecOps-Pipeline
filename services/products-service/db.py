import os
import psycopg2


def get_db_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST", "postgres"),
        port=os.getenv("DB_PORT", "5432"),
        dbname=os.getenv("DB_NAME", "products"),
        user=os.getenv("DB_USER", "products_user"),
        password=os.getenv("DB_PASSWORD", "products_pass"),
    )


def init_db():
    with get_db_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS products (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    price_cents INTEGER NOT NULL
                );
                """
            )
        conn.commit()