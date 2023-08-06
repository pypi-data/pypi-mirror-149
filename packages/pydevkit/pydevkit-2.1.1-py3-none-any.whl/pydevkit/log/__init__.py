import logging
import sys
import re
import os
import json
import datetime
import threading
from ..term import Terminal


conf = {
    'term': None
}


def conf_set(key, value):
    conf[key] = value


def conf_get(key, value=None):
    return conf.get(key, value)


def term_set(state):
    conf_set('term', Terminal(state))


def term_get():
    return conf_get('term')


class ColorLevelFormatter(logging.Formatter):
    """Logging Formatter to add colors and count warning / errors"""

    def __init__(self, *args, **kwargs):
        # print("fmt args", args)
        # print("fmt kwargs", kwargs)
        term = term_get()
        # term_print("ColorLevelFormatter")
        self.colors = {
            "DEBUG": term.cyan_dim,
            "INFO": term.grey,
            "WARNING": term.yellow,
            "ERROR": term.red_bold,
            "CRITICAL": term.red_bold_underline
        }
        if 'format' in kwargs:
            kwargs['fmt'] = kwargs['format']
            del kwargs['format']
        if 'colors' in kwargs:
            self.colors.update(kwargs['colors'])
            del kwargs['colors']
        logging.Formatter.__init__(self, *args, **kwargs)

    def format(self, record):
        term = term_get()
        record.clr_level = self.colors.get(record.levelname, '')
        record.clr_details = term.white_dim
        record.clr_reset = term.normal
        return logging.Formatter.format(self, record)


class JsonFormatter(logging.Formatter):
    """Json Formatter"""

    def __init__(self, *args, **kwargs):
        # print('='*20 + ' JsonFormatter ' + str(kwargs))
        # term_print("JsonFormatter")
        if 'format' in kwargs:
            kwargs['fmt'] = kwargs['format']
            del kwargs['format']
        reg = '%\\((?P<name>[^)]+)\\)s'
        self.props = [p.group(1) for p in re.finditer(reg, kwargs['fmt'])]
        logging.Formatter.__init__(self, *args, **kwargs)

    def format(self, record):
        # print(dir(record))
        record.message = record.msg % record.args
        rc = {}
        for a in self.props:
            rc[a] = getattr(record, a, "")
        return json.dumps(rc)


_app_name = sys.argv[0].split('/')[-1]


class AppNameFilter(logging.Filter):

    def __init__(self, name=None, threads="no"):
        self.app_name = name if name else _app_name
        self.threads = threads
        logging.Filter.__init__(self)

    def filter(self, record):
        record.appname = self.app_name
        if self.threads == "yes":
            record.appname += ':' + threading.current_thread().name
        return True


class TimeFilter(logging.Filter):
    _format = {
        "datetime": '%Y-%m-%d %H:%M:%S',
        "date": '%Y-%m-%d',
        "time": '%H:%M:%S'
    }

    def __init__(self, format="datetime"):
        self.format = self._format.get(format, format)

    def filter(self, record):
        tmp = datetime.datetime.fromtimestamp(record.created)
        tmp = tmp.strftime(self.format)
        record.time = tmp
        return True


class ExtraFilter(logging.Filter):

    def filter(self, record):
        if not hasattr(record, "extra"):
            record.extra = ""
        return True


class LogNameFilter(logging.Filter):

    def filter(self, record):
        record.logname = record.name
        pfx = "debug."
        if record.logname.startswith(pfx):
            record.logname = record.logname[len(pfx):]
        pfx = "__main__"
        if record.logname.startswith(pfx):
            record.logname = 'main' + record.logname[len(pfx):]
        return True


class AllEncoder(json.JSONEncoder):
    reg = re.compile('\\s+at\\s+[^>]+')

    def no_addr(self, s):
        return self.reg.sub('', s)

    def default(self, obj):
        if hasattr(obj, '__call__'):
            return self.no_addr(str(obj))
        elif isinstance(obj, object):
            return self.no_addr(str(obj))
        try:
            return json.JSONEncoder.default(self, obj)
        except:
            return str(obj)


def prettify(eobj):
    return json.dumps(eobj, indent=4, sort_keys=True, cls=AllEncoder)


def log_argparse(p):
    p.add_argument("--log-level",
                   help="values: %(choices)s; default is %(default)s",
                   metavar="arg",
                   choices=['debug', 'info', 'warning', 'error', 'critical'],
                   default=os.environ.get('PYDEVKIT_LOG_LEVEL', "info"))
    p.add_argument("--log-color",
                   help="values: %(choices)s; default is %(default)s",
                   metavar="arg",
                   choices=['auto', 'yes', 'no'],
                   default=os.environ.get('PYDEVKIT_LOG_COLOR', "auto"))
    p.add_argument("--log-handler",
                   help="values: %(choices)s; default is %(default)s",
                   metavar="arg",
                   choices=['app', 'app_mini', 'json', 'json_mini'],
                   default=os.environ.get('PYDEVKIT_LOG_HANDLER', "app_mini"))
    p.add_argument("--log-date",
                   help="values: predefined formats: 'datetime', 'date', 'time'"
                        " or strftime format eg '%%Y-%%m-%%d'",
                   metavar="arg",
                   default=os.environ.get('PYDEVKIT_LOG_DATE', "datetime"))
    p.add_argument("--log-threads",
                   help="values: %(choices)s; default is %(default)s",
                   metavar="arg",
                   choices=['yes', 'no'],
                   default=os.environ.get('PYDEVKIT_LOG_THREADS', "no"))
