# -*- coding: utf-8 -*-

import json
import uuid

import requests
from fn import _
from owlmixin.owlcollections import TList

from todoistools.models import TodoistApiTask, PendulumDate

TODOIST_API_URL = 'https://todoist.com/API/v7'


def fetch_uncompleted_tasks(todoist_token: str, date: PendulumDate) -> TList[TodoistApiTask]:
    items = requests.get(f"{TODOIST_API_URL}/sync", params={
        "token": todoist_token,
        "sync_token": "*",
        "resource_types": '["items"]'
    }).json()['items']

    return TodoistApiTask.from_dicts(items, restrict=False)\
        .reject(_.checked)\
        .filter(lambda x: x.due_date_utc.map(
                lambda y: y.in_tz('Asia/Tokyo').format('YYYY-MM-DD')).get() == date.format('YYYY-MM-DD'))


def update_day_orders(todoist_token: str, ids: TList[str]) -> bool:
    commands = [{
        "type": "item_update_day_orders",
        "uuid": str(uuid.uuid4()),
        "args": {
            "ids_to_orders": {x: i+1 for i, x in enumerate(ids)},
        }
    }]

    r = requests.get(f"{TODOIST_API_URL}/sync", params={
        "token": todoist_token,
        "commands": json.dumps(commands)
    })

    return r.ok
