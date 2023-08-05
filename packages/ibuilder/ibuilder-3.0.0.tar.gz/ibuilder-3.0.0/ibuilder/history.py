#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2020 drad <drader@adercon.com>

import logging
from pprint import pformat

import arrow
import typer
from rich import box
from rich.console import Console
from rich.table import Table
from tinydb import where

from ibuilder.config.config import APP_LOGLEVEL, get_db
from ibuilder.models import HistoryOnDB, ResultStatus

logging.basicConfig(level=logging.getLevelName(APP_LOGLEVEL))
app = typer.Typer(help="Interact with build history.")


def completed(item):
    return "✓" if item else "✗"


def version_with_latest(version: str = None, last: bool = False):
    return f"[bold red]✦{version}[/bold red]" if last else version


def history_summary(db):
    """Shows a summary of the history."""

    table = Table(
        title="History Summary", show_header=True, header_style="bold magenta"
    )
    table.add_column("Id", style="dim")
    table.add_column("Date")
    table.add_column("Runtime")
    table.add_column("Result")
    table.add_column("Calling Params")
    table.add_column("B/L/S/P")
    table.add_column("Version")

    history = db.table("history").all()
    if history:
        for r in history:
            h = HistoryOnDB(doc_id=r.doc_id, **r)
            blsp = []
            ver = ""
            if h.run_params:
                blsp.append(completed(h.run_params["build"]["image"]))
                blsp.append(completed(h.run_params["build"]["tag_image_latest"]))
                blsp.append(completed(h.run_params["source"]["tag"]))
                blsp.append(completed(h.run_params["push"]["image"]))
                ver = version_with_latest(h.run_params["build"]["version"], h.last)
            table.add_row(
                h.doc_id,
                arrow.get(h.created).to("local").format("YYYY-MM-DD HH:mm:ss"),
                str(h.runtime),
                h.result,
                h.calling_params,
                "/".join(blsp),
                ver,
            )
        return table
    else:
        typer.echo(typer.style("No Data found.", fg=typer.colors.YELLOW, bold=True))
    return False


def history_detail(db, id):
    """Show history detail (all info for a specific history item)."""

    table = Table(
        title=f"History Detail for: {str(id)}",
        show_header=False,
        show_edge=True,
        show_lines=True,
        header_style=None,
        box=box.SQUARE,
    )
    r = db.table("history").get(doc_id=id)
    h = HistoryOnDB(doc_id=r.doc_id, **r)
    table.add_column("", justify="right", style="bold magenta")
    table.add_column("", justify="left")
    table.add_row("Id", h.doc_id)
    table.add_row(
        "Date", arrow.get(h.created).to("local").format("YYYY-MM-DD HH:mm:ss")
    )
    table.add_row("Last", str(h.last))
    table.add_row("Runtime", str(h.runtime))
    table.add_row("Result", h.result)
    table.add_row("Task Status", ", ".join(h.task_status))
    table.add_row("Calling Params", h.calling_params)
    table.add_row("Run Params", str(pformat(h.run_params)))

    return table


def history_prune(db, result):
    """Remove data from history file by result value."""

    h = db.table("history")  # .search(Result.status == 1)
    canceled = h.search(where("result") == result)
    if canceled:
        h.remove(where("result") == result)
        typer.echo(f"Items with result of '{result}' removed, history is now:")
        # show the history table after pruning.
        summary()
        return True
    else:
        typer.echo(
            typer.style(
                f"Nothing to remove, no items matched: '{result}'",
                fg=typer.colors.YELLOW,
                bold=True,
            )
        )
        return False


@app.command()
def summary():
    """Show the history summary."""

    console = Console()
    table = history_summary(get_db())
    if table:
        console.print(table)


@app.command()
def detail(id: int = typer.Option(..., help="id of History item")):
    """Show details for a specific history item."""

    console = Console()
    table = history_detail(get_db(), id)
    console.print(table)


@app.command()
def prune(result: ResultStatus = typer.Option(..., help="result type")):
    """Prune items from the history."""

    history_prune(get_db(), result)
