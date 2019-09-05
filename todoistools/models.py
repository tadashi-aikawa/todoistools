# -*- coding: utf-8 -*-

import pendulum
from pendulum import DateTime
from owlmixin import OwlMixin, TList, TOption
from owlmixin.transformers import ValueTransformer


class PendulumDate(DateTime, ValueTransformer):
    @classmethod
    def from_value(cls, value: str) -> 'PendulumDate':
        origin: DateTime = pendulum.parse(value, strict=False)
        return cls(
            year=origin.year,
            month=origin.month,
            day=origin.day,
            hour=origin.hour,
            minute=origin.minute,
            second=origin.second,
            microsecond=origin.microsecond,
            tzinfo=origin.tzinfo
        )

    def to_value(self, ignore_none: bool, force_value: bool) -> str:
        return self.isoformat()



class Due(OwlMixin):
    date: PendulumDate
    is_recurring: bool
    lang: str


class TodoistApiTask(OwlMixin):
    id: int
    content: str
    priority: int
    project_id: int
    labels: TList[int]
    checked: int
    due: TOption[Due]
    day_order: TOption[int]


class Config(OwlMixin):
    token: str

