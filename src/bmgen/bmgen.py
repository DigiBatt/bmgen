#! /usr/bin/python3.10

import ast
import astor
import sys
from bmgen.transformer import Transformer


def main():
    filename = sys.argv[1]
    target = "bm"
    with open(filename, "r") as f:
        tree = ast.parse(f.read())

    # print(ast.dump(tree, indent=2))

    newtree = Transformer(target).visit(tree)
    print(astor.to_source(newtree))
