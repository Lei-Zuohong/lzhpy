# -*- coding: UTF-8 -*-
# Public package
import os
import shutil
from compileall import compile_dir
# Private package
# Internal package
from .path import *


def mv(path_source, path_target):
    shutil.move(path_source, path_target)


def rm(path):
    if (os.path.isdir(path)):
        shutil.rmtree(path)
    elif (os.path.exists(path)):
        os.remove(path)


def makedirs(path):
    os.makedirs(path, exist_ok=True)


def copy_file(source='', target=''):
    source_path, source_name = split(source)
    target_path, target_name = split(target)
    if (target_name in os.listdir(target_path)):
        os.remove('%s/%s' % (target_path, target_name))
    shutil.copy('%s/%s' % (source_path, source_name),
                '%s' % (target_path))
    if (source_name != target_name):
        shutil.move('%s/%s' % (target_path, source_name),
                    '%s/%s' % (target_path, target_name))


def copy_folder(source='', target='', delete_origin=True):
    source_path, source_name = split(source)
    target_path, target_name = split(target)
    if (delete_origin):
        if (target_name in os.listdir(target_path)):
            shutil.rmtree('%s/%s' % (target_path, target_name))
    shutil.copytree('%s/%s' % (source_path, source_name),
                    '%s/%s' % (target_path, target_name))


def copy(source='', target=''):
    if (os.path.isfile(source)):
        copy_file(source, target)
    else:
        copy_folder(source, target)


def pycache_remove(folder):
    for root, dirs, files in os.walk(folder, topdown=False):
        for dir_name in dirs:
            if dir_name == "__pycache__":
                dir_path = os.path.join(root, dir_name)
                print(f"Deleting {dir_path}")
                shutil.rmtree(dir_path)


def pycache_compile(folder):
    pycache_remove(folder)
    compile_dir(folder)
    for root, subdir, files in os.walk(folder):
        for _file in files:
            if _file.endswith(".py"):
                os.remove(os.path.join(root, _file))
            if _file.endswith(".pyc") and len(_file.split(".")) == 3:
                _file_tmp = _file.replace("." + _file.split(".")[1], "")
                shutil.move(
                    os.path.join(root, _file),
                    os.path.join(os.path.dirname(root), _file_tmp))
        if root.endswith("__pycache__"):
            os.rmdir(root)
