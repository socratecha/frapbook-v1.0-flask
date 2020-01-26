import sqlalchemy
from sqlalchemy import create_engine, Column, types
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import CheckConstraint
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

connection_string = "sqlite:///checksdemo.db"

db   = create_engine(connection_string)
base = declarative_base()


class Employee(base):
    __tablename__ = 'employees'
    id = Column(types.Integer, primary_key=True)
    name  = Column(types.String(length=50), nullable=False)
    skill = Column(types.String(length=20))
    assignments = relationship("Assignment", back_populates="employee")

class Project(base):
    __tablename__ = 'projects'
    id = Column(types.Integer, primary_key=True)
    name  = Column(types.String(length=50), nullable=False)
    needs = Column(types.String(length=120))
    members = relationship("Assignment", back_populates="project")
                           
class Assignment(base):
     __tablename__ = 'assignments'
     id = Column(types.Integer, primary_key=True)
     employee_id = Column(types.Integer,
                          ForeignKey('employees.id'),
                          nullable=False)
     project_id   = Column(types.Integer,
                           ForeignKey('projects.id'),
                           nullable=False)
     employee    = relationship("Employee", back_populates="assignments")
     project     = relationship("Project",  back_populates="members")
    
Session = sessionmaker(db)
session = Session()

base.metadata.create_all(db)
