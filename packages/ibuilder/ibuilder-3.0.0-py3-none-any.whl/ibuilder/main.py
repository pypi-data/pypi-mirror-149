#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2020 drad <drader@adercon.com>

import logging
from datetime import datetime
from typing import List, Optional

import typer
from tinydb import where

import ibuilder.history
import ibuilder.images
from ibuilder.config.config import (
    APP,
    CALLING_PARAMS,
    RUNDTS,
    get_db,
    get_prj_conf,
    load_prj_conf,
)
from ibuilder.models import History, ResultStatus, TaskStatus, VersionIncrementType
from ibuilder.utils import (
    confirm_data,
    history_last_build,
    image_build,
    image_push,
    image_repush,
    increment_build_version,
    tag_source,
)

app = typer.Typer(help="build, tag, and push images")
app.add_typer(ibuilder.history.app, name="history")
app.add_typer(ibuilder.images.app, name="images")

_prj = None
_db = None


@app.command()
def build(
    version: str = typer.Option(
        None, help="build version (leave blank to auto-generate)"
    ),
    image: bool = typer.Option(None, "--image", help="perform build of image"),
    no_image: bool = typer.Option(
        None, "--no-image", help="do not perform build of image"
    ),
    push: bool = typer.Option(None, "--push", help="push image to registry"),
    no_push: bool = typer.Option(
        None, "--no-push", help="do not push image to registry"
    ),
    source_tag: bool = typer.Option(None, "--source-tag", help="tag source code"),
    no_source_tag: bool = typer.Option(
        None, "--no-source-tag", help="do not tag source code"
    ),
    version_increment_type: VersionIncrementType = typer.Option(
        VersionIncrementType.default,
        "--version-increment-type",
        "-i",
        show_default=True,
        help="specify the build version increment type (for auto-generate of build-version only)",
    ),
):
    """Perform a build, tag, or push."""

    # check for/set cli overrides.
    _prj.build.image = True if image else _prj.build.image
    _prj.push.image = True if push else _prj.push.image
    _prj.source.tag = True if source_tag else _prj.source.tag

    _prj.build.image = False if no_image else _prj.build.image
    _prj.push.image = False if no_push else _prj.push.image
    _prj.source.tag = False if no_source_tag else _prj.source.tag

    last = history_last_build(_db)
    logging.debug(f"- last is: {last}")
    lbv = None
    if last:
        lbv = last["run_params"]["build"]["version"]
    else:
        lbv = "0.0.0"
    logging.debug(f"- ######## lbv is: {lbv} - vit={version_increment_type}")
    gen_build_version = False
    if not version:
        gen_build_version = True
        logging.debug("- generating build version...")
        version = increment_build_version(version=lbv, vit=version_increment_type)
    logging.debug(f"- building version: {version}")
    # update project version with version we will build.
    _prj.build.version = version
    confirm_data(
        prj=_prj,
        last_build_version=lbv,
        build_version_generated=gen_build_version,
    )

    proceed = typer.confirm("Proceed with build?")
    result_status = ResultStatus.success
    task_status: List[TaskStatus] = []
    if proceed:
        tasks_start = datetime.utcnow()
        logging.debug("proceeding with build...")
        if _prj.build.image:
            logging.debug("- build the image...")
            logging.debug(f"- build will use project labels: {_prj.build.labels}")
            if image_build(prj=_prj, app=APP):
                logging.debug("- build succeeded...")
                task_status.append(TaskStatus.build_ok)
            else:
                logging.debug("- build failed...")
                task_status.append(TaskStatus.build_fail)
                result_status = result_status.build_fail

                # @todo: need to handle build fail, stop the process, write history and exit

        # tag source before push as push often fails.
        if _prj.source.tag:
            logging.debug("- tag source...")
            if tag_source(
                prj=_prj,
                app=APP,
                push_tag=_prj.source.push_tag,
            ):
                logging.debug("- tag source succeeded...")
                task_status.append(TaskStatus.source_tag_ok)
            else:
                logging.debug("- tag source failed...")
                task_status.append(TaskStatus.source_tag_fail)
                result_status = result_status.source_tag_fail

        if _prj.push.image:
            logging.debug("- push the image...")
            if image_push(prj=_prj):
                logging.debug("- push succeeded...")
                task_status.append(TaskStatus.push_ok)
            else:
                logging.debug("- push failed...")
                task_status.append(TaskStatus.push_fail)
                result_status = result_status.push_fail

        # if we did a push and it was successful then set this as 'latest' and all others to not latest.
        if TaskStatus.push_ok in task_status:
            _db.table("history").update({"last": False})
        runtime = (datetime.utcnow() - tasks_start).total_seconds()
        # create and write the history record.
        h = History(
            created=RUNDTS,
            runtime=runtime,
            result=result_status,
            task_status=task_status,
            calling_params=CALLING_PARAMS,
            run_params=_prj,
            last=True
            if result_status == ResultStatus.success
            and TaskStatus.push_ok in task_status
            else False,
        )
        hid = _db.table("history").insert(h.dict())
        typer.echo(
            f"- history: {hid} - {result_status} ({runtime}s) [{', '.join(task_status)}]"
        )
    else:
        typer.echo("Not confirmed, build canceled.")
        if _prj.history.save_request_canceled:
            logging.debug("Saving canceled build request..")
            h = History(
                created=RUNDTS,
                runtime=0,
                result=ResultStatus.user_cancel,
                calling_params=CALLING_PARAMS,
                run_params={},
                last=False,
            )
            hid = _db.table("history").insert(h.dict())
            typer.echo(f"- history: {hid}")
        else:
            logging.debug(
                "Project settings indicate to NOT save canceled build requests..."
            )


@app.command()
def repush(
    last: bool = typer.Option(True, "--last", help="repush from last history item"),
    id: int = typer.Option(None, help="id of History item"),
):
    """Repush a previously built image."""

    # if id is supplied we will use it otherwise we use last.
    if id:
        typer.echo(f"Repushing from History id: {id}")
        r = _db.table("history").get(doc_id=id)
        if r:
            logging.info(f"- found history record: {r}")
            image_repush(r)
        else:
            typer.secho(f"No history entry found with id: {id}", fg=typer.colors.YELLOW)
    else:
        typer.echo("Repushing from last history record")
        r = _db.table("history").search(where("last") == True)[0]  # noqa
        if r:
            logging.info(f"- found history record: {r}")
            image_repush(r)
        else:
            typer.secho("No last history entry found.", fg=typer.colors.YELLOW)


def version_callback(value: bool):
    if value:
        typer.echo(f"{APP.name} {APP.version}")

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
    global _db, _prj

    # load PRJ (project config file)
    load_prj_conf()
    _prj = get_prj_conf()
    _db = get_db()
