# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2020 drad <drader@adercon.com>

import logging
import subprocess  # nosec
from datetime import datetime
from typing import List

import docker
import typer
from packaging.version import parse
from rich.console import Console
from rich.table import Table
from tinydb import where

from ibuilder.config.config import APP_LOGLEVEL, CALLING_PARAMS, RUNDTS, get_db
from ibuilder.config.models import Application, Project
from ibuilder.models import UNITS, History, ResultStatus, TaskStatus, VersionIncrementType

logging.basicConfig(level=logging.getLevelName(APP_LOGLEVEL))


def approximate_size(size, flag_1024_or_1000=True):
    """
    Get approximate size - converts from bytes to mb/mib.
    """

    mult = 1024 if flag_1024_or_1000 else 1000
    for unit in UNITS[mult]:
        size = size / mult
        if size < mult:
            return "{0:.1f} {1}".format(size, unit)


def history_last_build(db):
    """
    Get the last build from history.
    """

    history = db.table("history").search(where("last") == True)  # noqa
    if history:
        logging.debug("- we have history...")
        return history[0]
    else:
        logging.debug("- no history...")
        return None


def increment_build_version(
    version: str = None, vit: VersionIncrementType = VersionIncrementType.default
):
    """
    Increment build version.
    """

    if version:
        lbv = parse(version).release
        if vit == VersionIncrementType.major:
            return f"{lbv[0] + 1}.{0}.{0}"
        elif vit == VersionIncrementType.minor:
            return f"{lbv[0]}.{lbv[1] + 1}.{0}"
        else:
            return f"{lbv[0]}.{lbv[1]}.{lbv[2] + 1}"
    else:
        return "0.0.1"


def confirm_data(
    prj: Project = None,
    last_build_version: str = None,
    build_version_generated: bool = False,
):
    """
    Show data for user to confirm before building.
    """

    table = Table(title="Review", expand=True, title_style="bold cyan", show_lines=True)
    table.add_column("Item", justify="left", style="bold cyan", no_wrap=True)
    table.add_column("Value", justify="left")

    table.add_row("component", prj.config.component)
    table.add_row("build", f"{prj.build.image}")
    table.add_row("push", f"{prj.push.image}")
    table.add_row(
        "tag source",
        f"{prj.source.tag} ({'push' if prj.source.push_tag else 'no push'})",
    )
    table.add_row("tag image latest", f"{prj.build.tag_image_latest}")
    table.add_row(
        "version",
        f"{prj.build.version} (last:{last_build_version} / generated: {build_version_generated})",
    )
    table.add_row("base path", prj.build.base_path)
    table.add_row("dockerfile", prj.build.dockerfile)
    table.add_row("network mode", prj.build.network_mode)
    table.add_row("build repo", prj.build.repository)
    table.add_row("push registry", prj.push.registry.url)
    table.add_row("build args", f"{get_build_args(prj)}")
    table.add_row("labels", f"{get_build_labels(prj.build.labels)}")
    table.add_row("docker config", prj.push.docker_config_path)

    console = Console()
    console.print(table)


def get_build_args(prj):
    """
    Convert build args from list to dict.
    NOTE: if BUILD_VERSION is an arg its value will be replaced by the build version.
    """

    r = {}
    for a in prj.build.args:
        if "BUILD_VERSION" in a:
            a["BUILD_VERSION"] = f"{prj.build.version}"

        r.update(a)
    return r


def get_build_labels(labels):
    """
    Convert labels from list to dict.
    """

    r = {}
    for label in labels:
        r.update(label)
    return r


def image_build(prj: Project = None, app: Application = None):
    """
    Build image using a docker client.
    """

    logging.debug("- building image...")
    try:
        client = docker.from_env()
        typer.secho("Building image (this may take a while)...", fg=typer.colors.YELLOW)
        labels = {"BUILDER": app.name, "BUILDER_VERSION": app.version}
        # add any additional labels specified.
        labels.update(get_build_labels(prj.build.labels))
        logging.debug(f"building with labels: {labels}")
        buildargs = get_build_args(prj)
        logging.debug(f"building with args: {buildargs}")
        tag = f"{prj.build.repository}:{prj.build.version}"
        logging.debug(f"build with tag: {tag}")

        build = client.images.build(
            path=prj.build.base_path,
            dockerfile=prj.build.dockerfile,
            tag=tag,
            buildargs=buildargs,
            labels=labels,
            network_mode=prj.build.network_mode,  # this is needed to get ukse app image to build for assets:precompile (@todo: need to find a better way to do this)
        )
        built_image = build[0]
        built_logs = build[1]
        typer.echo("BUILD LOG FOLLOW:")
        for r in built_logs:
            if "stream" in r:
                # typer.echo(f"{' '.join(r['stream'].split()).rstrip()}")
                for line in r["stream"].splitlines():
                    typer.echo(line)
            else:
                # @TODO: we have a bug here where in some cases there is no 'stream' in r
                #        but we have not been able to track it down. For now we will dump r
                logging.critical(
                    f"No 'stream' in built_logs, please report this as an issue with the following information:\n{r}"
                )

        logging.debug("- After built_logs loop...")
        if prj.build.tag_image_latest:
            logging.debug("- tagging image with 'latest'...")
            built_image.tag(f"{prj.build.repository}", "latest")
        return True
    except docker.errors.BuildError as e:
        typer.secho(
            f"Docker Build Error, cannot continue.\n- details: {e}",
            fg=typer.colors.RED,
            err=True,
        )
        return False
    except docker.errors.APIError as e:
        typer.secho(
            f"Docker API Error, cannot continue.\n- details: {e}",
            fg=typer.colors.RED,
            err=True,
        )
        return False
    except Exception as e:
        typer.secho(
            f"Other Docker Build Error, cannot continue.\n- details: {e}",
            fg=typer.colors.RED,
            err=True,
        )
        return False


