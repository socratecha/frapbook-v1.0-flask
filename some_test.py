import json
import pytest

from flask_app import app

def test_arithmetic():
    '''Placeholder test to see how tests works with pytest.'''

    x = 17
    assert 3*x == 51, 'Math is broken!'
    # assert True == False, 'Surprise!'    
def some_function(i):
    '''For demonstration purposes, raises a IndexError'''
    a = [1,2,3]
    return a[i]
    
def test_some_function():
    '''Test that some_function works and also raises a IndexError'''
    assert some_function(1) == 2
    with pytest.raises(IndexError) as e:
        x = some_function(10)

@pytest.fixture(scope='module')
def test_app():
    '''Uses ``app`` imported from flask_app to create a testable Flask
    application.

    :yield: Flask application with a context, ready for testing
    '''
    # Uses global variable "app"
    app.config['TESTING'] = True
    test_app = app.test_client() 
    ctx = app.app_context()
    ctx.push()
    yield test_app 
    ctx.pop()

def test_myapi_get(test_app):
    '''Using a ``test_app`` as a fixture, test its response on a GET
    request
    '''
    response = test_app.get('/my-api')
    assert response.status_code == 200

    data = json.loads(response.data.decode())
    assert isinstance(data, list)
    for datum in data:
        assert isinstance(datum, dict) and set(datum.keys()) == {'id', 'number', 'description'}

def test_myapi_id_get(test_app):
    '''Using ``test_app`` fixture, check response on a GET request
    '''
    response = test_app.get('/my-api/2')
    assert response.status_code == 200

    data = json.loads(response.data.decode())
    assert isinstance(data, dict)
    assert isinstance(data['number'], int)

def test_myapi_post(test_app):
    '''Using ``test_app`` fixture, check response on a POST request
    '''    
    response = test_app.post(
        '/my-api',
        data=json.dumps({
            "number":1729,
            "description":"First taxi-cab number"}),
        headers = {'Content-Type': 'application/json',
                   'Accept': 'application/json'}
    )
    assert response.status_code == 200

    data = json.loads(response.data.decode())
    assert isinstance(data, int)
