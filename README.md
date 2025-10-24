# Library Management System (SQL + Python)

Relational Library Management System built with Python and SQLite. Includes schema design, entity relations, and SQL queries for search, checkout, and returns.

## Tech
- **DB**: SQLite (SQL DDL in `schema.sql`, seed data in `seed.sql`)
- **Python**: `sqlite3` stdlib for queries, small CLI in `app.py`
- **Tables**: `books`, `authors`, `book_authors` (M:N), `patrons`, `book_copies`, `loans`


## Schema

- books(id, isbn, title, published_year)
- authors(id, name)
- book_authors(book_id, author_id)  
- patrons(id, name, email)
- book_copies(id, book_id, barcode)  
- loans(id, copy_id, patron_id, checkout_at, due_at, returned_at)

**Rules**
- A loan exists only for a valid patron + copy (FKs).
- A copy is available when it has no active loan (returned_at IS NULL).
- Checkout sets `checkout_at=now`, `due_at=now + 14 days` (configurable in `app.py`).


## Files
```
src/
  app.py          
  db.py           
  schema.sql      
  seed.sql        
  queries.sql     
tests/
  test_smoke.py   
requirements.txt
README.md
```
