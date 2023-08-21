from typing import List


def charge(current: float, voltage: float | None = None, limits: List[bool] = []):
    pass


def discharge(current: float, voltage: float | None = None, limits: List[bool] = []):
    pass


def pause(limits: List[bool] = []):
    pass


def time(
    hours: float | None = None,
    minutes: float | None = None,
    seconds: float | None = None,
) -> bool:
    pass
