#! /usr/bin/python3.10

import ast
import astor
import sys
from bmgen.transformer import Transformer
import click
import bmgen
from importlib import import_module


@click.command()
@click.argument("filename", required=True)
@click.option("-t", "--target", default="bm")
@click.option("-f", "--format")
@click.option("-i", "--intermediate")
@click.option("-o", "--out")
def main(filename, target, format, intermediate, out):
    generate(filename, target, format, intermediate, out)


def generate(file, target, format, intermediate, out):
    filename = None
    if file == "-":
        program = sys.stdin.read()
    elif isinstance(file, str):
        with open(file, "r") as f:
            program = f.read()
        filename = file
    else:
        program = file.read()

    tree = ast.parse(program)

    if intermediate == "ast":
        output(out, ast.dump(tree, indent=2))
        return

    newtree = Transformer(target).visit(tree)
    newtree = ast.fix_missing_locations(newtree)
    if intermediate == "flat":
        output(out, astor.to_source(newtree))
        return

    if intermediate == "flatast":
        output(out, ast.dump(newtree, indent=2))
        return

    target_module = import_module(f"bmgen.targets.{target}")
    if not format:
        format = target_module.default_format
    FormatGenerator = getattr(
        import_module(f"bmgen.targets.{target}.generators.{format}_generator"),
        f"{format.capitalize()}Generator",
    )
    target_module.generator = FormatGenerator()
    exec(compile(newtree, filename="<ast>", mode="exec"))
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
            target.write(text)
    else:
        print(text)
