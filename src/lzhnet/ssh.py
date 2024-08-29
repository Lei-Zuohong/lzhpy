# -*- coding: UTF-8 -*-
# Public package
import paramiko
# Private package

################################################################################
# 远程利用ssh传输文件
################################################################################


def upload(host, user, password, local_path, server_path, timeout=10):
    '''Upload file to server

    Args:
        host (str): server ip
        user (str): server username
        password (str): server password
        local_path (str): local file path
        server_path (str): server file path
        timeout (int): timeout
    '''
    try:
        t = paramiko.Transport((host, 22))
        t.banner_timeout = timeout
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.put(local_path, server_path)
        t.close()
        return True
    except Exception as e:
        print(e)
        return False


def download(host, user, password, server_path, local_path, timeout=10):
    '''Download file from server

    Args:
        host (str): server ip
        user (str): server username
        password (str): server password
        server_path (str): server file path
        local_path (str): local file path
        timeout (int): timeout

    Returns:
        bool: True if success, False otherwise
    '''
    try:
        t = paramiko.Transport((host, 22))
        t.banner_timeout = timeout
        t.connect(username=user, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        sftp.get(server_path, local_path)
        t.close()
        return True
    except Exception as e:
        print(e)
        return False
