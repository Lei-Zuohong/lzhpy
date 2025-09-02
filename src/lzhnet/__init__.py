# -*- coding: UTF-8 -*-
# Public package
import os
import requests
# Private package
# Internal package


def download(url,
             nfolder=None,
             nfile=None):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        # 处理文件夹
        if (nfolder is None):
            _nfolder = '.'
        else:
            _nfolder = nfolder
        os.makedirs(_nfolder, exist_ok=True)
        # 处理文件名
        if (nfile is None):
            _nfile = os.path.basename(url.split('?')[0])
        else:
            _nfile = nfile
        # 下载
        with open(os.path.join(_nfolder, _nfile), 'wb') as fopen:
            for chunk in response.iter_content(1024):
                fopen.write(chunk)
        return os.path.join(_nfolder, _nfile)
    except requests.exceptions.RequestException as e:
        print(f"下载失败: {e}")
        return None
