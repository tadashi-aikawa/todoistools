#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import sys
import random

import fire
from fn import _
from typing import List

from owlmixin import TList

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(PROJECT_ROOT)

from todoistools import api
from todoistools.models import PendulumDate, TodoistApiTask, Config


def to_times(task: TodoistApiTask) -> List[str]:
    return ["".join(x.split(":")).zfill(4) for x in re.findall("\d+:\d+", task.content)]


def sort(config="config.yml", dry=False):
    conf: Config = Config.from_yamlf(config)

    scheduled_tasks, free_tasks = api.fetch_uncompleted_tasks(
        conf.token, PendulumDate.today()
    ).partial(to_times)

    work_tasks, not_work_tasks = free_tasks.partial(lambda x: x.project_id in conf.work_project_ids)

    sorted_tasks: TList[TodoistApiTask] = (
        scheduled_tasks.order_by(lambda x: to_times(x))
        .concat(not_work_tasks, first=True)
        .concat(work_tasks, first=False)
    )

    if dry:
        print(sorted_tasks.map(lambda x: x.content).to_yaml())
    else:
        is_success = api.update_day_orders(conf.token, sorted_tasks.map(_.id))
        print("success" if is_success else "failure update")


def main():
    fire.Fire()


if __name__ == "__main__":
    main()
