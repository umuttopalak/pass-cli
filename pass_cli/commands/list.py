import sys

import click

from ..database import PasswordManager
from ..utils import check_initialized, check_sudo


@click.command()
@click.option('--service', '-s', help='Filter passwords by service name')
def list(service: str = None) -> None:
    """List saved passwords for all or specific service"""
    try:
        if not check_sudo():
            click.echo(click.style(
                "✗ Authentication required! Please run 'pass-cli auth' first.", fg="red"))
            sys.exit(1)

        if not check_initialized():
            click.echo(click.style(
                "✗ Password manager not initialized! Please run 'pass-cli init' first.", 
                fg="red"))
            raise click.Abort()

        # Get encryption key and initialize password manager
        password_manager = PasswordManager(PasswordManager.get_stored_key())
        
        # Get stored passwords
        stored_passwords = password_manager.list_passwords(service)
        
        if not stored_passwords:
            if service:
                click.echo(click.style(
                    f"No passwords found for service: {service}", fg="yellow"))
            else:
                click.echo(click.style("No passwords stored yet.", fg="yellow"))
            return

        # Display results
        click.echo(click.style("\nStored Passwords:", fg="green"))
        click.echo("─" * 50)
        for service_name, username in stored_passwords:
            click.echo(f"Service: {service_name}")
            click.echo(f"Username: {username}")
            click.echo("─" * 50)
    except Exception as e:
        click.echo(click.style(f"Error: {str(e)}", fg="red"))
        raise click.Abort()
