import json
import pytest
from flask_orm2 import drop_tables, add_sample_data, clean_data
from flask_orm2 import Employee, Project, Assignment, session

@pytest.fixture(scope='module')
def db_session_clean():
    '''Creates a database and populates it with clean data'''
    drop_tables()       # drop tables, but keep schema
    add_sample_data()   # populate uncleanly
    clean_data()        
    yield session
    
def test_clean_nonstandard_skills(db_session_clean):
    '''Check project required skills are from the standard list'''
    for project in db_session_clean.query(Project).all():
        assert not project.nonstandard_needs()

def test_clean_needless_assignments(db_session_clean):
    '''Check that everyone is on a project where they can contribute'''
    for employee in db_session_clean.query(Employee).all():
        assert not employee.needless_assignments()

