from unittest.mock import patch

import pytest
from click.testing import CliRunner

from pass_cli.commands.auth import auth
from pass_cli.commands.auth_check import auth_check
from pass_cli.commands.generate import generate
from pass_cli.commands.init import init
from pass_cli.commands.retrieve import retrieve
from pass_cli.commands.store import store


@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def mock_sudo():
    """Mock sudo checks to always succeed"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 0
        yield mock_run

@pytest.fixture
def mock_keyring():
    """Mock keyring operations"""
    stored_key = "testkey"  # Use consistent key value
    with patch('keyring.set_password') as mock_set, \
         patch('keyring.get_password') as mock_get:
        mock_set.return_value = None
        mock_get.return_value = stored_key
        yield {'set': mock_set, 'get': mock_get, 'key': stored_key}

@pytest.fixture
def mock_db_path(tmp_path, monkeypatch):
    """Mock database path for commands"""
    test_db = str(tmp_path / 'test_passwords.db')
    monkeypatch.setattr('pass_cli.database.PasswordManager.DEFAULT_DB_PATH', test_db)
    return test_db

def test_init_command(runner, mock_keyring, mock_db_path):
    """Test initialization command"""
    with runner.isolated_filesystem():
        result = runner.invoke(init, input='testkey\ntestkey\n')
        assert result.exit_code == 0
        assert "Password manager initialized successfully" in result.output

def test_generate_command(runner, mock_sudo, mock_keyring, mock_db_path):
    """Test password generation command"""
    with runner.isolated_filesystem():
        # First initialize the password manager
        init_result = runner.invoke(init, input='testkey\ntestkey\n')
        assert init_result.exit_code == 0
        
        # Test basic generation with --no-copy
        result = runner.invoke(generate, ['--length', '16', '--no-copy'])
        assert result.exit_code == 0
        password = result.output.strip().split('\n')[-1]
        assert len(password) == 16
        assert any(c.islower() for c in password)
        assert any(c.isupper() for c in password)
        assert any(c.isdigit() for c in password)
        assert any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

        # Test generation with storage
        result = runner.invoke(generate, [
            '--length', '16',
            '--service', 'testservice',
            '--username', 'testuser'
        ], input=mock_keyring['key'] + '\n')
        assert result.exit_code == 0
        assert "Generated and stored password for testservice" in result.output
        assert "✓ Password copied to clipboard!" in result.output

def test_store_command(runner, mock_sudo, mock_keyring, mock_db_path):
    """Test password storage command"""
    with runner.isolated_filesystem():
        # First initialize the password manager
        init_result = runner.invoke(init, input='testkey\ntestkey\n')
        assert init_result.exit_code == 0
        
        result = runner.invoke(store, [
            '--service', 'testservice',
            '--username', 'testuser',
            '--password', 'testpass'
        ], input=mock_keyring['key'] + '\n')  # Provide encryption key as input
        assert result.exit_code == 0

def test_retrieve_command(runner, mock_sudo, mock_keyring, mock_db_path):
    """Test password retrieval command"""
    with runner.isolated_filesystem():
        # First initialize the password manager
        init_result = runner.invoke(init, input='testkey\ntestkey\n')
        assert init_result.exit_code == 0
        
        # First store the password
        store_result = runner.invoke(store, [
            '--service', 'testservice',
            '--username', 'testuser',
            '--password', 'testpass'
        ], input=mock_keyring['key'] + '\n')  # Provide encryption key as input
        assert store_result.exit_code == 0
        
        # Then retrieve it
        result = runner.invoke(retrieve, [
            '--service', 'testservice',
            '--username', 'testuser'
        ], input=mock_keyring['key'] + '\n')  # Provide encryption key as input
        assert result.exit_code == 0
        assert "testpass" in result.output

def test_auth_commands(runner, mock_sudo):
    """Test authentication commands"""
    result = runner.invoke(auth)
    assert result.exit_code == 0
    assert "Authentication successful" in result.output

    result = runner.invoke(auth_check)
    assert result.exit_code == 0
    assert "User is authenticated" in result.output 