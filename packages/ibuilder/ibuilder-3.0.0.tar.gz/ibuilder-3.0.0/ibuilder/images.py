#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2020 drad <drader@adercon.com>

import json
import logging
from base64 import b64decode
from os import path

import arrow
import docker
import requests
import typer
from rich.console import Console
from rich.table import Table
from rich.text import Text

from ibuilder.config.config import APP_LOGLEVEL, get_prj_conf
from ibuilder.config.models import Project
from ibuilder.utils import approximate_size

logging.basicConfig(level=logging.getLevelName(APP_LOGLEVEL))
app = typer.Typer(help="View previously build image info.")

client = docker.from_env()


def local_images(prj: Project = None):
    """Get local images."""

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Id", style="dim")
    table.add_column("Tag")
    table.add_column("Created")
    table.add_column("Size")

    images = client.images.list(name=prj.build.repository)
    for i in images:
        img_id = i.short_id.split(sep=":")[1]
        versions = []
        for t in i.tags:
            versions.append(t.split(sep=":")[1])
        table.add_row(
            img_id,
            ", ".join(versions),
            arrow.get(i.attrs["Created"]).to("local").format("YYYY-MM-DD HH:mm:ss"),
            approximate_size(i.attrs["Size"], False),
        )

    return table


def remote_images(prj: Project = None):
    """Get remote images."""

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Id", style="dim")
    table.add_column("Tag")
    table.add_column("Created")
    table.add_column("Size")

    dcp = path.expandvars(prj.push.docker_config_path)
    logging.debug(f"docker config path: {dcp}")
    registry_url, registry_repo = prj.build.repository.split(sep="/")
    url_endpoint = f"https://{registry_url}/v2/{registry_repo}/tags/list"

    # open dockercfg file, get pertinent registry, base64 decode it, split into auth (user/pwd)
    with open(dcp) as jf:
        data = json.load(jf)

    if data:
        d_user, d_pwd = (
            b64decode(data["auths"][registry_url]["auth"])
            .decode("utf-8")
            .split(sep=":")
        )
    auth = (d_user, d_pwd)

    try:
        logging.debug(f"- connecting to: {url_endpoint}")
        r = requests.get(url_endpoint, auth=auth)

        if r and r.status_code == 200 and r.text:
            tags = r.json()["tags"]
            # sorted_tags = sorted(tags, key=lambda x: version.Version(x))
            # NOTICE: advanced sorting (e.g. via version.Version) is not worth
            #   it as tags could be anything (e.g. 1.0.1, v1.0.1, a, b, etc.)
            for t in sorted(tags):
                # note: I've researched for a way to get size for a remote image and
                #  it appears to not be possible with a docker-registry instance.
                table.add_row("", t, "", "")
        else:
            logging.critical("No tags found")

    except requests.ConnectionError:
        logging.critical("Cannot connect to Registry")

    return table


@app.command()
def list(
    local: bool = typer.Option(False, "--local"),
    remote: bool = typer.Option(False, "--remote"),
):
    """List images."""

    _prj = get_prj_conf()

    console = Console()
    text = Text()

    if local:
        text = Text.assemble(
            ("Local Images for: ", "bold magenta"), _prj.build.repository
        )
        table = local_images(_prj)
        console.print(text)
        console.print(table)

    if remote:
        text = Text.assemble(
            ("Remote Images for: ", "bold magenta"), _prj.build.repository
        )
        table = remote_images(_prj)
        console.print(text)
        console.print(table)
