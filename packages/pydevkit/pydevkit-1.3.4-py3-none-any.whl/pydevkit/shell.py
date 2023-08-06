import subprocess as sp

import logging
log = logging.getLogger(__name__)


class Shell(object):
    def __init__(self, exe='/bin/bash'):
        self.fmt = {}
        self.exe = exe

    def __call__(self, cmd, output=False):
        cmd = cmd % self.fmt
        log.debug("shell '%s'", cmd)
        kwargs = {
            'shell': True,
            'executable': self.exe,
            'universal_newlines': True
        }
        if output:
            rc = sp.check_output(cmd, **kwargs).strip()
        else:
            rc = sp.check_call(cmd, **kwargs)
        return rc

    def inp(self, cmd):
        return self(cmd, output=True)

    def __getitem__(self, k):
        return self.fmt[k]

    def __setitem__(self, k, v):
        self.fmt[k] = v
        return v
