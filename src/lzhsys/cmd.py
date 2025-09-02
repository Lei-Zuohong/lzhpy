# -*- coding: UTF-8 -*-
# Public package
import os
import subprocess
# Private package
# Internal package


def build(cmd,  # 构建命令行
          nohup: bool = False,
          stdout: str = None,
          stdout_add: bool = False,
          stderr: str = None,
          stderr_add: bool = False,
          bkg: bool = False,
          previous: list = None,
          root: str = None):
    '''
    - nohup: 是否脱离终端运行
    - stdout: 标准输出文件
    - stdout_add: 输出文件是否为增加模式
    - stderr: 标准错误文件
    - stderr_add: 输出文件是否为增加模式
    - bkg: 是否后台运行
    - previous: 前置命令
    - root: 运行目录
    '''
    exe = cmd
    if (nohup):
        exe = 'nohup ' + exe
    if (stdout is not None):
        if (stdout_add):
            exe += ' 1>>%s' % (stdout)
        else:
            exe += ' 1>%s' % (stdout)
    if (stderr is not None):
        if (stderr_add):
            exe += ' 2>>%s' % (stderr)
        else:
            exe += ' 2>%s' % (stderr)
    if (bkg):
        exe += ' &'
    if (previous is not None):
        previou = ' && '.join(previous)
        exe = previou + ' && ' + exe
    if (root is not None):
        exe = 'cd %s' % (root) + ' && ' + exe
    return exe


def popen(cmd):  # 运行指令，即时屏幕输出，返回退出值
    env = dict(os.environ)
    if ('PYTHONPATH' not in env):
        env['PYTHONPATH'] = ''
    env['PYTHONUNBUFFERED'] = '1'
    with subprocess.Popen(cmd,
                          shell=True,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,
                          bufsize=1,
                          env=env,
                          text=True) as process:
        for line in iter(process.stdout.readline, ''):
            print(line, end='')  # 不添加额外的换行符，因为line已经包含
        process.wait()
        output = process.returncode
    return output
