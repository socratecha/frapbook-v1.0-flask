import pytest

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
