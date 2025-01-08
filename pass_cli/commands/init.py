import secrets
import string

import click

from ..database import PasswordManager
from ..utils import generate_strong_password


@click.command()
def init():
    """Initialize the password manager with an encryption key.
    
    If no key is entered, a secure random key will be generated.
    Make sure to save your encryption key - it cannot be recovered!
    """
    try:
        if PasswordManager()._has_encryption_key():
            click.echo(click.style("Password manager is already initialized", fg="yellow"))
            return

        click.echo("Enter encryption key (press Enter for a random secure key)")
        key = click.prompt('Encryption key', hide_input=True, default='', show_default=False)
        
        if not key:
            key = generate_strong_password(is_encryption_key=True)
            click.echo(click.style("\nGenerated encryption key:", fg="green"))
            click.echo(click.style(key, fg="yellow"))
            click.echo(click.style("\n⚠️  IMPORTANT: Save this encryption key securely! You won't be able to recover it!", fg="red"))
        else:
            confirm = click.prompt('Confirm encryption key', hide_input=True)
            if key != confirm:
                click.echo(click.style("Error: Keys do not match", fg="red"))
                raise click.Abort()
        
        pm = PasswordManager(key)
        click.echo(click.style("\nPassword manager initialized successfully", fg="green"))
    except Exception as e:
        click.echo(click.style(f"Error initializing password manager: {str(e)}", fg="red")) 