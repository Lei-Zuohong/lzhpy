# -*- coding: UTF-8 -*-
# Public package
import os
# Private package
# Internal package


def cmd_build(cmd,
              nohup=False, bkg=False,
              stdout=None, stdout_add=False,
              stderr=None, stderr_add=False,
              **argv):
    '''
    构建命令行
        - addition: 附加参数字符串
        - nohup (bool): 是否脱离终端运行
        - bkg (bool): 是否后台运行
        - stdout (str): 标准输出文件
        - stdout_add (bool): 输出文件是否为增加模式
        - stderr (str): 标准错误文件
        - stderr_add (bool): 输出文件是否为增加模式
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
    return exe


def cmd_run(cmd,
            root=None,
            previous=[],
            **argv):
    '''
    运行命令行
        - root (str): 更改启动目录
        - previous (list): 前置命令
    '''
    if (root is not None):
        os.chdir(root)
    for previou in previous:
        os.system(previou)
    os.system(cmd_build(cmd, **argv))
