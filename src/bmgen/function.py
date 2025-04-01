from dataclasses import dataclass
from typing import List

from bmgen.stepinfo import StepInfo


def charge(
    current: float,
    voltage: float | None = None,
    limits: List[bool] = [],
    registrations: List = [],
) -> StepInfo:
    """Charge the battery connected to the cycler circuit.

    :param current: Current setpoint in Ampere.
    :type current: float
    :param voltage: Voltage setpoint in Volt, defaults to None.
    :type voltage: float | None
    :param limits: List of limits, see the :py:func:`limit` function, defaults to [].
    :type limits: List[bool]
    :param registrations: List of registrations, see the :py:func:`register` function, defaults to [].
    :type registrations: List
    :return: :py:class:`StepInfo` object containing information about the executed step.
    :rtype: StepInfo
    """
    pass


def discharge(
    current: float,
    voltage: float | None = None,
    limits: List[bool] = [],
    registrations: List = [],
) -> StepInfo:
    """Discharge the battery connected to the cycler circuit.

    :param current: Current setpoint in Ampere.
    :type current: float
    :param voltage: Voltage setpoint in Volt, defaults to None.
    :type voltage: float | None
    :param limits: List of limits, see the :py:func:`limit` function, defaults to [].
    :type limits: List[bool]
    :param registrations: List of registrations, see the :py:func:`register` function, defaults to [].
    :type registrations: List
    :return: :py:class:`StepInfo` object containing information about the executed step.
    :rtype: StepInfo
    """
    pass


def pause(
    limits: List[bool] = [],
    hours: float | None = None,
    minutes: float | None = None,
    seconds: float | None = None,
    registrations: List = [],
) -> StepInfo:
    """Pause the program until a limit is reached.

    Limits can be set using the `limit` argument.
    The arguments `hours`, `minutes`, and `seconds` are provided as a shorthand to set a time-based limit.
    They act the same way as the the :py:func:`time` function.

    :param limits: List of limits, see the :py:func:`limit` function, defaults to [].
    :type limits: List[bool], optional
    :param hours: Hours of the time-based limit, defaults to None.
    :type hours: float | None, optional
    :param minutes: Minutes of the time-based limit, defaults to None.
    :type minutes: float | None, optional
    :param seconds: Seconds of the time-based limit, defaults to None.
    :type seconds: float | None, optional
    :param registrations: List of registrations, see the :py:func:`register` function, defaults to [].
    :type registrations: List, optional
    :return: :py:class:`StepInfo` object containing information about the executed step.
    :rtype: StepInfo
    """
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
