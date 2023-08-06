#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2022 drad <drader@adercon.com>

import logging
from os import environ, getenv, path

import pkg_resources
import tomli

from mpbroker.config.models import UserConfigBase

logger = logging.getLogger("default")

user_config_file_name = "user_config.toml"


def env_strtobool(val: str) -> bool:
    if val in ["true", "'true'"]:
        return True
    return False


def csv_to_set(in_str: str) -> set:

    return set(map(int, in_str.split(",")))


def load_config(cfg_file: str = None) -> dict:
    """
    Load config data from toml config file
    """

    conf = {}
    try:
        with open(cfg_file, "rb") as f:
            conf = tomli.load(f)
    except FileNotFoundError as e:
        print(f"File not found: {e}")
    except Exception as e:
        print(f"Other Exception: {e}")
    return conf


APP_VERSION = pkg_resources.get_distribution("mpbroker").version
APP_NAME = pkg_resources.get_distribution("mpbroker").project_name

# get user config file (e.g. ~/.config/{APP_NAME}/{user_config_file_name)
_user_config_file = None
if environ.get("MPB_CONFIG_HOME"):
    _user_config_file = path.join(environ.get("MPB_CONFIG_HOME"), user_config_file_name)
elif environ.get("XDG_CONFIG_HOME"):
    _user_config_file = path.join(
        environ.get("XDG_CONFIG_HOME"), APP_NAME, user_config_file_name
    )
elif environ.get("APPDATA"):
    _user_config_file = path.join(
        environ.get("APPDATA"), APP_NAME, user_config_file_name
    )
else:
    _user_config_file = path.join(
        environ["HOME"], ".config", APP_NAME, user_config_file_name
    )

user_cfg = UserConfigBase.parse_obj(load_config(_user_config_file))

# ENV Based Variables
DEPLOY_ENV = getenv("DEPLOY_ENV", "prd")

# logging
LOG_TO = getenv("LOG_TO", "console").split(",")
APP_LOGLEVEL = getenv("LOG_LEVEL", "WARNING")

# List of all databases (used by db_init to ensure all are created)
DATABASES = ["media", "injest_logs"]
