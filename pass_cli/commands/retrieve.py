import click
import pyperclip

from ..database import PasswordManager
from ..utils import check_initialized, check_sudo


@click.command()
@click.option('--service', '-s', required=True, help='Service name')
@click.option('--username', '-u', required=True, help='Username')
@click.option('--no-copy', is_flag=True, help='Show password in terminal instead of copying to clipboard')
def retrieve(service: str, username: str, no_copy: bool) -> None:
    """Retrieve a stored password"""
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

        password = password_manager.get_password(service, username)
        if password is None:
            click.echo(click.style(
                f"✗ No password found for {service} / {username}", fg="red"))
            return

        if no_copy:
            click.echo(click.style("Retrieved password:", fg="green"))
            click.echo(password)
        else:
            pyperclip.copy(password)
            click.echo(click.style("✓ Password copied to clipboard!", fg="green"))

    except Exception as e:
        click.echo(click.style(f"✗ {str(e)}", fg="red"))
        return
