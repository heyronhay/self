import os
import pytest

'''
For pytest, conftest.py sets up fixtures that can be used by tests
'''
@pytest.fixture
def testdir():
    return os.path.dirname(os.path.abspath(__file__))
