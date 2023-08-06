"""
Kortical Software Development Kit

usage:
    kortical <command> [<args>...] [-hv]

options:
    -h, --help     Display help.
    -v, --version  Display version.

Commands:
    config        Manage Kortical config.
    app           Manage Kortical Cloud apps.
    docker        Manage Docker images.
    secret        Manage Kortical secrets.
    storage       Manage Kortical Cloud storage.

For more information on a command, run `kortical <cmd> --help`.
"""

import logging
import os
import sys
import warnings

from docopt import docopt
from docopt import DocoptExit

warnings.filterwarnings('ignore')

from . import _cmd_registry

# If you add a module containing commands, you must import it here for
# it to have any effect. Include the "# NOQA" comment to prevent
# flake8 warning about the unused import.
from . import _config  # NOQA
from . import _app     # NOQA
from . import _docker  # NOQA
from . import _storage # NOQA
from . import _secret  # NOQA


def disable_logging():
    logging.disable(logging.DEBUG)
    logging.disable(logging.INFO)
    logging.disable(logging.WARNING)
    logging.disable(logging.ERROR)
    logging.disable(logging.CRITICAL)


def get_version():
    script_dir = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(script_dir, "../VERSION")) as f:
        return f.read().strip()


def handle_args(args):
    cmd = _cmd_registry.get_command(args['<command>'])
    if cmd is None:
        print(f"kortical: Unrecognised command [{args['<command>']}]", file=sys.stderr)
        raise DocoptExit()
    return cmd()


def main():
    warnings.filterwarnings('ignore')
    disable_logging()
    args = docopt(__doc__, version=get_version(), options_first=True)
    return handle_args(args)


if __name__ == '__main__':
    main()
