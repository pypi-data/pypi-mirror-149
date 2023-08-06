import sys

import logging
log = logging.getLogger(__name__)


class Terminal:

    color_codes = {
        "black": "0",
        "red": "1",
        "green": "2",
        "yellow": "3",
        "blue": "4",
        "magenta": "5",
        "cyan": "6",
        "white": "7"
    }

    tone_codes = {
        "normal": "0",
        "bold": "1",
        "dim": "2",
        "italic": "3",
        "underline": "4",
        "blink": "5",
        "blink2": "6",
        "reverse": "7",
        "hide": "8",
        "overstrike": "9"
    }

    def __init__(self, colors="auto"):
        if colors == 'auto':
            colors = "yes" if sys.stderr.isatty() else "no"
        self.colors = colors

    def __getattr__(self, name):
        # log.debug("term: attr %s", name)
        if self.colors != "yes":
            return ""
        cflag = "fg"
        rc = []
        for n in name.split('_'):
            if n == 'on':
                cflag = "bg"
                continue
            if n in self.color_codes:
                pfx = "3" if cflag == "fg" else "4"
                rc.append(pfx + self.color_codes[n])
                cflag = "fg"
                continue
            if n in self.tone_codes:
                rc.append(self.tone_codes[n])

        if rc:
            return '\x1b[' + ';'.join(rc) + 'm'
        return ""
