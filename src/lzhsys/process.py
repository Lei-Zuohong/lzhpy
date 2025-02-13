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
from .cmd import cmd_run


################################################################################
# 多进程并发
################################################################################


def error_callback(log, name):
    def output(value):
        log.error('Process No.%s: %s' % (name, value))
    return output


class Pool:
    def __init__(self, nthread, progress=True):
        if (multiprocessing.current_process().name == 'MainProcess'):
            self.pool = multiprocessing.Pool(nthread)
            self.processes = []
            self.progress = progress
        else:
            self.processes = []
            self.results = []
        self.log = lzhlog.get_class_logger(self)

    def apply_async(self, *args, **argv):
        if (multiprocessing.current_process().name == 'MainProcess'):
            self.processes.append(self.pool.apply_async(*args, **argv))
        else:
            self.processes.append([args, argv])

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
        if (multiprocessing.current_process().name == 'MainProcess'):
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
        else:
            for process in self.processes:
                self.results.append(process[0][0](*process[1]['args'],
                                                  **process[1]['kwds']))

    def get(self):
        if (multiprocessing.current_process().name == 'MainProcess'):
            return [process.get() for process in self.processes]
        else:
            return self.results
