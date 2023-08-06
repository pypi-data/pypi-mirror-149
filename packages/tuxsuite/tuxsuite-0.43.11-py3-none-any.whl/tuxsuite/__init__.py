# -*- coding: utf-8 -*-


"""
This is the tuxsuite module.
"""

__version__ = "0.43.11"


from . import build
from . import config
import logging


logging.basicConfig(format="%(levelname)s: %(message)s")


__config__ = None


def load_config():
    global __config__
    if not __config__:
        __config__ = config.Config()
    return __config__


class Configurable:
    """
    This class loads the configuration.
    """

    def __init__(self, *args, **kwargs):
        cfg = load_config()
        if "token" not in kwargs:
            kwargs["token"] = cfg.auth_token
        if "kbapi_url" not in kwargs:
            kwargs["kbapi_url"] = cfg.kbapi_url
        if "tuxapi_url" not in kwargs:
            kwargs["tuxapi_url"] = cfg.tuxapi_url
        if "group" not in kwargs:
            kwargs["group"] = cfg.group
        if "project" not in kwargs:
            kwargs["project"] = cfg.project
        super().__init__(*args, **kwargs)


class Build(Configurable, build.Build):
    """
    This class represents individual builds. It should be used to trigger
    builds, and optionally wait for them to finish.
    """


class Bitbake(Configurable, build.Bitbake):
    """
    This class represents individual builds. It should be used to trigger
    builds, and optionally wait for them to finish.
    """


class Plan(Configurable, build.Plan):
    """
    This class represent a test plan.
    """


class Test(Configurable, build.Test):
    """
    This class represents individual tests. It should be used to trigger
    tests, and optionally wait for them to finish.
    """


class Results(Configurable, build.Results):
    """
    This class represents individual results. It should be used to get results.
    """
