import secrets
import string

import click

from ..database import PasswordManager
from ..utils import check_initialized, generate_strong_password


@click.command()
def init():
    """Initialize the password manager"""
    try:
        if check_initialized():
            click.echo(click.style(
                "✗ Password manager is already initialized!", fg="yellow"))
            return

        encryption_key = click.prompt(
            "Enter encryption key (or press Enter to generate one)", 
            default='', 
            hide_input=True
        )

        if not encryption_key:
            encryption_key = generate_strong_password(is_encryption_key=True)
            click.echo(click.style(
                "Generated secure encryption key.", fg="green"))

        PasswordManager(encryption_key)
        click.echo(click.style("✓ Password manager initialized successfully!", fg="green"))

    except Exception as e:
        click.echo(click.style(f"✗ {str(e)}", fg="red"))
        return 