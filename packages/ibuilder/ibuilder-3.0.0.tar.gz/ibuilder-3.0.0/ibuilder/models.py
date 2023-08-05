#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#  SPDX-License-Identifier: GPL-3.0-only
#  Copyright 2020 drad <drader@adercon.com>

from enum import Enum
from typing import List

from pydantic import BaseModel

UNITS = {1000: ["KB", "MB", "GB"], 1024: ["KiB", "MiB", "GiB"]}


class VersionIncrementType(str, Enum):
    major = "major"
    minor = "minor"
    patch = "patch"
    default = minor


class ResultStatus(str, Enum):
    initialize = "initialize"
    success = "success"
    user_cancel = "canceled by user"
    build_fail = "build failure"
    push_fail = "push failure"
    source_tag_fail = "source tag failure"


class TaskStatus(str, Enum):
    build_ok = "build ok"
    build_fail = "build failure"
    push_ok = "push ok"
    push_fail = "push failure"
    repush_ok = "repush ok"
    repush_fail = "repush fail"
    source_tag_ok = "source tag ok"
    source_tag_fail = "source tag failure"


class History(BaseModel):
    """Base History."""

    created: str = None
    runtime: float = None
    result: ResultStatus = None
    task_status: List[TaskStatus] = []
    calling_params: str = None
    run_params: dict = None
    last: bool = False


class HistoryOnDB(History):
    """Extended History ."""

    doc_id: str = None
