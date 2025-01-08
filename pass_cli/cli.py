import click

from .commands.auth import auth
from .commands.auth_check import auth_check
from .commands.generate import generate
from .commands.init import init
from .commands.retrieve import retrieve
from .commands.store import store


class CustomHelpCommand(click.Group):
    def format_help(self, ctx, formatter):
        """Customize the help message."""
        formatter.write("\nA secure password manager CLI application.\n")
        formatter.write("\nCommands:\n")
        formatter.write("\n  Setup:\n")
        formatter.write("    pass-cli init        Initialize password manager\n")
        formatter.write("    pass-cli auth        Authenticate with sudo\n")
        formatter.write("    pass-cli auth-check  Check authentication status\n")
        formatter.write("\n  Password Management:\n")
        formatter.write("    pass-cli generate    Generate a secure password\n")
        formatter.write("      -l, --length       Password length (default: 12)\n")
        formatter.write("      -s, --service      Service name to store password\n")
        formatter.write("      -u, --username     Username to store password\n")
        formatter.write("      --no-copy          Show password in terminal instead of copying to clipboard\n")
        formatter.write("\n    pass-cli store        Store a password\n")
        formatter.write("      -s, --service      Service name (required)\n")
        formatter.write("      -u, --username     Username (required)\n")
        formatter.write("      -p, --password     Password (required)\n")
        formatter.write("\n    pass-cli retrieve     Retrieve a password\n")
        formatter.write("      -s, --service      Service name (required)\n")
        formatter.write("      -u, --username     Username (required)\n")
        formatter.write("\nExamples:\n")
        formatter.write("  pass-cli generate -l 16 -s github -u johndoe\n")
        formatter.write("  pass-cli store -s github -u johndoe -p mypassword\n")
        formatter.write("  pass-cli retrieve -s github -u johndoe\n")
        formatter.write("\nOptions:\n")
        formatter.write("  --help  Show this message and exit.\n")


@click.group(cls=CustomHelpCommand)
def main():
    """A secure password manager CLI application."""
    pass


main.add_command(auth)
main.add_command(auth_check)
main.add_command(generate)
main.add_command(init)
main.add_command(store)
main.add_command(retrieve)

if __name__ == "__main__":
    main()
