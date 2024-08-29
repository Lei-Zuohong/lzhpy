# -*- coding: UTF-8 -*-
# Public package
import re
import sys
# Private package
# Internal package


def argv(cmds=sys.argv):
    cmd_list = []
    cmd_dict = {}
    for icmd, cmd in enumerate(cmds):
        check1 = re.match(r'-(.*)', cmd)
        check2 = re.match(r'--(.*)', cmd)
        if (check2):
            if (icmd + 1 >= len(cmds)):
                raise Exception('cmd value is missing.')
            cmd_dict[check2.group(1)] = cmds[icmd + 1]
            passthis = True
        elif (check1):
            cmd_list.append(check1.group(1))
    return cmd_list, cmd_dict


class Argv:
    def __init__(self, cmds=sys.argv) -> None:
        self.args, self.argv = argv(cmds)

    def has(self, key):
        return key in self.argv or key in self.args

    def get(self, key, value, func=None):
        if key in self.argv:
            if (func is None):
                return self.argv[key]
            else:
                return func(self.argv[key])
        else:
            return value
