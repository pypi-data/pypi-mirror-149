#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2022 drad <drader@adercon.com>

from typing import List

from pydantic import BaseModel


class UserConfigDefaults(BaseModel):
    """
    Defaults for UserConfig.
    """

    source: str = None
    user: str = None


class UserConfigInjest(BaseModel):
    """
    User Config Injest.
    """

    file_types: List[str] = None


class UserConfigDatabase(BaseModel):
    """
    User Config database info.
    """

    db_uri: str = None


class UserConfigBase(BaseModel):
    """
    User config base.
    """

    player: str = None

    database: UserConfigDatabase = None
    defaults: UserConfigDefaults = None
    injest: UserConfigInjest = None
    source_mappings: dict = None
