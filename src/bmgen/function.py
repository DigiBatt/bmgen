from dataclasses import dataclass
from typing import List

from bmgen.stepinfo import StepInfo


def charge(
    current: float,
    voltage: float | None = None,
    limits: List[bool] = [],
    registrations: List = [],
) -> StepInfo:
    pass


def discharge(
    current: float,
    voltage: float | None = None,
    limits: List[bool] = [],
    registrations: List = [],
) -> StepInfo:
    pass


def pause(
    limits: List[bool] = [],
    hours: float | None = None,
    minutes: float | None = None,
    seconds: float | None = None,
    registrations: List = [],
) -> StepInfo:
    pass


def limit(condition: bool, action=None) -> bool:
    pass


def error(errnum: int):
    pass


def message(errnum: int):
    pass


@dataclass
class time:
    hours: float | None = None
    minutes: float | None = None
    seconds: float | None = None


def seconds(value: float) -> time:
    pass


def minutes(value: float) -> time:
    pass


def hours(value: float) -> time:
    pass


def register(
    time: time | None = None,
    voltage: float | None = None,
    current: float | None = None,
    format: List | None = None,
):
    pass
