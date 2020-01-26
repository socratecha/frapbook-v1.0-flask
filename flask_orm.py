from sqlalchemy import create_engine, Column, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

connection_string = "sqlite:///database.db"   # for SQLite, local file
db   = create_engine(connection_string)
base = declarative_base()

class Book(base):
    __tablename__ = 'books'
    id = Column(types.Integer, primary_key=True)
    author = Column(types.String(length=50))
    title = Column(types.String(length=120), nullable=False)
    available = Column(types.Boolean, nullable=False)

class BirthYear(base):
    __tablename__ = 'birth_years'
    author = Column(types.String(length=50), primary_key=True)
    birth_year = Column(types.Integer, nullable=False)

Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)

# Create
session.add_all([                # add a list of books
    Book(author="Annie Dillard", title="Pilgrim at Tinker Creek", available=False),
    Book(author="Lewis Carroll", title="Alice in Wonderland", available=True),
    Book(author="Kurt Vonnegut", title="Sirens of Titan", available=True),
    Book(author="Seymour Hersh", title="The Price of Power", available=False),
])

session.add_all([
    BirthYear(author="Lewis Carroll", birth_year=1832),
    BirthYear(author="Kurt Vonnegut", birth_year=1922),
    BirthYear(author="Seymour Hersh", birth_year=1937),
    BirthYear(author="Annie Dillard", birth_year=1945),
])
session.commit()
session.add(Book(author="Seymour M. Hersh", title="Chain of Command", available=False))
session.commit()
Q = session.query(BirthYear, Book).filter(
    Book.title == "Chain of Command", 
    BirthYear.author == Book.author,
)
books = Q.all()
print('Found {} books'.format(len(books)))
