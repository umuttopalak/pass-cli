import click

from ..database import PasswordManager
from ..utils import check_initialized, check_sudo


@click.command()
@click.option('--service', '-s', required=True, help='Service name')
@click.option('--username', '-u', required=True, help='Username')
@click.option('--force', '-f', is_flag=True, help='Skip confirmation')
def delete(service: str, username: str, force: bool) -> None:
    """Delete a stored password"""
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

        if not password_manager.get_password(service, username):
            click.echo(click.style(
                f"✗ No password found for {service} / {username}", fg="red"))
            return

        if not force:
            confirm = click.confirm(
                f"Are you sure you want to delete the password for {service} / {username}?",
                abort=True
            )

        password_manager.delete_password(service, username)
        click.echo(click.style("✓ Password deleted successfully!", fg="green"))

    except click.Abort:
        click.echo(click.style("Operation cancelled.", fg="yellow"))
        return
    except Exception as e:
        click.echo(click.style(f"✗ {str(e)}", fg="red"))
        return 