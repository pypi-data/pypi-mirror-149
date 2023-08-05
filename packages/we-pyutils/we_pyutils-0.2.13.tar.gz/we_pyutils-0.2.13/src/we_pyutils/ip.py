#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : ip.py
@Time    : 2022/3/14 19:30
@Author  : ZENKR
@Email   : zenkr@qq.com
@Software: PyCharm
@Desc    :
@license : Copyright (c) 2022 WingEase Technology Co.,Ltd. All Rights Reserved.
"""
import json

import requests

from we_pyutils.settings import get_wepyutils_setting


def get_my_ip(url: str = None, tries: int = 3, count: int = 1):
    """
    获取当前IP地址
    :param tries: 尝试次数
    :param count: 当前次数
    :return: IP 或 None
    """
    if not url:
        url = get_wepyutils_setting('get_my_ip_url')
    if count <= tries:
        print(f'Try to get my IP.')
        try:
            headers = {
                'Accept-Encoding': 'application/json',
            }
            req = requests.get(url, headers=headers)
            content = str(req.content, encoding='utf-8')
            my_ip = json.loads(content)['ip']
            if my_ip:
                return my_ip
            print(f'Retrying get ip.')
            return get_my_ip(tries=tries, count=count + 1)
        except Exception as e:
            print(f'Can not get my IP. detail: {e}')
            return get_my_ip(tries=tries, count=count + 1)
    print(f'Get ip: too many attempts')
    return ''


if __name__ == '__main__':
    ip = get_my_ip()
    pass
