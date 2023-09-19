from typing import List
from dataclasses import dataclass


def charge(current: float, voltage: float | None = None, limits: List[bool] = []):
    pass


def discharge(current: float, voltage: float | None = None, limits: List[bool] = []):
    pass


def pause(
    limits: List[bool] = [],
    hours: float | None = None,
    minutes: float | None = None,
    seconds: float | None = None,
):
    pass


def limit(condition: bool, action=None) -> bool:
    pass


def error(errnum: int):
    pass


@dataclass
class time:
    hours: float | None = None
    minutes: float | None = None
    seconds: float | None = None


def register(
    time: time | None = None,
    voltage: float | None = None,
    current: float | None = None,
    format: List | None = None,
):
    pass
