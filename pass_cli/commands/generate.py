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
    if not check_sudo():
        click.echo(click.style("✗ Authentication required! Please run 'pass-cli auth' first.", fg="red"))
        raise click.Abort()

    if length < 8:
        click.echo(click.style("Warning: Password length should be at least 8 characters", fg="yellow"))
        return

    final_password = generate_strong_password(length=length)

    if service and username:
        try:
            if not check_initialized():
                click.echo(click.style("Password manager not initialized. Please run 'pass-cli init' first.", fg="red"))
                raise click.Abort()

            stored_key = PasswordManager.get_stored_key()
            if not stored_key:
                encryption_key = click.prompt('Enter encryption key', hide_input=True)
            else:
                encryption_key = stored_key

            try:
                pm = PasswordManager(encryption_key)
                pm.store_password(service, username, final_password)
                click.echo(click.style(f"Generated and stored password for {service}", fg="green"))
            except ValueError:
                click.echo(click.style("Invalid encryption key", fg="red"))
                raise click.Abort()
        except Exception as e:
            click.echo(click.style(f"Error storing password: {str(e)}", fg="red"))
            raise click.Abort()

    if no_copy:
        # Show password in terminal if --no-copy is used
        click.echo(click.style("Generated password:", fg="green"))
        click.echo(final_password)
    else:
        # Only copy to clipboard by default
        pyperclip.copy(final_password)
        click.echo(click.style("✓ Password copied to clipboard!", fg="green"))
