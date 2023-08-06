import logging.config
import sys
import os
import json

from . import conf_set, conf_get, term_set


defaultConf = {
    "version": 1,
    "disable_existing_loggers": True,
    "loggers": {
        "": {"level": "%LEVEL%", "handlers": ["app_handler"]},
        "trace": {"level": "WARNING"},
        "lu": {"level": "INFO"},
        "urllib3": {"level": "INFO"},
        "requests": {"level": "WARNING"},
    },
    "handlers": {
        "null_handler": {"class": "logging.NullHandler"},
        "app_handler": {
            "level": "DEBUG",
            "formatter": "%FMT%",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
            "filters": ["app_name", "time", "extra"],
        },
    },
    "filters": {
        "app_name": {
            "()": "pydevkit.log.AppNameFilter",
            "threads": "no"
        },
        "time": {
            "()": "pydevkit.log.TimeFilter",
            "format": "%DATE%",
        },
        "extra": {"()": "pydevkit.log.ExtraFilter"},
    },
    "formatters": {
        "app_mini": {
            "()": "pydevkit.log.ColorLevelFormatter",
            "format": "%(clr_details)s%(time)s%(clr_reset)s :: %(appname)s :: "
                      "%(clr_level)s%(levelname)s%(clr_reset)s :: %(message)s %(extra)s",
        },
        "app": {
            "()": "pydevkit.log.ColorLevelFormatter",
            "format": "%(clr_details)s%(time)s%(clr_reset)s :: %(appname)s :: "
                      "%(clr_level)s%(levelname)-7s%(clr_reset)s :: %(message)s "
                      "%(extra)s :: %(clr_details)s%(name)s%(clr_reset)s",
        },
        "json_mini": {
            "()": "pydevkit.log.JsonFormatter",
            "format": "%(appname)s %(name)s %(levelname)s %(message)s %(extra)s",
        },
        "json": {
            "()": "pydevkit.log.JsonFormatter",
            "format": "%(time)s %(appname)s %(levelno)s %(levelname)s %(message)s %(extra)s %(name)s",
        },
    },
}


def _get_conf(kwargs):
    ovals = {
        "level": "INFO",
        "handler": "app_mini",
        "date": "datetime",
        "color": "auto",
        "threads": 'yes'
    }
    vals = dict(ovals)
    vals.update(kwargs)
    conf_set('level', vals["level"].upper())
    defaultConf["loggers"][""]["level"] = conf_get('level')
    defaultConf["handlers"]["app_handler"]["formatter"] = vals["handler"]
    if vals["handler"] == "app_mini":
        if "date" not in kwargs:
            vals["date"] = "time"
    term_set(vals["color"])

    defaultConf["filters"]["time"]["format"] = vals["date"]
    defaultConf["filters"]["app_name"]["threads"] = vals['threads']
    return defaultConf


from pydevkit.argparse import ArgumentParser


def _logging_config():
    conf_path = os.environ.get("PYDEVKIT_LOG_CONFIG", None)
    if conf_path:
        if conf_path.endswith(".json"):
            conf = json.load(open(conf_path, "r"))
            logging.config.dictConfig(conf)
        else:
            logging.config.fileConfig(conf_path)
    else:
        args = []
        for a in sys.argv[1:]:
            if a == '--':
                break
            if a.startswith('--log-'):
                args.append(a)
        p = ArgumentParser(args=args)
        Args, UnknownArgs = p.args_resolve()
        args = vars(Args)
        # print("Args", prettify(args))
        kwargs = {}
        for k, v in args.items():
            # print("Args", k, v)
            if not k.startswith("log_"):
                continue
            kwargs[k[4:]] = v

        conf = _get_conf(kwargs)
        logging.config.dictConfig(conf)


_logging_config()

# }}}
