import os
import importlib.metadata

from bmgen.battery import Battery
from bmgen.channel import *
from bmgen.function import *

SPHINX_AUTODOC = False

battery = Battery()
options = {}


def get_version():
    return importlib.metadata.version("bmgen")