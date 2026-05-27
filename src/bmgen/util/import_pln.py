#! /usr/bin/env python3

from bmgen.targets.basytec.formats.pln import Program
import sys


def import_pln(buffer):
    program = Program.fromPln(buffer)
    print(program)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: import_pln.py <program file>")
        sys.exit(1)

    filename = sys.argv[1]
    with open(filename, "rb") as f:
        import_pln(f)
