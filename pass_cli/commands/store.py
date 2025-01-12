import os

import click

from ..database import PasswordManager
from ..utils import check_initialized, check_sudo


@click.command()
@click.option('--service', '-s', required=True, help='Service name')
@click.option('--username', '-u', required=True, help='Username')
@click.option('--password', '-p', required=True, help='Password to store')
def store(service: str, username: str, password: str) -> None:
    """Store a password for a service"""
    if not check_sudo():
        click.echo(click.style(
            "✗ Authentication required! Please run 'pass-cli auth' first.", fg="red"))
        return

    if not check_initialized():
        click.echo(click.style(
            "✗ Password manager not initialized! Please run 'pass-cli init' first.", 
            fg="red"))
        return

    try:
        encryption_key = PasswordManager.get_stored_key()
        if not encryption_key:
            click.echo(click.style(
                "✗ No encryption key found! Please run 'pass-cli init' first.", fg="red"))
            return

        password_manager = PasswordManager(encryption_key)
        password_manager.store_password(service, username, password)
        click.echo(click.style("✓ Password stored successfully!", fg="green"))

    except Exception as e:
        click.echo(click.style(f"✗ {str(e)}", fg="red"))
        return
