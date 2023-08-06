#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2022 drad <drader@adercon.com>

from datetime import datetime
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class InjestLogReason(str, Enum):
    """
    Injest Log Reasons.
    """

    ok = "ok"
    metadata_extract_issue = "metadata extraction issue"
    updated = "updated"
    already_exists = "already exists"


class InjestLogStatus(str, Enum):
    """
    Injest Log Statuses.
    """

    ok = "ok"
    fail = "fail"
    issue = "issue"


class InjestLogBase(BaseModel):
    """
    Injest Log.
    """

    batchid: str = None  # injest batch-id (YYYY-MM-DD_HHMMSS.nnnn) used to group an injest log set.
    source: str = None  # source
    status: InjestLogStatus = None  # ok, fail, etc.
    reason: Optional[InjestLogReason] = None  # metadata_issue
    message: Optional[str] = None  # metadata extraction failed with error: xxxx


class InjestLog(InjestLogBase):
    """
    Extended (added by backend logic)
    """

    # note: this needs to be set/overwrote on result instantiation as using
    #  datetime.now() here will only get you now of when worker was started.
    created: datetime = datetime.now()
    updated: datetime = datetime.now()

    creator: Optional[str] = None
    updator: Optional[str] = None

    class Config:
        json_encoders = {datetime: lambda v: v.timestamp()}


class InjestResultType(str, Enum):
    """
    Injest Result types.
    """

    ok = "ok, processed successfully"
    updated = "document updated"
    fail_exists = "failure, document already exists"
    extract_metadata_issue = "extract metadata issue"
