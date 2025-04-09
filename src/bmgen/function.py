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


def limit(condition: bool, action=None):
    """Define a limit for the current program step or the entire program.

    Limits can be defined for one step if they are passed in the `limits` parameter.
    If a limit is defined on its own, it will apply to the entire program. In this case, an action must be specified, e.g. :py:func:`error`.

    :param condition: Condition that will trigger the limit once it is reached.
    :type condition: bool
    :param action: Action to take once the limit condition is met. If this is None, the next step in the program will be executed.
    :type action: _type_, optional
    """
    pass


def error(errnum: int):
    """Set an error as the action for a limit.

    An error will stop the execution of the current program until it is continued by an operator.

    :param errnum: A number specifying what kind of error occured. The meaning of each numbers depends on the selected cycler target.
    :type errnum: int
    """
    pass


def message(errnum: int):
    """Set a message as the action for a limit.

    A message is informational and will not stop the execution of the current program.

    :param errnum: A number specifying what kind of error occured. The meaning of each numbers depends on the selected cycler target.
    :type errnum: int
    """
    pass


@dataclass
class time:
    """Object expressing a timespan that can be used for defining limits.

    The timespan can be set using different units.
    If multiple values are set, the will be converted to one unit and added together, e.g. minutes=1 and seconds=30 will result in seconds=90.
    """

    hours: float | None = None
    minutes: float | None = None
    seconds: float | None = None


def seconds(value: float) -> time:
    """Convenience method to create a :py:class:`time` instance with the :py:attr:`seconds` attribute set.

    :param value: The number of seconds.
    :type value: float
    :rtype: time
    """
    pass


def minutes(value: float) -> time:
    """Convenience method to create a :py:class:`time` instance with the :py:attr:`minutes` attribute set.

    :param value: The number of minutes.
    :type value: float
    :rtype: time
    """
    pass


def hours(value: float) -> time:
    """Convenience method to create a :py:class:`time` instance with the :py:attr:`hours` attribute set.

    :param value: The number of hours.
    :type value: float
    :rtype: time
    """
    pass


def register(
    time: time | None = None,
    voltage: float | None = None,
    current: float | None = None,
    format: List | None = None,
):
    pass
