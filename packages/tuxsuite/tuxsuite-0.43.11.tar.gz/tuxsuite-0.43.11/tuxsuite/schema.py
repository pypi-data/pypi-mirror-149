# -*- coding: utf-8 -*-

from voluptuous import Any, Optional, Required, Schema


def plan():
    return Schema(
        {
            Required("version"): 1,
            Optional("name"): str,
            Optional("description"): str,
            Required("jobs"): [
                Any(
                    {Required("build"): dict},
                    {Required("build"): dict, Required("test"): dict},
                    {Required("build"): dict, Required("tests"): list},
                    {Required("builds"): list},
                    {Required("builds"): list, Required("test"): dict},
                    {Required("builds"): list, Required("tests"): list},
                    {Required("tests"): list},
                    {Required("test"): dict},
                )
            ],
        }
    )
