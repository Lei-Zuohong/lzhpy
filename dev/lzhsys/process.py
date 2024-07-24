# -*- coding: UTF-8 -*-
# Public package
import os
import time
import tqdm
import numpy
import multiprocessing
# Private package
import lzhlog
# Internal package


################################################################################
# 多进程并发
################################################################################


def cmd_build(cmd,
              addition=None,
              nohup=False,
              background=False,
              stdout=None,
              stdout_add=True,
              stderr=None,
              stderr_add=True,
              **argv):
    '''
    构建命令行
        - addition: 附加参数字符串
        - nohup (bool): 是否使用nohup
        - background (bool): 是否后台运行
        - stdout (str): 标准输出文件
        - stdout_add (bool): 输出文件是否为增加模式
        - stderr (str): 标准错误文件
        - stderr_add (bool): 输出文件是否为增加模式
    '''
    exe = cmd
    if (addition is not None):
        exe += ' ' + addition
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
    if (background):
        exe += ' &'
    return exe


def cmd_run(cmd,
            root=None,
            previous=None,
            **argv):
    '''
    运行命令行
        - root (str): 更改启动目录
        - previous (list): 前置命令
    '''
    if (root is not None):
        os.chdir(root)
    if (previous is not None):
        for previou in previous:
            os.system(previou)
    os.system(cmd_build(cmd, **argv))


def error_callback(log, name):
    def output(value):
        log.error('Process No.%s: %s' % (name, value))
    return output


class Pool:
    def __init__(self, nthread, progress=True):
        self.pool = multiprocessing.Pool(nthread)
        self.processes = []
        self.progress = progress
        self.log = lzhlog.get_class_logger(self)

    def apply_async(self, *args, **argv):
        self.processes.append(self.pool.apply_async(*args, **argv))

    def apply_asyncs(self, *args, **argv):
        '''
        并发运行函数
        可选两种参数传递模式
            - 传递多个args，传递通用argv
            - apply_asyncs(func, argss, **argv)
            - 传递多个args，传递多个argv
            - apply_asyncs(func, argss, argvs)
        '''
        if (len(args) == 2):
            func = args[0]
            argss = args[1]
            for args in argss:
                self.apply_async(func,
                                 args=args,
                                 kwds=argv,
                                 error_callback=error_callback(self.log, '%d' % (len(self.processes))))
        elif (len(args) == 3):
            func = args[0]
            argss = args[1]
            argvs = args[2]
            for count, args in enumerate(argss):
                self.apply_async(func,
                                 args=args,
                                 kwds=argvs[count],
                                 error_callback=error_callback(self.log, '%d' % (len(self.processes))))

    def shell_asyncs(self, *args, **argv):
        '''
        并发运行命令行
        可选两种参数传递模式
            - 传递通用argv
            - shell_asyncs(commands, **argv)
            - 传递多个argv
            - shell_asyncs(commands, argvs)
        '''
        if (len(args) == 1):
            commands = args[0]
            for command in commands:
                self.apply_async(cmd_run,
                                 args=(command,),
                                 kwds=argv)
        elif (len(args) == 2):
            commands = args[0]
            argvs = args[1]
            for count, command in enumerate(commands):
                self.apply_async(cmd_run,
                                 args=(command,),
                                 kwds=argvs[count])

    def close(self):
        self.pool.close()

    def join(self):
        self.close()
        self.bar = tqdm.tqdm(total=len(self.processes))
        while (self.bar.n < len(self.processes)):
            try:
                self.bar.update(numpy.sum([process.ready() for process in self.processes]) - self.bar.n)
                time.sleep(1)
            except KeyboardInterrupt:
                self.pool.terminate()
                exit()
        self.bar.close()
        self.pool.join()

    def get(self):
        return [process.get() for process in self.processes]
