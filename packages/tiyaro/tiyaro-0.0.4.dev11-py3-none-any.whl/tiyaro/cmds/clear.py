import os
import shutil

import click

from ..common.constants import *
from ..common.utils import success, warn


@click.command()
@click.option('-f', '--force', is_flag=True, help=CLEAR_HELP)
@click.option('-v', '--verbose', is_flag=True, default=False, help=VERBOSE_HELP)
def clear(force, verbose):
    """
    - Forcefully clears all tiyaro generated files
    """
    if not force:
        warn('No action taken.  Run using -f flag')
        exit(-1)
    do_clear(verbose)


def do_clear(is_verbose):
    took_action = False
    if (os.path.isdir(TIYARO_HANDLER_DIR)):
        shutil.rmtree(TIYARO_HANDLER_DIR)
        took_action = True

    if (os.path.isfile(HANDLER_MODEL_MODEL_TEST_FILE)):
        os.remove(HANDLER_MODEL_MODEL_TEST_FILE)
        took_action = True

    if took_action:
        success(
            f'Cleared {TIYARO_HANDLER_DIR}, {HANDLER_MODEL_MODEL_TEST_FILE} templates', is_verbose)
