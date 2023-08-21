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
    if filename == "-":
        tree = ast.parse(sys.stdin.read())
    else:
        with open(filename, "r") as f:
            tree = ast.parse(f.read())

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
    if format:
        FormatGenerator = getattr(
            import_module(f"bmgen.targets.{target}.generators.{format}_generator"),
            f"{format.capitalize()}Generator",
        )
        target_module.generator = FormatGenerator()
    exec(compile(newtree, filename="<ast>", mode="exec"))
    output(out, target_module.generator.generate())


def output(target, text):
    if target:
        with open(target, "w") as f:
            f.write(text)
    else:
        print(text)
