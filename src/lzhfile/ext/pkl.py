# -*- coding: UTF-8 -*-
# Public package
import pickle
# Private package
# Internal package


def pkl_read(filename):
    with open(filename, 'rb') as infile:
        output = pickle.load(infile)
    return output


def pkl_dump(filename, target):
    with open(filename, 'wb') as outfile:
        pickle.dump(target, outfile)
