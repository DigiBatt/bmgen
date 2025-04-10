I: float  #: Current measurement in A.
V: float  #: Voltage measurement in V.
StepCharge: float  #: Charge throughput of the current step in Ah.
T: float  #: Temperature measurement in °C.
Tenv: float  #: Environment temperature measurement in °C.


def channel(name: str) -> float:
    """Define a custom channel.

    :param name: Name of the custom channel that is recognized by the targeted cycler.
    :type name: str
    :return: Channel value that can be used in limits in calculations.
    :rtype: float
    """
    pass
