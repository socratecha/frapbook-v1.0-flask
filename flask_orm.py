import sqlalchemy
from sqlalchemy import create_engine, Column, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import CheckConstraint
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

connection_string = "postgresql://localhost:5432/books"   # Postgres books DB
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
    birth_year = Column(types.Integer,
                        CheckConstraint('birth_year < 2020'),
                        nullable=False)
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
newbook = Book(author="Annie Dillard", title="Teaching a Stone to Talk", available=True)
session.add(newbook)
session.commit()
newyear = BirthYear(author="Perfect Vision", birth_year=2020)
session.add(newyear)
try:
    session.commit()
except sqlalchemy.exc.IntegrityError as e:
    print("Integrity violation blocked!")
    session.rollback()
