import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / 'library.db'

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db(schema_sql: str, seed_sql: str):
    with get_conn() as conn:
        conn.executescript(schema_sql)
        conn.executescript(seed_sql)

def query(conn, sql, params=None):
    cur = conn.execute(sql, params or {})
    return [dict(row) for row in cur.fetchall()]

def execute(conn, sql, params=None):
    cur = conn.execute(sql, params or {})
    return cur.lastrowid
