import argparse
from datetime import datetime, timedelta
from pathlib import Path
from tabulate import tabulate
from db import get_conn, init_db, query, execute

BASE = Path(__file__).resolve().parents[1]
SCHEMA = (BASE / 'src' / 'schema.sql').read_text(encoding='utf-8')
SEED = (BASE / 'src' / 'seed.sql').read_text(encoding='utf-8')

DUE_DAYS = 14

def fmt(rows):
    if not rows:
        print('(no results)')
        return
    print(tabulate(rows, headers='keys', tablefmt='github'))

def cmd_init(args):
    init_db(SCHEMA, SEED)
    print('Database initialized and seeded: library.db')

def cmd_search(args):
    kw = f"%{args.q}%"
    sql = '''
    SELECT b.id, b.title,
           GROUP_CONCAT(a.name, ', ') AS authors,
           b.published_year
    FROM books b
    JOIN book_authors ba ON ba.book_id = b.id
    JOIN authors a ON a.id = ba.author_id
    WHERE b.title LIKE :kw OR a.name LIKE :kw
    GROUP BY b.id
    ORDER BY b.title;
    '''
    with get_conn() as conn:
        rows = query(conn, sql, {'kw': kw})
        fmt(rows)

def available_copy(conn, book_id: int):
    sql = '''
    SELECT c.id, c.barcode
    FROM book_copies c
    LEFT JOIN loans l ON l.copy_id = c.id AND l.returned_at IS NULL
    WHERE c.book_id = :book_id AND l.id IS NULL
    LIMIT 1;
    '''
    rows = query(conn, sql, {'book_id': book_id})
    return rows[0] if rows else None

def cmd_checkout(args):
    with get_conn() as conn:
        copy = available_copy(conn, args.book)
        if not copy:
            print('No available copies for that book.')
            return
        now = datetime.utcnow()
        due = now + timedelta(days=DUE_DAYS)
        sql = '''
        INSERT INTO loans(copy_id, patron_id, checkout_at, due_at)
        VALUES (:copy_id, :patron_id, :checkout_at, :due_at);
        '''
        execute(conn, sql, {
            'copy_id': copy['id'],
            'patron_id': args.patron,
            'checkout_at': now.strftime('%Y-%m-%d %H:%M:%S'),
            'due_at': due.strftime('%Y-%m-%d %H:%M:%S'),
        })
        conn.commit()
        print(f"Checked out {copy['barcode']} to patron {args.patron}. Due {due.date()}.")

def cmd_return(args):
    with get_conn() as conn:
        sql = '''
        SELECT l.id
        FROM loans l
        JOIN book_copies c ON c.id = l.copy_id
        WHERE c.barcode = :barcode AND l.returned_at IS NULL
        LIMIT 1;
        '''
        rows = query(conn, sql, {'barcode': args.barcode})
        if not rows:
            print('No active loan found for that barcode.')
            return
        loan_id = rows[0]['id']
        now = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        execute(conn, 'UPDATE loans SET returned_at = :ts WHERE id = :id;', {'ts': now, 'id': loan_id})
        conn.commit()
        print(f'Returned {args.barcode}.')

def cmd_overdue(args):
    sql = '''
    SELECT p.name AS patron, b.title, c.barcode, l.due_at
    FROM loans l
    JOIN patrons p ON p.id = l.patron_id
    JOIN book_copies c ON c.id = l.copy_id
    JOIN books b ON b.id = c.book_id
    WHERE l.returned_at IS NULL AND l.due_at < datetime('now')
    ORDER BY l.due_at ASC;
    '''
    with get_conn() as conn:
        rows = query(conn, sql)
        fmt(rows)

def cmd_whohas(args):
    sql = '''
    SELECT p.name AS patron, p.email, b.title, l.checkout_at, l.due_at
    FROM loans l
    JOIN patrons p ON p.id = l.patron_id
    JOIN book_copies c ON c.id = l.copy_id
    JOIN books b ON b.id = c.book_id
    WHERE c.barcode = :barcode AND l.returned_at IS NULL
    '''
    with get_conn() as conn:
        rows = query(conn, sql, {'barcode': args.barcode})
        fmt(rows)

def main():
    ap = argparse.ArgumentParser(description='Library DB CLI')
    ap.add_argument('--init', action='store_true', help='Initialize database and seed data')
    sub = ap.add_subparsers(dest='cmd')

    s = sub.add_parser('search', help='Search books by title/author')
    s.add_argument('--q', required=True, help='Keyword')
    s.set_defaults(func=cmd_search)

    co = sub.add_parser('checkout', help='Checkout the first available copy of a book to a patron')
    co.add_argument('--patron', required=True, type=int, help='Patron ID')
    co.add_argument('--book', required=True, type=int, help='Book ID')
    co.set_defaults(func=cmd_checkout)

    ret = sub.add_parser('return', help='Return a copy by barcode')
    ret.add_argument('--barcode', required=True)
    ret.set_defaults(func=cmd_return)

    ov = sub.add_parser('overdue', help='List overdue loans')
    ov.set_defaults(func=cmd_overdue)

    wh = sub.add_parser('whohas', help='Who has a copy (by barcode)')
    wh.add_argument('--barcode', required=True)
    wh.set_defaults(func=cmd_whohas)

    args = ap.parse_args()
    if args.init:
        cmd_init(args)
        return
    if hasattr(args, 'func'):
        args.func(args)
    else:
        ap.print_help()

if __name__ == '__main__':
    main()
