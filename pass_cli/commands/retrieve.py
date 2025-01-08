import os

import click

from ..database import PasswordManager
from ..utils import check_sudo


@click.command()
@click.option('--service', '-s', required=True, help='Service name')
@click.option('--username', '-u', required=True, help='Username')
def retrieve(service: str, username: str):
    """Retrieve a password for a service"""
    if not check_sudo():
        click.echo(click.style("✗ Authentication required! Please run 'pass-cli auth' first.", fg="red"))
        raise click.Abort()

    try:
        master_password = click.prompt('Enter master password', hide_input=True)
        pm = PasswordManager(master_password)
        password = pm.get_password(service, username)
        
        if password:
            click.echo(click.style(f"Password for {service}:", fg="green"))
            click.echo(password)
        else:
            click.echo(click.style(f"No password found for {service} with username {username}", fg="yellow"))
    except ValueError as e:
        click.echo(click.style(f"Error: {str(e)}", fg="red"))
    except Exception as e:
        click.echo(click.style(f"Error retrieving password: {str(e)}", fg="red"))
