# -*- coding: UTF-8 -*-
# Public package
import os
import itertools
# Private package
# Internal package


class FileBase:
    def __init__(self, path, keys=[]):
        self.path = path
        self.keys = keys

    def __getitem__(self, key):
        return FileBase(os.path.join(self.path, key), self.auth, self.keys[1:])

    def get_path(self, *args, **argv):
        if (len(args) == self.depth()):
            return os.path.join(self.path, *args)
        elif (len(argv) == self.depth()):
            for key in self.keys:
                if (key not in argv):
                    raise ValueError('Must indicate key %s in FileBase' % (key))
            return os.path.join(self.path, *[argv[key] for key in self.keys])
        else:
            raise ValueError('Must indicate %d keys in FileBase' % (self.depth()))

    def get_paths(self, *argss, **argvs):
        if (len(argss) == self.depth()):
            prods = itertools.product(*argss)
            output = [self.path(*list(prod)) for prod in prods]
            return output
        elif (len(argvs) == self.depth()):
            for key in self.keys:
                if (key not in argvs):
                    raise ValueError('Must indicate key %s in FileBase' % (key))
            prods = itertools.product(*[argvs[key] for key in self.keys])
            output = [self.path(*list(prod)) for prod in prods]
            return output
        else:
            raise ValueError('Must indicate %d keys in FileBase' % (self.depth()))

    def is_missing(self, *args, **argv):
        return not os.path.exists(self.get_path(*args, **argv))

    def missing(self, *argss, **argvs):
        if (len(argss) == self.depth()):
            prods = itertools.product(*argss)
            output = [list(prod) for prod in prods if not os.path.exists(self.get_path(*list(prod)))]
            return output
        elif (len(argvs) == self.depth()):
            for key in self.keys:
                if (key not in argvs):
                    raise ValueError('Must indicate key %s in FileBase' % (key))
            prods = itertools.product(*[argvs[key] for key in self.keys])
            output = [list(prod) for prod in prods if not os.path.exists(self.get_path(*list(prod)))]
            return output
        else:
            raise ValueError('Must indicate %d keys in FileBase' % (self.depth()))

    def depth(self):
        return len(self.keys)


class FileBases:
    def __init__(self):
        self.wfb = None
        self.fbs = {}

    def regist(self, name, path, keys=[], auth=['r']):
        self.fbs[name] = FileBase(path, keys=keys)
        if ('w' in auth):
            if (self.wfb is not None):
                raise ValueError('Only one FileBase can be writeable')
            self.wfb = FileBase(path, keys=keys)

    def rpath(self, name, *args, **argv):
        return self.fbs[name].get_path(*args, **argv)

    def wpath(self, name, *args, **argv):
        return self.wfb.get_path(*args, **argv)
