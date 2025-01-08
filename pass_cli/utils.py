import secrets
import string
import subprocess

from .database import PasswordManager


def check_sudo():
    """Check if user has sudo privileges"""
    try:
        subprocess.run(["sudo", "-n", "true"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False


def check_initialized():
    """Check if password manager is initialized"""
    try:
        pm = PasswordManager()
        return pm._has_encryption_key()
    except Exception:
        return False


def generate_strong_password(length: int = 16, is_encryption_key: bool = False) -> str:
    """Generate a strong random password or encryption key

    Args:
        length: Length of the password/key
        is_encryption_key: If True, uses 64 characters for encryption key
    """
    if is_encryption_key:
        length = 64

    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    special = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    password = [
        secrets.choice(lowercase),
        secrets.choice(uppercase),
        secrets.choice(digits),
        secrets.choice(special)
    ]

    all_characters = lowercase + uppercase + digits + special
    password.extend(secrets.choice(all_characters) for _ in range(length - 4))

    password = list(password)
    secrets.SystemRandom().shuffle(password)

    return ''.join(password)
