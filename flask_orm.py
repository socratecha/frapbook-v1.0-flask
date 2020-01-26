import sqlalchemy
from sqlalchemy import create_engine, Column, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

connection_string = "sqlite:///database.db"   # for SQLite, local file
db   = create_engine(connection_string)
base = declarative_base()

class Book(base):
    __tablename__ = 'books'
    id = Column(types.Integer, primary_key=True)
    author = Column(types.String(length=50), ForeignKey('birth_years.author'), nullable=False)
    title = Column(types.String(length=120), nullable=False)
    available = Column(types.Boolean, nullable=False)
    birth_year = relationship("BirthYear", back_populates="books")

class BirthYear(base):
    __tablename__ = 'birth_years'
    author = Column(types.String(length=50), primary_key=True)
    birth_year = Column(types.Integer, nullable=False)
    books = relationship("Book", back_populates="birth_year")

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
newbook = Book(author="Seymour M. Hersh", title="Chain of Command", available=False)
session.execute('pragma foreign_keys=on')    # keeping SQLite honest
session.add(newbook)
try:
    session.commit()
    print('Success!')
except sqlalchemy.exc.IntegrityError as e:
    print('Failed with "{}" error message'.format(e.orig))
    session.rollback()
