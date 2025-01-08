# pass-cli

[![Tests](https://github.com/umuttopalak/pass-cli/actions/workflows/test.yml/badge.svg)](https://github.com/umuttopalak/pass-cli/actions/workflows/test.yml)
[![PyPI version](https://badge.fury.io/py/password-cli.svg)](https://badge.fury.io/py/password-cli)
[![Python versions](https://img.shields.io/pypi/pyversions/password-cli.svg)](https://pypi.org/project/password-cli/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A secure command-line password manager with sudo authentication.

## Features

- Secure password storage with AES-256 encryption
- Generate strong random passwords
- Store and retrieve passwords for different services
- Sudo authentication for added security
- Secure encryption key management
- System keyring integration

## Installation

```bash
pip install password-cli
```

## Quick Start

1. Initialize the password manager:
```bash
pass-cli init
```
This will prompt you to set up your encryption key or generate a secure random one.

2. Authenticate with sudo:
```bash
pass-cli auth
```

## Usage

### Generate Passwords

Generate a random secure password:
```bash
pass-cli generate -l 16
```

Generate and store a password:
```bash
pass-cli generate -l 16 -s github -u johndoe
```

### Store Passwords

Store an existing password:
```bash
pass-cli store -s github -u johndoe -p your-password
```

### Retrieve Passwords

Retrieve a stored password:
```bash
pass-cli retrieve -s github -u johndoe
```

### Check Authentication

Check sudo authentication status:
```bash
pass-cli auth-check
```

## Security Features

- AES-256 encryption for all stored passwords
- PBKDF2 key derivation with high iteration count
- Secure random password generation using `secrets` module
- System keyring integration for encryption key storage
- Sudo authentication requirement for all operations
- Local storage only - no cloud sync for enhanced security

## Development Setup

1. Clone the repository:
```bash
git clone https://github.com/yourusername/pass-cli.git
cd pass-cli
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. Run tests:
```bash
pytest
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Click](https://click.palletsprojects.com/)
- Uses [cryptography](https://cryptography.io/) for secure encryption
- Integrates with system keyring using [keyring](https://pypi.org/project/keyring/)