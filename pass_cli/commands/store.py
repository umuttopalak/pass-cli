import os

import click

from ..database import PasswordManager
from ..utils import check_sudo


@click.command()
@click.option('--service', '-s', required=True, help='Service name')
@click.option('--username', '-u', required=True, help='Username')
@click.option('--password', '-p', required=True, help='Password to store')
def store(service: str, username: str, password: str):
    """Store a password for a service"""
    if not check_sudo():
        click.echo(click.style("✗ Authentication required! Please run 'pass-cli auth' first.", fg="red"))
        raise click.Abort()

    try:
        master_password = click.prompt('Enter master password', hide_input=True)
        pm = PasswordManager(master_password)
        pm.store_password(service, username, password)
        click.echo(click.style(f"Password stored successfully for {service}", fg="green"))
    except ValueError as e:
        click.echo(click.style(f"Error: {str(e)}", fg="red"))
    except Exception as e:
        click.echo(click.style(f"Error storing password: {str(e)}", fg="red"))
