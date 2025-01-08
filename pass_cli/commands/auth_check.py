import click

from ..utils import check_initialized, check_sudo


@click.command()
def auth_check():
    """Check if user is authenticated with sudo privileges"""
    if not check_initialized():
        click.echo(click.style("Password manager not initialized. Please run 'pass-cli init' first.", fg="red"))
        raise click.Abort()

    if check_sudo():
        click.echo(click.style("✓ User is authenticated", fg="green"))
    else:
        click.echo(click.style("✗ User is not authenticated", fg="red"))