def tag_source(prj: Project = None, app: Application = None, push_tag: bool = False):
    """
    Tag source code with build version.
    """

    try:
        tag_name = f"{prj.config.component + '-' if prj.config.component else ''}{prj.build.version}"
        typer.echo(f"- tag source with: {tag_name}")
        tag_calling_params = [
            "git",
            "tag",
            "-a",
            tag_name,
            "-m",
            f"{app.name} created {prj.build.version}",
        ]
        typer.echo("-- applying tag...")
        subprocess.call(tag_calling_params, shell=False)  # nosec
        if push_tag:
            push_calling_params = ["git", "push", "origin", tag_name]
            typer.echo("-- pushing tag...")
            subprocess.call(push_calling_params, shell=False)  # nosec

        return True
    except Exception as e:
        typer.secho(
            f"Error in applying source code tag: {e}", fg=typer.colors.RED, err=True
        )
        return False


def image_registry_login(prj: Project = None):
    """
    Login to image registry.
    """

    client = docker.from_env()
    try:
        client.login(
            username=prj.push.registry.username,
            password=prj.push.registry.password
            if prj.push.registry.password and len(prj.push.registry.password) > 0
            else None,
            registry=prj.push.registry.url,
            dockercfg_path=prj.push.docker_config_path,
        )
        return True
    except Exception as e:
        logging.error(
            f"Registry Login Problem, cannot continue.\n  You likely need to do a 'docker login...' or supply the 'push.registry.password' config variable.\nDetails: {e}"
        )
        return False


def image_push_by_tag(prj: Project = None, tag: str = None):
    """
    Push an image by tag.
    """

    logging.debug(f"- pushing tag: {tag}")
    client = docker.from_env()
    ret = False
    last_line = ""
    # @TODO: current docker-py does not support content trust logic, [see](https://github.com/docker/docker-py/issues/1773). Once it is supported we will use it!
    #        also note that the only apparent work-around for this is to use subprocess, our issue with that is we would loose streaming of build push data.
    for line in client.images.push(
        repository=prj.build.repository, tag=tag, stream=True, decode=True
    ):
        if "status" in line:
            typer.echo(line["status"])
            last_line = line["status"]
    # if success return true, otherwise try again.
    # success line looks like the following
    # 0.7.0: digest: sha256:eda4a046da5d045cf19af68165f7c1c0a9801ed9c711dd6dc277480b6338bf05 size: 2200
    # {tag}: digest: * size: xxx
    logging.debug(f"--> push of {tag} complete.")
    try:
        pr_tag, pr_digest_label, pr_digest, pr_size_label, pr_size = last_line.replace(
            ":", ""
        ).split(" ")
        if pr_tag == tag:
            typer.echo(f"Push of {tag} succeeded!")
            ret = True
        else:
            typer.secho(f"Push of {tag} failed!", fg=typer.colors.RED, err=True)
    except ValueError as e:
        typer.secho(f"Push failed with: {e}", fg=typer.colors.RED, err=True)
        ret = False

    return ret


def image_push(prj: Project = None):
    """
    Push the built image to the registry.
    NOTE: 'latest' tag is only pushed if specified.
    """

    logging.debug("- push image...")
    ret = False
    ret_base = False
    ret_latest = False
    if image_registry_login(prj=prj):
        ret_base = image_push_by_tag(prj=prj, tag=prj.build.version)
        ret = ret_base
        if prj.build.tag_image_latest:
            ret_latest = image_push_by_tag(prj=prj, tag="latest")
            if not ret_base or not ret_latest:
                ret = False
            else:
                ret = True

    return ret


def image_repush(r):
    """
    Repush an image from a history entry.
    """

    _db = get_db()
    tasks_start = datetime.utcnow()
    result_status = ResultStatus.success
    task_status: List[TaskStatus] = []
    prj: Project = Project(**r["run_params"])
    if image_push(prj=prj):
        logging.debug("- repush succeeded...")
        task_status.append(TaskStatus.repush_ok)
        result_status = result_status.success
        # if we have a success then update all other history records to have last=False.
        _db.table("history").update({"last": False})
    else:
        logging.debug("- repush failed...")
        task_status.append(TaskStatus.repush_fail)
        result_status = result_status.push_fail
    runtime = (datetime.utcnow() - tasks_start).total_seconds()
    # create and write the history record.
    h = History(
        created=RUNDTS,
        runtime=runtime,
        result=result_status,
        task_status=task_status,
        calling_params=CALLING_PARAMS,
        run_params=prj,
        last=True if result_status == ResultStatus.success else False,
    )
    hid = _db.table("history").insert(h.dict())
    typer.echo(
        f"- history: {hid} - {result_status} ({runtime}s) [{', '.join(task_status)}]"
    )
