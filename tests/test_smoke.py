from pathlib import Path
from src.db import get_conn, query

def test_books_exist():
    db = Path('library.db')
    assert db.exists(), 'Initialize the DB first with: python src/app.py --init'
    with get_conn() as conn:
        rows = query(conn, 'SELECT COUNT(*) AS n FROM books')
        assert rows[0]['n'] >= 5
