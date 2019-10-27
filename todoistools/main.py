#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import os
import sys
import random

import fire
from fn import _
from typing import List

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.append(PROJECT_ROOT)

from todoistools import api
from todoistools.models import PendulumDate, TodoistApiTask, Config


def to_times(task: TodoistApiTask) -> List[str]:
    return [''.join(x.split(':')).zfill(4) for x in re.findall('\d+:\d+', task.content)]


def sort(config='config.yml', randomize=False):
    conf: Config = Config.from_yamlf(config)

    scheduled_tasks, free_tasks = api.fetch_uncompleted_tasks(conf.token, PendulumDate.today())\
        .partial(to_times)

    sorted_tasks: TList[TodoistApiTask] = scheduled_tasks\
        .order_by(lambda x: to_times(x))\
        .concat(free_tasks.filter(_.labels), first=True)\
        .concat(free_tasks.reject(_.labels), first=False)

    if randomize:
        print('Sort randomize')
        random.shuffle(sorted_tasks)

    if api.update_day_orders(conf.token, sorted_tasks.map(_.id)):
        print('success')
    else:
        print('failure update')


def main():
    fire.Fire()


if __name__ == '__main__':
    main()


