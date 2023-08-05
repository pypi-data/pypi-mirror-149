#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : file.py
@Time    : 2020-02-09 7:01
@Author  : ZENKR
@Email   : zenkr@qq.com
@Software: PyCharm
@Desc    :
@license : Copyright (c) 2020 WingEase Technology Co.,Ltd. All Rights Reserved.
"""

from os import listdir
from os.path import isfile, join, splitext
from typing import Union

from ruamel import yaml


# 获取文件列表（支持指定扩展名）
def get_file_list(dir_path, extension_list=None):
    file_list = []
    for f in listdir(dir_path):
        if isfile(join(dir_path, f)):
            if extension_list is None or extension_list == []:
                file_list.append(f)
            else:
                if splitext(f)[1] in extension_list:
                    file_list.append(f)
    return file_list


def load_yaml_file(file: str, multiple: bool = False) -> Union[dict, list]:
    """
    读取YAML文件
    @param file: 文件路径
    @param multiple: 同文件内是否包含多个文档
    @return: 字典或列表
    """
    with open(file, 'r', encoding="utf-8") as f:
        yaml_data = f.read()
    if multiple:
        yaml_load = yaml.load_all(yaml_data, Loader=yaml.Loader)
    else:
        yaml_load = yaml.load(yaml_data, Loader=yaml.Loader)
    data_list = []
    for item in yaml_load:
        data_list.append(item)
    return data_list


def export_yaml_file(content: Union[dict, list], path: str, multiple: bool = False):
    """
    保存YAML文件
    @param content: 文件内容
    @param path: 保存文件路径
    @param multiple: 同文件内是否包含多个文档
    @return:
    """
    with open(path, "w", encoding="utf-8") as f:
        if multiple:
            yaml.dump_all(content, f, Dumper=yaml.RoundTripDumper)
        else:
            yaml.dump(content, f, Dumper=yaml.RoundTripDumper)


if __name__ == '__main__':
    f = load_yaml_file('./data/demo.yaml', multiple=True)
    export_yaml_file(f, './data/demo_export.yaml', multiple=True)
    print(0)
