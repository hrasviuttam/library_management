-- Reference SQL snippets used by the CLI

-- Search by title/author
SELECT b.id, b.title, GROUP_CONCAT(a.name, ', ') AS authors, b.published_year
FROM books b
JOIN book_authors ba ON ba.book_id = b.id
JOIN authors a ON a.id = ba.author_id
WHERE b.title LIKE :kw OR a.name LIKE :kw
GROUP BY b.id
ORDER BY b.title;

-- Available copies for a book
SELECT c.id, c.barcode
FROM book_copies c
LEFT JOIN loans l ON l.copy_id = c.id AND l.returned_at IS NULL
WHERE c.book_id = :book_id AND l.id IS NULL;

-- Overdue
SELECT p.name AS patron, b.title, c.barcode, l.due_at
FROM loans l
JOIN patrons p ON p.id = l.patron_id
JOIN book_copies c ON c.id = l.copy_id
JOIN books b ON b.id = c.book_id
WHERE l.returned_at IS NULL AND l.due_at < datetime('now');
