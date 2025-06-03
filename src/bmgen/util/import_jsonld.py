from enum import Enum

import bmgen.targets.python.ast as ast


class FUNCTION_ARGS(Enum):
    CURRENT = 0
    VOLTAGE = 1
    LIMIT = 2
    TIME = 3


TASK_TYPES = {
    "ConstantCurrentConstantVoltageCharging": "charge",
    "ConstantCurrentCharging": "charge",
    "ConstantCurrentConstantVoltageDischarging": "discharge",
    "ConstantCurrentDischarging": "discharge",
    "Resting": "pause",
}

PROCESS_PARAMETER_TYPES = {
    "ChargingCurrent": FUNCTION_ARGS.CURRENT,
    "ChargingVoltage": FUNCTION_ARGS.VOLTAGE,
    "TerminationQuantity": (FUNCTION_ARGS.LIMIT, "I", "<", "Ampere"),
    "StepDuration": (FUNCTION_ARGS.TIME, "Second"),
    "DischargingCurrent": FUNCTION_ARGS.CURRENT,
    "LowerVoltageLimit": (FUNCTION_ARGS.LIMIT, "V", "<", "Volt"),
    "UpperVoltageLimit": (FUNCTION_ARGS.LIMIT, "V", ">", "Volt"),
}


def import_jsonld(j):
    program = ast.Program()
    program.statements.append(ast.Import("bmgen.function", ["*"]))
    program.statements.append(ast.Import("bmgen.channel", ["*"]))
    t = j["hasTask"]
    while t is not None:
        program.statements.append(convert_task(t))
        t = t.get("hasNext", None)

    return program


def convert_task(j):
    taskType = j.get("@type", None)
    if taskType is None:
        raise Exception("Task must have a @type")
    if taskType not in TASK_TYPES:
        raise Exception(f"Unknown task type {taskType}")
    current = None
    voltage = None
    limits = []
    for p in j["hasProcessParameter"]:
        paramType = p.get("@type", None)
        if paramType is None:
            raise Exception("Process parameter must have a @type")
        if paramType not in PROCESS_PARAMETER_TYPES:
            raise Exception(f"Unknown process parameter type {paramType}")
        match PROCESS_PARAMETER_TYPES[paramType]:
            case FUNCTION_ARGS.CURRENT:
                current = convert_value(p, "Ampere")
            case FUNCTION_ARGS.VOLTAGE:
                voltage = convert_value(p, "Volt")
            case (FUNCTION_ARGS.LIMIT, variable, operator, unit):
                limits.append(
                    ast.BinaryOperation(
                        operator,
                        ast.Variable(variable),
                        convert_value(p, unit),
                    )
                )
            case (FUNCTION_ARGS.TIME, unit):
                limits.append(
                    ast.FunctionCall(
                        "time", kwargs={"seconds": convert_value(p, "Second")}
                    )
                )
    kwargs = {}
    # TODO: figure out proper pause steps
    if taskType == "ConstantCurrentCharging" and current.value == 0:
        taskType = "Resting"
        current = None
    if current:
        kwargs["current"] = current
    if voltage:
        kwargs["voltage"] = voltage
    kwargs["limits"] = ast.ListLiteral(limits)
    return ast.FunctionCall(TASK_TYPES[taskType], kwargs=kwargs)


def convert_value(v, unit):
    givenUnit = v["hasMeasurementUnit"]["@type"]
    if unit != givenUnit:
        raise Exception(
            f"Unexpected unit {givenUnit} for process parameter value, should be {unit}"
        )
    return ast.NumberLiteral(v["hasNumericalPart"]["hasNumberValue"])
