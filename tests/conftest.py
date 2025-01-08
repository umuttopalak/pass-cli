import os

import pytest


@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment"""
    os.environ['TESTING'] = 'true'
    yield
    os.environ.pop('TESTING', None) 
    
