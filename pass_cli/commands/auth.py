import subprocess

import click

from ..utils import check_initialized


@click.command()
def auth():
    """Authenticate user with sudo privileges"""
    if not check_initialized():
        click.echo(click.style("Password manager not initialized. Please run 'pass-cli init' first.", fg="red"))
        raise click.Abort()

    try:
        subprocess.run(["sudo", "-v"], check=True)
        click.echo(click.style("✓ Authentication successful!", fg="green"))
    except subprocess.CalledProcessError:
        click.echo(click.style("✗ Authentication failed!", fg="red"))
        raise click.Abort()
