import os
from unittest.mock import patch

import pytest

from pass_cli.commands.init import init


@pytest.fixture(autouse=True)
def setup_test_env():
    """Set up test environment"""
    os.environ['TESTING'] = 'true'
    yield
    os.environ.pop('TESTING', None)


@pytest.fixture
def initialized_db(runner, mock_keyring, mock_db_path, mock_sudo):
    """Fixture that provides an initialized database"""
    with runner.isolated_filesystem():
        # Initialize the password manager
        init_result = runner.invoke(init, input='testkey\ntestkey\n')
        assert init_result.exit_code == 0
        yield


@pytest.fixture
def mock_sudo_fail():
    """Mock sudo checks to always fail"""
    with patch('subprocess.run') as mock_run:
        mock_run.return_value.returncode = 1
        yield mock_run
