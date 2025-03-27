#! /bin/env python

import difflib
import io
import os
import sys

import click

from bmgen import bmgen


@click.command()
@click.option("--generate", is_flag=True, default=False)
@click.option("--update", is_flag=True, default=False)
@click.argument("testdir", type=click.Path(dir_okay=True), default="./tests")
def main(generate, update, testdir):
    success = True
    for test in os.listdir(testdir + "/input"):
        testfile = f"{testdir}/input/{test}"
        testname = os.path.splitext(test)[0]
        for target in [
            dir
            for dir in os.listdir(testdir)
            if dir != "input" and os.path.isdir(f"{testdir}/{dir}")
        ]:
            for format in os.listdir(testdir + "/" + target):
                print(f"{testname} - {target} - {format}")
                outfile = f"{testdir}/{target}/{format}/{testname}"
                try:
                    if generate:
                        if not os.path.exists(outfile):
                            bmgen.generate(
                                testfile, target, format, None, outfile, True
                            )
                    elif update:
                        if os.path.exists(outfile):
                            bmgen.generate(
                                testfile, target, format, None, outfile, True
                            )
                    else:
                        if os.path.exists(outfile):
                            output = io.StringIO()
                            bmgen.generate(testfile, target, format, None, output, True)
                            output.seek(0)
                            with open(outfile, "r") as reference:
                                difflines = list(
                                    difflib.unified_diff(
                                        reference.readlines(), output.readlines()
                                    )
                                )
                                if len(difflines) > 0:
                                    success = False
                                    print("\n".join(difflines))
                        else:
                            print("skipped (no reference file)")
                except Exception as e:
                    success = False
                    print(e)
    exit(0 if success else 1)


if __name__ == "__main__":
    main()
