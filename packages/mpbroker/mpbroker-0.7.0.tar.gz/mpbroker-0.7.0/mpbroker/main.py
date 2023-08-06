# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2022 drad <drader@adercon.com>
#
# LOGGING: designed to run at INFO loglevel.

import json
import subprocess  # nosec
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

import arrow
import click
import pycouchdb
import requests
import typer
import urllib3

import mpbroker.tools
from mpbroker.config.config import APP_NAME, APP_VERSION, user_cfg
from mpbroker.models.injest import InjestLog, InjestLogReason, InjestLogStatus
from mpbroker.models.media import (
    Media,
    MediaPlay,
    MediaPlayHistory,
    MediaPlayRating,
    MediaPlayStatus,
)
from mpbroker.utils import extract_metadata, get_sources_paths, make_doc

# disable InsecureRequestWarnings which come up if you are proxying couchdb through haproxy with ssl termination.
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

server = pycouchdb.Server(user_cfg.database.db_uri)
app = typer.Typer()
app.add_typer(mpbroker.tools.app, name="tools")


@app.command()
def play(
    name: str,
    user: str = typer.Option(
        user_cfg.defaults.user,
        "--user",
        help="user to use for playing",
    ),
):
    """
    Play a media item.
    """

    _base = Path(name)
    media_item = _base.name
    # typer.echo(f"Playing item [{name}/{media_item}]")

    # lookup item to get source.
    try:
        db = server.database("media")
        _id = f"{user}:{media_item}"
        # ~ typer.echo(f"- getting media item with id={_id} of name={name}")
        _doc = db.get(_id)
        # ~ typer.echo(f"- play doc: {_doc}")

        # typer.echo(f">> source_mappings: {user_cfg.source_mappings}")
        source_paths = get_sources_paths(_doc["sources"])
        if len(source_paths) < 1:
            typer.echo(
                f"No viable sources found for {name} with sources: {_doc['sources']}"
            )
            raise typer.Exit()
        # typer.echo(f" source_paths: {source_paths}")

        # @TODO: currently we simply play the first source_path - should have something
        #  better here eventually like a ranking or some checking.
        _media_path = f"{source_paths[0]['path']}/{name}"

        # capture when we start playing.
        _start = time.time()

        # @TODO: check if file and player exist, then execute
        # ~ typer.echo(f"Playing item with: {user_cfg.player} from location: {_media_path}")
        subprocess.call([user_cfg.player, _media_path])  # nosec
        _end = time.time()
        # ~ typer.echo("Play completed, creating play history...")

        # create the play history.
        _new_history = MediaPlayHistory(
            base=source_paths[0]["path"],
            player=user_cfg.player,
            start=_start,
            end=_end,
            client=f"{user}",
        )
        _history = []
        if (
            "play" in _doc
            and "history" in _doc["play"]
            and _doc["play"]["history"]
            and len(_doc["play"]["history"]) > 0
        ):
            _history = _doc["play"]["history"]
        _history.append(json.loads(_new_history.json()))
        # ~ j = json.loads(doc.json())
        # ~ typer.echo(f"- _history of type={type(_history)} is: {_history}")
        _doc["play"]["history"] = _history
        _doc["play"]["status"] = typer.prompt(
            "update Play Status",
            default=MediaPlayStatus.played,
            type=click.Choice([str(i) for i in MediaPlayStatus._value2member_map_]),
        )
        _doc["play"]["rating"] = int(
            typer.prompt(
                "Rate item",
                default=MediaPlayRating.ok,
                type=click.Choice([str(i) for i in MediaPlayRating._value2member_map_]),
            )
        )
        rating_notes = typer.prompt(
            "Add Rating notes? (leave blank to not add a note)",
            default="",
            show_default=False,
        )
        if rating_notes:
            _doc["play"]["rating_notes"] = rating_notes

        notes = typer.prompt(
            "Add Notes for media item? (leave blank to not add a note update)\n  A note for the media item could be something specific like 'watched Ep 1, 2, and 4'",
            default="",
            show_default=False,
        )
        if notes:
            _doc["play"]["notes"] = notes

        db.save(_doc)

    except requests.exceptions.ConnectionError:
        typer.echo("Database unavailable, is it up?")
        raise typer.Exit()
    except pycouchdb.exceptions.NotFound:
        typer.secho(
            f"Media item {name} not found for user {user}.",
            fg=typer.colors.RED,
            bold=True,
        )
        raise typer.Exit()


