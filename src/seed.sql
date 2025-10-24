INSERT INTO books(isbn, title, published_year) VALUES
 ('9780439708180','Harry Potter and the Sorcerer''s Stone',1997),
 ('9780439064873','Harry Potter and the Chamber of Secrets',1998),
 ('9780590353427','The Pragmatic Programmer',1999),
 ('9780131103627','The C Programming Language',1988),
 ('9781492051367','Fluent Python',2015);

INSERT INTO authors(name) VALUES
 ('J.K. Rowling'),
 ('Andrew Hunt'),
 ('David Thomas'),
 ('Brian W. Kernighan'),
 ('Dennis M. Ritchie'),
 ('Luciano Ramalho');

INSERT INTO book_authors(book_id, author_id) VALUES
 (1,1),
 (2,1),
 (3,2),(3,3),
 (4,4),(4,5),
 (5,6);

INSERT INTO patrons(name,email) VALUES
 ('Alice Johnson','alice@example.com'),
 ('Bob Smith','bob@example.com'),
 ('Carol Nguyen','carol@example.com');

INSERT INTO book_copies(book_id, barcode) VALUES
 (1,'CPY-0001'),
 (1,'CPY-0002'),
 (2,'CPY-0003'),
 (2,'CPY-0004'),
 (3,'CPY-0005'),
 (3,'CPY-0006'),
 (4,'CPY-0007'),
 (4,'CPY-0008'),
 (5,'CPY-0009');
