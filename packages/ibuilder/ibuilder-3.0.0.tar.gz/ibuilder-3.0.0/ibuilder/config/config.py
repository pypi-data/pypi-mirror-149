# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2020 drad <drader@adercon.com>

import logging
import sys
from os import getenv
from pathlib import Path

import arrow
import pkg_resources
import tomli
import typer
from tinydb import TinyDB

from ibuilder.config.models import Application, Project


def load_config(conf_file, ctype) -> dict:
    """
    Load config data from toml config file.
    """

    try:
        with open(conf_file, "rb") as f:
            return ctype(**tomli.load(f))

    except FileNotFoundError as e:
        typer.secho(f"File [{conf_file}] not found: {e}", fg=typer.colors.RED, err=True)
        return None
    except Exception as e:
        typer.secho(
            f"Exception handling file [{conf_file}]: {e}", fg=typer.colors.RED, err=True
        )
        return None


def get_prj_conf():
    """
    Get PRJ.
    """

    global PRJ

    return PRJ


def get_db():
    """
    Get DB.
    """

    global DB

    return DB


def load_prj_conf():
    """
    Load the PRJ object
    """
    global PRJ, DB

    PRJ = load_config(".boi.toml", Project)

    if not PRJ:
        # we need the project conf as it has the pass to the database to use.
        typer.secho(
            "  Are you sure you are in the correct directory?",
            fg=typer.colors.YELLOW,
            err=True,
        )
        raise typer.Exit(code=12)

    # if we have a project db and it has content and it is a pre-version 2 format convert it.
    if Path(PRJ.config.dbpath).exists():
        DB = TinyDB(PRJ.config.dbpath)
        if len(DB.table("history")) > 0:
            logging.debug("DB has data...")
            # check db version in 'version' 'table'
            try:
                version = DB.table("version").all()[0]
                logging.debug(f"db version is: {version}")
            except IndexError:
                logging.warning(
                    "No database version found (must be a v1 db), moving db to create a new v2 db..."
                )
                dest_name = "{0}.v1.{1}".format(
                    PRJ.config.dbpath, arrow.now("local").timestamp
                )
                dest = Path(dest_name)
                src = Path(PRJ.config.dbpath)
                dest.write_text(src.read_text())
                src.write_text("")  # wipe the file.
                typer.echo(
                    typer.style(
                        f"NOTICE: Local boi database has been cleaned, refer to {dest_name} for your old (v1) database if needed",
                        fg=typer.colors.YELLOW,
                        bold=True,
                    )
                )
                DB.table("version").insert({"db": 2})
        else:
            logging.debug("Looks like you have an empty db!")

    else:
        typer.echo(f"- no project db, creating: {PRJ.config.dbpath}")
        open(PRJ.config.dbpath, "a").close()
        DB = TinyDB(PRJ.config.dbpath)


APP = Application(
    name=pkg_resources.get_distribution("boi").project_name,
    version=pkg_resources.get_distribution("boi").version,
)
# log level [CRITICAL|ERROR|WARNING|INFO|DEBUG]
APP_LOGLEVEL = getenv("LOG_LEVEL", "INFO")
CALLING_PARAMS = " ".join(sys.argv[1:])
DB = None
# ~ PRJ = load_config(".boi.toml", Project)
PRJ = None
RUNDTS = arrow.now("local").format("YYYY-MM-DD HH:mm:ss")

logging.basicConfig(level=logging.getLevelName(APP_LOGLEVEL))
