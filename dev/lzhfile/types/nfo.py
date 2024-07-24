# -*- coding: UTF-8 -*-
# Public package
import re
# Private package
# Internal package
from .txt import *


def nfo_read(path):
    tags = {}
    lines = txt_readlines(path)
    for line in lines:
        check = re.search(r'<([a-z]*)>(.*)</([a-z]*)>', line)
        if (check):
            if (check.group(1) == check.group(3)):
                tag = check.group(1)
                value = check.group(2)
                if (tag in tags):
                    if (isinstance(tags[tag], list)):
                        tags[tag].append(value)
                    else:
                        tags[tag] = [tags[tag], value]
                else:
                    tags[tag] = value
    return tags
