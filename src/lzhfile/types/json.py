# -*- coding: UTF-8 -*-
# Public package
import json
# Private package
# Internal package
from ..core import *


def json_read(filename):
    with open(filename, 'r') as infile:
        output = json.load(infile)
    return output


def json_write(filename, target):
    if (split(filename)[0] != ''):
        makedirs(split(filename)[0])
    with open(filename, 'w') as outfile:
        json.dump(target, outfile, indent=4, sort_keys=False)
