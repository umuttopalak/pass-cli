import os
from unittest.mock import patch

import pytest
from cryptography.fernet import Fernet

from pass_cli.database import PasswordManager


@pytest.fixture
def temp_db_path(tmp_path):
    """Create temporary test database"""
    return str(tmp_path / 'test_passwords.db')

@pytest.fixture
def mock_keyring():
    """Mock keyring operations"""
    with patch('keyring.set_password') as mock_set, \
         patch('keyring.get_password') as mock_get:
        mock_set.return_value = None
        mock_get.return_value = "test_key"
        yield {'set': mock_set, 'get': mock_get}

def test_password_manager_initialization(temp_db_path, mock_keyring):
    """Test PasswordManager initialization"""
    pm = PasswordManager("test_key", db_path=temp_db_path)
    assert pm._has_encryption_key() == True

def test_store_and_retrieve_password(temp_db_path, mock_keyring):
    """Test password storage and retrieval"""
    pm = PasswordManager("test_key", db_path=temp_db_path)
    pm.store_password("github", "testuser", "testpass123")
    password = pm.get_password("github", "testuser")
    assert password == "testpass123"

def test_invalid_encryption_key(temp_db_path, mock_keyring):
    """Test invalid encryption key handling"""
    pm1 = PasswordManager("correct_key", db_path=temp_db_path)
    
    with pytest.raises(ValueError, match="Invalid encryption key"):
        pm2 = PasswordManager("wrong_key", db_path=temp_db_path)

def test_keyring_integration(temp_db_path, mock_keyring):
    """Test keyring integration"""
    pm = PasswordManager("test_key", db_path=temp_db_path)
    mock_keyring['set'].assert_called_once_with(
        PasswordManager.KEYRING_SERVICE,
        PasswordManager.KEYRING_USERNAME,
        "test_key"
    ) 