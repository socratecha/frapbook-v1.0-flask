from sqlalchemy import create_engine, Column, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

connection_string = "sqlite:///database.db"

db   = create_engine(connection_string)
base = declarative_base()

class Book(base):
    __tablename__ = 'books'
    id = Column(types.Integer, primary_key=True)
    author = Column(types.String(length=50))
    title = Column(types.String(length=120), nullable=False)
    available = Column(types.Boolean, nullable=False)

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

# Create 
book1 = Book(author="Kurt Vonnegut", title="Player Piano", available=True)
session.add(book1)               # add one book

session.add_all([                # add a list of books
    Book(author="Annie Dillard", title="Pilgrim at Tinker Creek", available=False),
    Book(author="Lewis Carroll", title="Alice in Wonderland", available=True),
    Book(author="Kurt Vonnegut", title="Sirens of Titan", available=True),
])
session.commit()

# Read
for book in session.query(Book):
    print(book.id, book.title)

# Update
book1.available = True
session.commit()

# Delete
session.delete(book1)
session.commit()

print('Which books are available to be checked out?')
for book in session.query(Book).filter(Book.available == True):
    print(book.title, book.author)

print('Are there any Vonnegut books available?')
Q = session.query(Book).filter(Book.available == True, Book.author == 'Kurt Vonnegut')
for book in Q:
    print(book.title, book.author)

Q2 = session.query(Book.id, Book.author).filter(Book.id != 1).all()
print(Q2[0])
print(Q2[0].author)

class BirthYear(base):
    __tablename__ = 'birth_years'
    author = Column(types.String(length=50), primary_key=True)
    birth_year = Column(types.Integer, nullable=False)

# Add the new table to the database
base.metadata.create_all(db)

session.add_all([
    BirthYear(author='Lewis Carroll', birth_year=1832),
    BirthYear(author='Kurt Vonnegut', birth_year=1922),
    BirthYear(author='Annie Dillard', birth_year=1945)
])

for birthyear,book in session.query(BirthYear, Book):
    print(birthyear.author, birthyear.birth_year, book.id, book.author, book.title, book.available)

Q = session.query(BirthYear, Book).filter(BirthYear.author == Book.author)
for birthyear,book in Q:
    print(birthyear.author, birthyear.birth_year, book.id, book.author, book.title, book.available)

Q = session.query(BirthYear, Book).filter(
    BirthYear.author == Book.author,
    BirthYear.birth_year > 1900,
    Book.available == True
)
for birthyear,book in Q:
    print(birthyear.author, birthyear.birth_year, book.id, book.author, book.title, book.available)
