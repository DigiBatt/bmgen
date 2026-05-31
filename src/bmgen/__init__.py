import os

from bmgen.battery import Battery
from bmgen.channel import *
from bmgen.function import *

SPHINX_AUTODOC = False

battery = Battery()
options = {}


def get_version():
    with open(
        os.path.join(os.path.dirname(os.path.realpath(__file__)), "version"), "r"
    ) as version_file:
        return version_file.read().strip()
