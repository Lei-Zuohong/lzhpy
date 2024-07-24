# -*- coding: UTF-8 -*-
# Public package
import sys
import json
import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
# Private package
import lzhlog
# Internal package

################################################################################
# 网页模拟操作
################################################################################


class Chrome():
    def __init__(self, debug=True, sleep=1):
        '''A chrome browser

        Args:
            debug (bool): 是否显示浏览器
            sleep (int): 操作间隔时间
        '''
        self.debug = debug
        self.sleep = sleep

    @lzhlog.dec_timer
    def init(self):
        '启动浏览器'
        options = Options()
        if (self.debug):
            options.headless = False
        else:
            options.headless = True
        self.driver = webdriver.Chrome(options=options)
        self.wait = WebDriverWait(self.driver, 5)

    @lzhlog.dec_timer
    def dump_cookie(self, filename='cookies.txt'):
        '保存cookie到文件'
        self.log.info('Please type anything to dump cookies')
        input()
        with open(filename, 'w') as f:
            f.write(json.dumps(self.driver.get_cookies()))

    @lzhlog.dec_timer
    def load_cookie(self, filename='cookies.txt'):
        '加载cookie文件'
        self.driver.delete_all_cookies()
        with open(filename, 'r') as f:
            cookies = json.load(f)
            for cookie in cookies:
                self.driver.add_cookie(cookie)
        self.driver.refresh()

    @lzhlog.dec_timer
    def clear(self):
        self.driver.delete_all_cookies()

    @lzhlog.dec_timer
    def close(self):
        self.driver.close()

    @lzhlog.dec_timer
    def sl(self, sleep=None):
        if (sleep is None):
            time.sleep(self.sleep)
        else:
            time.sleep(sleep)

    @lzhlog.dec_timer
    def get(self, url):
        self.driver.get(url)

    @lzhlog.dec_timer
    def fail_handler(self):
        self.init()

################################################################################
# 网络下载文件
################################################################################


def download(url, file_path):
    '''Download file from url

    Args:
        url (str): string, 下载地址
        file_path (str): string, 文件储存地址
    '''
    # 关闭网站证书
    r = requests.get(url, stream=True, verify=False)
    # 文件大小
    total_size = int(r.headers['Content-Length'])
    temp_size = 0
    # 写入文件
    with open(file_path, "wb") as f:
        # 指定单元大小
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                temp_size += len(chunk)
                f.write(chunk)
                f.flush()
                ############# 花哨的下载进度部分###############
                done = int(50 * temp_size / total_size)
                # 调用标准输出刷新命令行，看到\r回车符了吧
                # 相当于把每一行重新刷新一遍
                sys.stdout.write("\r[%s%s] %d%% %s" % (
                    '*' * done, ' ' * (50 - done), 100 * temp_size / total_size, file_path))
                sys.stdout.flush()
    print()  # 避免上面\r 回车符，执行完后需要换行了，不然都在一行显示
