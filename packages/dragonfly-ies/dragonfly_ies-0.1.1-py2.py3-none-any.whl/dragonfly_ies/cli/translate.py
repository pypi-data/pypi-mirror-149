"""honeybee ies translation commands."""
import click
import sys
import pathlib
import logging

from dragonfly.model import Model

_logger = logging.getLogger(__name__)


@click.group(help='Commands for translating Dragonfly JSON files to IES files.')
def translate():
    pass


@translate.command('model-to-gem')
@click.argument('model-json', type=click.Path(
    exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option(
    '--name', '-n', help='Name of the output file.', default="model", show_default=True
)
@click.option(
    '--folder', '-f', help='Path to target folder.',
    type=click.Path(exists=False, file_okay=False, resolve_path=True,
                    dir_okay=True), default='.', show_default=True
)
@click.option('--enforce-adj-check/--bypass-adj-check', ' /-bc', help='Flag to note '
              'whether an exception should be raised if an adjacency between two '
              'Room2Ds is invalid or if the check should be bypassed and the invalid '
              'Surface boundary condition should be replaced with an Outdoor boundary '
              'condition.', default=True, show_default=True)
def model_to_gem(model_json, name, folder, enforce_adj_check):
    """Translate a Dragonfly Model JSON file to an IES GEM file.

    \b
    Args:
        model_json: Full path to a Model JSON file (DFJSON) or a Model pkl (DFpkl) file.

    """
    try:
        model = Model.from_file(model_json)
        folder = pathlib.Path(folder)
        folder.mkdir(parents=True, exist_ok=True)
        model.to_gem(folder.as_posix(), name=name, enforce_adj=enforce_adj_check)
    except Exception as e:
        _logger.exception('Model translation failed.\n{}'.format(e))
        sys.exit(1)
    else:
        sys.exit(0)
