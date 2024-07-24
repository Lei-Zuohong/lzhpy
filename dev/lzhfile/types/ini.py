# -*- coding: UTF-8 -*-
# Public package
import configparser
# Private package
# Internal package


def config_read(filename='config.ini'):
    config = configparser.ConfigParser(interpolation=configparser.ExtendedInterpolation())
    config.read(filename, encoding="utf-8-sig")
    return config


def config_write(config, filename='config.ini'):
    with open(filename, 'w') as outfile:
        config.write(outfile)
