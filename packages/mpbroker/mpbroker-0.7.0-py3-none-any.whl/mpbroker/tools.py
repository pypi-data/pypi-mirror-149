# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2022 drad <drader@adercon.com>
#

import pycouchdb
import requests
import typer

from mpbroker.config.config import DATABASES, user_cfg

server = pycouchdb.Server(user_cfg.database.db_uri)

app = typer.Typer(help="[Somewhat] useful tools!")


@app.command()
def db_init():
    """
    Perform DB setup tasks: create databases, views, etc.
    """
    from mpbroker.config.db_init_design_docs import views

    typer.echo("Creating Databases:")
    for db in DATABASES:
        try:
            server.create(db)
            typer.secho(f" ✓ {db} - created", fg=typer.colors.GREEN)
        except pycouchdb.exceptions.Conflict:
            typer.secho(f" ✗ {db} - skipped (already exists)", fg=typer.colors.WHITE)
        except requests.exceptions.ConnectionError:
            typer.echo("Database unavailable, is it up?")
            raise typer.Exit()
        except Exception as e:
            typer.secho(
                f"Other error occurred during create databases: {e}",
                fg=typer.colors.RED,
                bold=True,
                err=True,
            )
            raise typer.Exit()

    typer.echo("Creating Views:")
    try:
        for view in views:
            db = server.database(view[0])
            db.save(view[1])
            typer.secho(
                f" ✓ {view[0]}/{view[1]['_id']} - created", fg=typer.colors.GREEN
            )

    except requests.exceptions.ConnectionError:
        typer.secho(
            "Database unavailable, is it up?", fg=typer.colors.RED, bold=True, err=True
        )
        raise typer.Exit()
    except pycouchdb.exceptions.Conflict:
        typer.secho(
            f" ✗ {view[0]}/{view[1]['_id']} - skipped (already exists)",
            fg=typer.colors.WHITE,
        )
    except Exception as e:
        typer.secho(
            f"Other error occurred during create views: {e}",
            fg=typer.colors.RED,
            bold=True,
            err=True,
        )
        raise typer.Exit()


@app.command()
def move_media(
    from_user: str = typer.Option(
        user_cfg.defaults.user,
        "--from-user",
        help="the user account to change",
    ),
    to_user: str = typer.Option(
        user_cfg.defaults.user,
        "--to-user",
        help="the user account to change to",
    ),
    limit: int = typer.Option(
        0,
        "--limit",
        help="limit number of media items to process (0 means no limit)",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="perform move without making any changes",
    ),
):
    """
    Move media (add username prefix to media in your library)
    """

    # show summary and confirm.
    typer.secho(
        "WARNING: this will move all media to the user listed below!",
        fg=typer.colors.BLACK,
        bg=typer.colors.RED,
        bold=True,
    )
    typer.secho(
        f"""\tfrom user: {from_user}
\tto user:   {to_user}
\tdb-uri:    {user_cfg.database.db_uri}
\tdry-run:   {dry_run}
\tlimit:     {limit if limit > 0 else 'none'}
"""
    )
    if not dry_run:
        typer.echo(
            "You may want to use the --dry-run parameter to test the changes before the final run"
        )
        typer.secho(
            "Only proceed if you know what you are doing!",
            fg=typer.colors.RED,
            bold=True,
        )
    typer.confirm("\nDo you want to continue?", abort=True)

    db = server.database("media")
    results = db.query(
        "filters/names",
        # group='true',
        # keys=[name],
        startkey=f"{from_user}",
        endkey=f"{from_user}\ufff0",
        as_list=True,
        # flat="key"
    )
    _processed = 0
    for _adoc in results:
        # skip any design-docs.
        # ~ if not _adoc['id'] == '_design/filters' and _adoc['id'].startswith(_from_user):
        if not _adoc["id"] == "_design/filters":
            typer.echo(f"- updating item with id: {_adoc['id']}")
            # ~ typer.echo(f" >> (adoc.id={_adoc['id']}): {_adoc}")
            doc = db.get(_adoc["id"])
            split_id = _adoc["id"].split(":")
            _name = None
            if len(split_id) < 2:
                _name = split_id[0]
            else:
                _name = split_id[1]
            # ~ typer.echo(f" >> (doc.id={doc['_id']}): {doc}")
            doc["_id"] = f"{to_user}:{_name}"
            if not dry_run:
                db.delete(_adoc["id"])
                del doc["_rev"]
                # ~ typer.echo(f" >> saving doc: {doc}")
                db.save(doc)
            typer.echo(f"  ─⏵ after update id: {doc['_id']}")
            _processed += 1
        if limit > 0 and _processed >= limit:
            break

    typer.secho(
        f"Total number processed: {_processed}", fg=typer.colors.MAGENTA, bold=True
    )
