# -*- coding: UTF-8 -*-
# Public package
import os
import time
import tqdm
import subprocess
from threading import Semaphore
# Private package
import lzhlog
# Internal package


################################################################################
# 多进程并发 (使用Popen实现)
################################################################################


class Pool:
    def __init__(self, nthread, show_bar=True):
        self.max_workers = max(1, nthread)
        self.semaphore = Semaphore(self.max_workers)
        self.processes = []  # 存储 (process, command) 元组
        self.show_bar = show_bar
        self.log = lzhlog.get_class_logger(self)

    def _run_command(self, command):
        """执行单个命令并返回进程对象"""
        with self.semaphore:  # 控制并发数量
            try:
                self.log.debug(f"Starting command: {command}")
                process = subprocess.Popen(command,
                                           shell=True,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE)
                return process
            except Exception as e:
                self.log.error(f"Failed to start command: {command}, error: {str(e)}")
                raise

    def apply_asyncs(self, commands):
        """
        并发执行多个shell命令
        :param commands: 要执行的命令列表
        """
        for cmd in commands:
            process = self._run_command(cmd)
            self.processes.append((process, cmd))

    def join(self):
        """等待所有命令执行完成"""
        if self.show_bar:
            self.bar = tqdm.tqdm(total=len(self.processes))

        remaining = self.processes.copy()
        while remaining:
            for process, cmd in remaining[:]:
                retcode = process.poll()
                if retcode is not None:  # 进程已完成
                    remaining.remove((process, cmd))
                    if self.show_bar:
                        self.bar.update(1)

                    # 记录命令输出
                    stdout, stderr = process.communicate()
                    if retcode != 0:
                        self.log.error(
                            f"Command failed (exit {retcode}): {cmd}\n"
                            f"STDERR: {stderr.decode().strip()}"
                        )
                    else:
                        self.log.debug(
                            f"Command succeeded: {cmd}\n"
                            f"STDOUT: {stdout.decode().strip()}"
                        )

            if remaining:
                time.sleep(0.1)  # 避免忙等待

        if self.show_bar:
            self.bar.close()

    def get_results(self):
        """获取所有命令的执行结果(返回码和输出)"""
        results = []
        for process, cmd in self.processes:
            retcode = process.returncode
            stdout, stderr = process.communicate()
            results.append({
                'command': cmd,
                'returncode': retcode,
                'stdout': stdout.decode().strip(),
                'stderr': stderr.decode().strip(),
            })
        return results

    def prt_results(self):
        for result in self.get_results():
            print(f"Command: {result['command']}")
            print(f"Return code: {result['returncode']}")
            if result['stdout']:
                print(f"Output:\n{result['stdout']}")
            if result['stderr']:
                print(f"Errors:\n{result['stderr']}")
            print("-" * 40)


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
    if ('previous' in argv):
        previou = ' && '.join(argv['previous'])
        exe = previou + ' && ' + exe
    return exe


def cmd_run(cmd,
            root=None,
            **argv):
    '''
    运行命令行
        - root (str): 更改启动目录
        - previous (list): 前置命令
    '''
    if (root is not None):
        os.chdir(root)
    os.system(cmd_build(cmd, **argv))
