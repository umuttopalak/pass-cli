import click
import pyperclip

from ..database import PasswordManager
from ..utils import check_initialized, check_sudo, generate_strong_password


@click.command()
@click.option('--length', '-l', type=int, default=12, help='Password length (default: 12)')
@click.option('--service', '-s', help='Service name to store the password')
@click.option('--username', '-u', help='Username to store the password')
@click.option('--no-copy', is_flag=True, help='Show password in terminal instead of copying to clipboard')
def generate(length: int, service: str, username: str, no_copy: bool) -> None:
    """Generate a secure random password"""
    if service and not check_sudo():
        click.echo(click.style(
            "✗ Authentication required! Please run 'pass-cli auth' first.", fg="red"))
        return

    if service and not check_initialized():
        click.echo(click.style(
            "✗ Password manager not initialized! Please run 'pass-cli init' first.", 
            fg="red"))
        return

    try:
        password = generate_strong_password(length)

        if service and username:
            encryption_key = PasswordManager.get_stored_key()
            if not encryption_key:
                click.echo(click.style(
                    "✗ No encryption key found! Please run 'pass-cli init' first.", fg="red"))
                return

            password_manager = PasswordManager(encryption_key)
            password_manager.store_password(service, username, password)
            click.echo(click.style(
                f"✓ Generated and stored password for {service}", fg="green"))

        if no_copy:
            click.echo(click.style("Generated password:", fg="green"))
            click.echo(password)
        else:
            pyperclip.copy(password)
            click.echo(click.style("✓ Password copied to clipboard!", fg="green"))

    except Exception as e:
        click.echo(click.style(f"✗ {str(e)}", fg="red"))
        return
