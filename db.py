import os
import json
import psycopg2
from pgvector.psycopg2 import register_vector

DATABASE_URL = os.environ.get("DATABASE_URL")  # e.g. postgres://user:pass@host:port/dbname

def get_conn():
    conn = psycopg2.connect(DATABASE_URL)
    register_vector(conn)  # enable pgvector adapter
    return conn

def create_tables():
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(open("schema.sql").read())
    conn.close()

def insert_person(name, embedding, metadata=None):
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO persons (name, embedding, metadata) VALUES (%s, %s, %s) RETURNING id",
                (name, embedding, json.dumps(metadata) if metadata else None),
            )
            new_id = cur.fetchone()[0]
    conn.close()
    return new_id

def find_nearest(embedding, top_k=5):
    """
    Returns rows ordered by L2 distance (closest first).
    Each row: (id, name, embedding, distance)
    """
    conn = get_conn()
    with conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT id, name, embedding, (embedding <-> %s) AS distance FROM persons ORDER BY distance ASC LIMIT %s",
                (embedding, top_k),
            )
            results = cur.fetchall()
    conn.close()
    return results
