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

standard_skills = ['designer', 'client', 'server', 'db_admin']

class Employee(base):
    __tablename__ = 'employees'
    id = Column(types.Integer, primary_key=True)
    name  = Column(types.String(length=50), nullable=False)
    skill = Column(types.String(length=20))
    assignments = relationship("Assignment", back_populates="employee")

    def needless_assignments(self):
        return [assignment for assignment in self.assignments
                if self.skill not in assignment.project.needs.split()]

class Project(base):
    __tablename__ = 'projects'
    id = Column(types.Integer, primary_key=True)
    name  = Column(types.String(length=50), nullable=False)
    needs = Column(types.String(length=120))
    members = relationship("Assignment", back_populates="project")
                           
    def nonstandard_needs(self):
        return [need for need in self.needs.split()
                if need not in standard_skills]

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
def add_sample_data():
    # Add employees and projects; assign employees to projects
    session.add_all([
        Employee(id=1, name="Hercules the Bear", skill="client"),
        Employee(id=2, name="Herman Hollerith", skill="db_admin"),
        Employee(id=3, name="Martina Hingis", skill="server"),
        Employee(id=4, name="Margo Hoff", skill="designer"),
        Employee(id=5, name="Hulk Hogan"),
        Project(id=1, name="Design Transmogrifier",
                needs='designer server'),
        Project(id=2, name="Build Duplicator", needs='client db_admin'),
        Project(id=3, name="Repair Enhance-o-Tron",
                needs='client juggler'),
        Assignment(employee_id=1, project_id=2),
        Assignment(employee_id=2, project_id=2),
        Assignment(employee_id=3, project_id=3),
        Assignment(employee_id=4, project_id=1),
    ])
    session.commit()

def clean_data():
    for project in session.query(Project).all():
        nonstandards = project.nonstandard_needs()
        if nonstandards:
            print('Project {} requires non-standard skill: {}'.format(
                project.name, ', '.join(nonstandards)))
            standards = [need for need in project.needs.split()
                         if need in standard_skills]
            project.needs = ' '.join(standards)   # update the object
            session.commit()                      # update the database
            print('Nonstandard skills removed')
    for employee in session.query(Employee).all():
        extra_projects = employee.needless_assignments()
        if extra_projects:
            print('Employee {} should not be on projects: {}'.format(
                employee.name, ', '.join([assignment.project.name
                                          for assignment in extra_projects])))
            for assignment in extra_projects:
                session.delete(assignment)
            session.commit()
            print('Extraneous assignments deleted')
def drop_tables():
    for Table in [Employee, Project, Assignment]:
        session.query(Table).delete()
if __name__ == '__main__':
    add_sample_data()
    clean_data()
