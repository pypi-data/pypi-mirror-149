#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2022 drad <drader@adercon.com>

import json
from pathlib import Path
from typing import List

from mpbroker.config.config import user_cfg
from mpbroker.models.media import MediaMetadata

# ~ import typer


def get_sources_paths(sources: List):
    """
    Get sources paths.
    NOTE: source paths are validated (checked), if a path is invalid (does not exist)
          it will not be returned.
    @return: list of source paths.
    """

    # ~ typer.echo(f">> sources: {sources}")
    _ret = []
    for source in sources:
        # ~ typer.echo(f"   ─⏵ checking source: {source}")
        if source in user_cfg.source_mappings:
            _path = user_cfg.source_mappings[source]
            # check if path exists.
            if Path(_path).is_dir() and any(Path(_path).iterdir()):
                # ~ typer.echo(f"- found {_path} and it has data...")
                _ret.append({"source": source, "path": _path})
            # ~ typer.echo(f"- found {source} in source_mappings: {user_cfg.source_mappings[source]}")

    # typer.echo(f"_ret is: {_ret}")
    return _ret


def generate_sid(instr: str = None):
    """
    Generate a sid given an input string.
    Example: 'Duck_Dynasty_S1_D1.mkv' ─⏵ 'DCKDNSTS1D1.MKV'
    """

    return instr.translate(str.maketrans("", "", "AaEeIiOoUuYy_-()[]")).upper()


def make_doc(doc=None, rename_doc_id: bool = False):
    """
    Create a couchdb doc by deserializing the class to json, loading it back to
    json and finally renaming the doc_id field to _id.

    NOTE: the double deserialization is needed to get dates deserialized (easily)
    NOTE: we need to rename doc_id to _id as we can name it _id in the model or alias
          it as python treats it as a local and does not export it on deserialization.
    """

    j = json.loads(doc.json())
    if "doc_id" in j and rename_doc_id:
        j["_id"] = j.pop("doc_id")
    # ~ typer.echo(f"j={j}")

    return j


def extract_metadata(filepath) -> MediaMetadata:
    """
    Extract media metadata from a file
    """

    from pymediainfo import MediaInfo

    # ~ typer.echo(f"- extracting media metadata for filepath: {filepath}")
    try:
        media_info = MediaInfo.parse(filepath)

        # extract metadata
        metadata = MediaMetadata(
            file_size=media_info.tracks[0].other_file_size[0],
            file_type=media_info.tracks[1].internet_media_type,
            file_format=media_info.tracks[0].format,
            encoding=media_info.tracks[1].encoded_library_name,
            duration=media_info.tracks[0].other_duration[0],
            resolution=f"{media_info.tracks[1].width} x {media_info.tracks[1].height}",
            aspect_ratio=media_info.tracks[1].other_display_aspect_ratio[0],
            audio_format=media_info.tracks[2].format,
            audio_sampling=media_info.tracks[2].sampling_rate,
        )
    except Exception as e:
        # typer.secho(f"Failed extracting metadata for {filepath} with error: {e}", fg=typer.colors.RED, bold=True, err=True)
        return None, f"Failed extracting metadata for {filepath} with error: {e}"

    # typer.echo(f"- extracted metadata: {metadata}")

    return metadata, None
