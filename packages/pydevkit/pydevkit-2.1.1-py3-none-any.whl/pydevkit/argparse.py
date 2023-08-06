
import argparse
import sys
from pydevkit.log import prettify
from pydevkit.log import log_argparse

import logging
log = logging.getLogger(__name__)


def ArgumentParser(_help=None, args=None, app_name=None):
    if app_name is None:
        app_name = sys.argv[0].split('/')[-1]
    if _help is None:
        _help = ""
    tmp = _help.split('\nEPILOG:\n')
    app_help = tmp[0]
    app_epilog = tmp[1] if len(tmp) == 2 else ''

    p = argparse.ArgumentParser(
        prog=app_name,
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=app_help,
        epilog=app_epilog)
    # p.add_argument("--debug", help="debug mode", action="store_true")
    log_argparse(p)

    def args_resolve(self, args=args):
        Args, UnknownArgs = self.parse_known_args(args)
        log.debug("Args: %s", prettify(vars(Args)))
        if UnknownArgs:
            log.debug("Not all arguments were parsed: '%s'", UnknownArgs)
            if UnknownArgs[0] == '--':
                del UnknownArgs[0]
        log.debug("UnknownArgs: %s", UnknownArgs)
        return Args, UnknownArgs

    p.args_resolve = args_resolve.__get__(p)
    return p
