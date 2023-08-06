"""dragonfly-ies commands which will be added to dragonfly command line interface."""
import click
from dragonfly.cli import main

from .translate import translate


# command group for all ies extension commands.
@click.group(help='dragonfly ies commands.')
@click.version_option()
def ies():
    pass


ies.add_command(translate)

# add ies sub-commands to honeybee CLI
main.add_command(ies)
