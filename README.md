# Library Management System (SQL + Python)

A simple **relational** library DB built on **SQLite** with a small Python query layer + CLI.
Kept intentionally straightforward (college-student level) but correct: proper FKs, indexes, and
a basic checkout/return flow with due dates and overdue reporting.

## Tech
- **DB**: SQLite (SQL DDL in `schema.sql`, seed data in `seed.sql`)
- **Python**: `sqlite3` stdlib for queries, small CLI in `app.py`
- **Tables**: `books`, `authors`, `book_authors` (M:N), `patrons`, `book_copies`, `loans`

---

## Quick Start

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate
pip install -r requirements.txt

# Initialize database (creates library.db and seeds data)
python src/app.py --init

# Try the CLI
python src/app.py --help
python src/app.py search --q "harry"
python src/app.py checkout --patron 1 --book 3
python src/app.py return --barcode CPY-0005
python src/app.py overdue
python src/app.py whohas --barcode CPY-0005
```

The DB file `library.db` is created in the project root.

---

## Schema (ER snapshot)

- **books(id, isbn, title, published_year)**
- **authors(id, name)**
- **book_authors(book_id, author_id)**  ← M:N bridge
- **patrons(id, name, email)**
- **book_copies(id, book_id, barcode)**  ← physical copies
- **loans(id, copy_id, patron_id, checkout_at, due_at, returned_at)**

**Rules**
- A loan exists only for a valid patron + copy (FKs).
- A copy is *available* when it has **no active loan** (returned_at IS NULL).
- Checkout sets `checkout_at=now`, `due_at=now + 14 days` (configurable in `app.py`).

---

## What to show recruiters
- Clean SQL DDL with keys + indexes (`src/schema.sql`).
- Parameterized queries (no string concat) in `src/db.py`.
- Clear functions: `search_books`, `checkout_book`, `return_copy`, `list_overdue`, etc.
- Small tests in `tests/test_smoke.py`.

---

## Files
```
src/
  app.py          # CLI + entry points
  db.py           # DB helpers / query layer
  schema.sql      # DDL
  seed.sql        # Starter data
  queries.sql     # Reference queries (study aid)
tests/
  test_smoke.py   # tiny smoke check
requirements.txt
README.md
```