@app.command()
def list(
    name: str,
    user: str = typer.Option(
        user_cfg.defaults.user,
        "--user",
        help="user to use for listing",
    ),
):
    """
    List media by name.
    """

    from rich.console import Console
    from rich.table import Table

    try:
        db = server.database("media")

        results = db.query(
            "filters/names",
            # ~ group='true',
            # ~ keys=[name],
            startkey=f"{user}:{name}",
            endkey=f"{user}:{name}\ufff0",
            as_list=True,
            # ~ flat="key"
        )

        if results:
            typer.echo("\n\n")
            # ~ typer.echo(f"- results: {results}")
            table = Table(
                title=f"Listing Results for: '{name}'", title_justify="center"
            )
            table.add_column("Item", style="cyan", no_wrap=True)
            table.add_column("Status", justify="center", style="magenta")
            table.add_column("Rating")
            table.add_column("Notes")
            table.add_column("Sources", justify="right", style="yellow")
            table.add_column("Length")

            for item in results:
                _status = item["value"][1]
                _rating = f"{item['value'][2]}" if item["value"][2] else ""
                _rating = (
                    f"{_rating} {item['value'][3]}" if item["value"][3] else _rating
                )
                _notes = f"{item['value'][4]}" if item["value"][4] else ""
                _duration = f"{item['value'][6]}" if item["value"][6] else ""
                # ~ typer.echo(f" - {item['value'][0]}/{item['key']} | {_status} {_rating}")
                _user = f"{user}:"
                table.add_row(
                    f"{item['value'][0]}/{item['key'].replace(_user, '')}",
                    _status,
                    _rating,
                    _notes,
                    f"{', '.join(item['value'][5])}",
                    _duration,
                )

            console = Console()
            console.print(table)
        else:
            typer.echo("No results found")

    except requests.exceptions.ConnectionError:
        typer.echo("Database unavailable, is it up?")
        raise typer.Exit()


@app.command()
def injest(
    base: str = typer.Option(
        ..., "--base", help="the base path to search for media items to injest"
    ),
    source: str = typer.Option(
        user_cfg.defaults.source,
        "--source",
        help="source to use for injest (injested data will have this source)",
    ),
    user: str = typer.Option(
        user_cfg.defaults.user,
        "--user",
        help="user to use for injest (injested data will belong to this user)",
    ),
    extract_metadata_flag: bool = typer.Option(
        False,
        "--extract-metadata",
        help="extract media metadata (e.g. duration, size, encoding type, etc.) - this increases injest time significantly",
    ),
):
    """
    Injest media from a given base location.
    """

    typer.echo("Scanning base ({base}) for media...")
    _user = user if len(user) > 0 else None

    _base = Path(base)
    if not _base.exists() or not _base.is_dir():
        typer.echo(f"Directory [{_base}] not found or not a directory, cannot proceed!")
        raise typer.Exit()

    all_files = []
    for ext in user_cfg.injest.file_types:
        all_files.extend(_base.rglob(ext))

    typer.echo(
        f"""
---------- Confirm Injest ----------
- file types:       {user_cfg.injest.file_types}
- base:             {_base.as_posix()}
- user:             {_user}
- source:           {source}
- extract metadata: {extract_metadata_flag}
- number of items:  {len(all_files)}
"""
    )

    typer.confirm("Do you want to continue?", abort=True)
    _start = time.time()
    _batchid = arrow.utcnow().format("YYYY-MM-DD_HH:mm:ss.SSSS")

    with typer.progressbar(all_files) as progress:
        for f in progress:
            injest_file(
                source=source,
                filepath=f,
                base=_base.as_posix(),
                extract_metadata_flag=extract_metadata_flag,
                batchid=_batchid,
                user=_user,
            )

    _stop = time.time()

    # get injest_logs info
    try:
        db = server.database("injest_logs")
        _il_status = db.query(
            "filters/status",
            group="true",
            # ~ keys=['2022-05-03_12:24:35.4292'],
            startkey=[_batchid],
            endkey=[f"{_batchid}\ufff0"],
            as_list=True,
            # ~ flat="key"
        )
        # typer.echo(f"injest_logs info: {_il_status}")
        _rr = []
        for row in _il_status:
            _rr.append(f"\n\t- {row['key'][1]} ({row['key'][2]}): {row['value']}")

    except requests.exceptions.ConnectionError:
        typer.echo("Database unavailable, is it up?")
        raise typer.Exit()

    typer.echo(
        f"""
---------- Injest Summary ----------
Details
\t- location:        {_base.as_posix()}
\t- user:            {_user}
\t- source:          {source}
\t- files to injest: {len(all_files)}
\t- batchid:         {_batchid}
Number Injested{"".join(_rr)}
Injestion took {_stop - _start}s
"""
    )


