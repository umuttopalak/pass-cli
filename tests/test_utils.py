import subprocess
from unittest.mock import patch

import pytest

from pass_cli.utils import (check_initialized, check_sudo,
                            generate_strong_password)


def test_check_sudo_success():
    """Test successful sudo check"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        assert check_sudo() == True

def test_check_sudo_failure():
    """Test failed sudo check"""
    with patch('subprocess.run') as mock_run:
        mock_run.side_effect = subprocess.CalledProcessError(1, "sudo")
        assert check_sudo() == False

def test_check_initialized():
    """Test initialization check"""
    with patch('pass_cli.database.PasswordManager._has_encryption_key') as mock_has_key:
        mock_has_key.return_value = True
        assert check_initialized() == True
        
        mock_has_key.return_value = False
        assert check_initialized() == False

def test_generate_strong_password():
    """Test password generation"""
    # Test normal password
    password = generate_strong_password(length=16)
    assert len(password) == 16
    assert any(c.islower() for c in password)
    assert any(c.isupper() for c in password)
    assert any(c.isdigit() for c in password)
    assert any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

    # Test encryption key
    key = generate_strong_password(is_encryption_key=True)
    assert len(key) == 64 