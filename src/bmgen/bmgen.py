#! /usr/bin/python3.10

import ast
import io
import json
import sys
from importlib import import_module

import astor
import click

import bmgen
from bmgen.battery import PredefindedBattery
from bmgen.transformer import Transformer


@click.command()
@click.argument("filename", required=True)
@click.option("-t", "--target", default="bm")
@click.option("-f", "--format")
@click.option("-i", "--intermediate")
@click.option("-o", "--out")
@click.option("--no-timestamps", is_flag=True, default=False)
@click.option("--battery")
@click.option("-c", "--config")
def main(
    filename,
    target,
    format,
    intermediate,
    out,
    no_timestamps=False,
    battery=None,
    config=None,
):
    generate(
        filename, target, format, intermediate, out, no_timestamps, battery, config
    )


def generate(
    file,
    target,
    format,
    intermediate,
    out,
    no_timestamps=False,
    battery=None,
    config=None,
):
    bmgen.options = {}
    if config:
        if isinstance(config, dict):
            bmgen.options = config
        elif config == "-":
            bmgen.options = json.load(sys.stdin)
        else:
            with open(config, "r") as f:
                bmgen.options = json.load(f)
    if not "no-timestamps" in bmgen.options:
        bmgen.options["no-timestamps"] = no_timestamps

    if file == "-":
        program = sys.stdin.read()
    elif isinstance(file, str):
        with open(file, "r") as f:
            program = f.read()
    else:
        program = file.read()

    tree = ast.parse(program)

    if intermediate == "ast":
        output(out, ast.dump(tree, indent=2))
        return

    target_module = import_module(f"bmgen.targets.{target}")
    newtree = target_module.Transformer(target).visit(tree)
    newtree = ast.fix_missing_locations(newtree)
    if intermediate == "flat":
        output(out, astor.to_source(newtree))
        return

    if intermediate == "flatast":
        output(out, ast.dump(newtree, indent=2))
        return

    if not format:
        format = target_module.default_format
    FormatGenerator = getattr(
        import_module(f"bmgen.targets.{target}.generators.{format}_generator"),
        f"{format.capitalize()}Generator",
    )
    target_module.generator = FormatGenerator()
    if battery:
        if isinstance(battery, dict):
            target_battery = PredefindedBattery(**battery)
        else:
            with open(battery, "r") as f:
                target_battery = PredefindedBattery(**json.load(f))
    elif "battery" in bmgen.options and bmgen.options.get("predefinedBattery", True):
        target_battery = PredefindedBattery(**bmgen.options["battery"])
    else:
        target_battery = getattr(
            import_module(f"bmgen.targets.{target}.battery"), "battery"
        )
    target_module.battery = target_battery
    exec(compile(newtree, filename="<ast>", mode="exec"), {})
    if intermediate == "targetast":
        output(out, target_module.generator.ast())
    else:
        output(out, target_module.generator.generate())


def output(target, text):
    if target:
        if isinstance(target, str):
            if isinstance(text, str):
                with open(target, "w") as f:
                    f.write(text)
            else:
                with open(target, "wb") as f:
                    f.write(text)
        else:
            if isinstance(target, io.BytesIO) and isinstance(text, str):
                target.write(text.encode())
            else:
                target.write(text)
    else:
        print(text)