def injest_file(
    source: str,
    filepath: str,
    base: str,
    extract_metadata_flag: bool = False,
    batchid: str = None,
    user: str = None,
):
    """
    Injest a file.
    @return: injest status
    """

    # ensure base ends with /
    _base = base if base.endswith("/") else f"{base}/"
    _user = f"{user}:" if user else ""
    # directory is filepath.parent - base
    directory = str(filepath.parent).replace(_base, "")

    # create InjestLog instance.
    il = InjestLog(
        batchid=batchid,
        source=source,
        status=InjestLogStatus.ok,
        reason=InjestLogReason.ok,
        message=None,
        created=datetime.now(),
        creator=_user,
    )

    metadata = None
    if extract_metadata_flag:
        metadata, error = extract_metadata(filepath)
        # if no metadata returned check error.
        # @TODO: need to properly handle metadata extraction issue (track and notify to user) - I like the write to db approach
        if not metadata:
            il.status = InjestLogStatus.issue
            il.reason = InjestLogReason.metadata_extract_issue

    m = Media(
        doc_id=f"{_user}{filepath.name}",
        # sid=make_sid(filepath.name),
        name=filepath.name,
        base=_base,
        directory=directory,
        sources=[source],
        media_type=filepath.suffix,
        # ~ notes="",
        play=MediaPlay(),
        metadata=metadata,
        creator=None,
        updator=None,
    )

    dts = make_doc(doc=m, rename_doc_id=True)

    try:
        db = server.database("media")
        db.save(
            dts
        )  # note: dont use .json() here as it serializes to a string which wont work!

    except requests.exceptions.ConnectionError:
        typer.echo("Database unavailable, is it up?")
        raise typer.Exit()
    except pycouchdb.exceptions.Conflict:
        _doc = db.get(m.doc_id)
        # set source and check if current matches, if not add.
        if source not in _doc["sources"]:
            _doc["sources"].append(source)
            db.save(_doc)
            # il.status = InjestLogStatus.ok
            il.reason = InjestLogReason.media_item_updated
        else:
            il.status = InjestLogStatus.fail
            il.reason = InjestLogReason.already_exists
            il.message = f"Duplicate item not injested: {m.directory}/{m.name}, source(s): {_doc['sources']}"

    # write the InjestLog record.
    try:
        db = server.database("injest_logs")
        db.save(
            # stopped here, need to get an _id on the il doc somewhere and go...
            make_doc(doc=il, rename_doc_id=False)
        )
    except requests.exceptions.ConnectionError:
        typer.echo("Database unavailable, is it up?")
        raise typer.Exit()


@app.command()
def info():
    """
    Show info such as config summary and library stats.
    """

    # NOTICE: this command is not 'user' aware, info is for complete Library.

    try:
        db = server.database("media")

        _total = db.query(
            "filters/stats_total",
            # ~ group='true',
            # ~ keys=[name],
            # ~ startkey=name,
            # ~ endkey=f"{name}\ufff0",
            as_list=True,
            # ~ flat="key"
        )
        if not _total or len(_total) < 1:
            typer.secho(
                "Your Library appears to be empty try, injesting something!",
                fg=typer.colors.MAGENTA,
                bold=True,
            )
            raise typer.Exit()

        _status = db.query(
            "filters/stats_status",
            group="true",
            as_list=True,
        )

        _sources = db.query(
            "filters/stats_sources",
            group="true",
            as_list=True,
        )

        _sources_list = [
            f"\n\t\t• {source['key'][0]} ({source['value']})" for source in _sources
        ]
        _new = [item for item in _status if item["key"] == MediaPlayStatus.new]
        _played = [item for item in _status if item["key"] == MediaPlayStatus.played]
        _watched = [item for item in _status if item["key"] == MediaPlayStatus.watched]

        typer.echo(
            f"""
{APP_NAME} {APP_VERSION}

Config
\t- Player:       {user_cfg.player}
\t- Database:     {user_cfg.database.db_uri}
\t- Injest Types: {user_cfg.injest.file_types}
Library
\t- TOTAL:   {_total[0]['value']}
\t- New:     {_new[0]['value'] if _new else 0}
\t- Played:  {_played[0]['value'] if _played else 0}
\t- Watched: {_watched[0]['value'] if _watched else 0}
\t- Sources: {''.join(_sources_list)}
"""
        )

    except requests.exceptions.ConnectionError:
        typer.echo("Database unavailable, is it up?")
        raise typer.Exit()


def version_callback(value: bool):
    if value:
        typer.echo(f"{APP_NAME} {APP_VERSION}")

        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        help="Show application version and exit",
    ),
):

    pass


if __name__ == "__main__":
    app()
