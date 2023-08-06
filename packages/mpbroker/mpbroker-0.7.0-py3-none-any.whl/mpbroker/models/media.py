#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2022 drad <drader@adercon.com>

from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel


class MediaType(str, Enum):
    """
    Media types.
    """

    mkv = ".mkv"
    mp4 = ".mp4"


class MediaPlayStatus(str, Enum):
    """
    Media play statuses.
    """

    new = "new"
    played = "played"
    watched = "watched"


class MediaPlayRating(str, Enum):
    """
    Media play Ratings.
    """

    unwatchable = 0
    horrible = 1
    bad = 2
    ok = 3
    good = 4
    excellent = 5


class MediaPlayHistory(BaseModel):
    """
    Media item Play History info.
    """

    base: str = None  # the base (directory) of the media_item.
    player: str = None  # the player used.
    start: datetime = None  # when play started.
    end: datetime = None  # when play ended.
    client: str = None  # the host/client:user who played the item.

    class Config:
        json_encoders = {datetime: lambda v: v.timestamp()}


class MediaPlay(BaseModel):
    """
    Media item Play info.
    """

    status: MediaPlayStatus = MediaPlayStatus.new  # the play status of the item.
    rating: Optional[MediaPlayRating] = None  # play rating.
    rating_notes: Optional[str] = None  # notes about rating.
    notes: Optional[str] = None  # notes about the play (e.g. watched 1, 2, 3).
    history: Optional[List[MediaPlayHistory]] = None  # play history info.


class MediaMetadata(BaseModel):
    """
    Media Metadata.
    """

    file_size: str = None  # filesize in human readable format (569 MiB, 1.1 GiB)
    file_type: str = None  # file type (video/H265)
    file_format: str = None  # file format (Matroska)
    encoding: str = None  # encoding (x265)
    duration: str = None  # duration in human readable format (1 h 52 min, 2 h 48 min)
    resolution: str = None  # resulution in width x height format (720 x 480)
    aspect_ratio: str = None  # display aspect ratio (16:9)
    audio_format: str = None  # audio format (AAC)
    audio_sampling: str = None  # audio sample rate (48000)


class MediaBase(BaseModel):
    """
    A media item.
    """

    name: str = None  # name of item (e.g. Duck_Dynasty_S1_D2.mkv)
    base: str = None  # base location of item (e.g. /opt/media)
    directory: str = None  # directory item is in (e.g. shows/Duck_Dynasty)
    sources: List[
        str
    ] = None  # list of sources the item is available at (e.g. gaz, bob, festus, etc.)
    media_type: Optional[
        MediaType
    ] = None  # media type of media item (e.g. .mkv, .mp4, etc. - the file extension)
    notes: Optional[
        str
    ] = None  # notes about the media item (e.g. video has defect aroudn 33m into movie)
    play: Optional[MediaPlay] = None  # play info for an item.
    metadata: Optional[
        MediaMetadata
    ] = None  # metadata such as file size, duration, etc.

    class Config:
        json_encoders = {"MediaType": lambda t: t.value}


class MediaExt(MediaBase):
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


class Media(MediaExt):
    """
    The media item.
    """

    doc_id: str = None  # doc id
