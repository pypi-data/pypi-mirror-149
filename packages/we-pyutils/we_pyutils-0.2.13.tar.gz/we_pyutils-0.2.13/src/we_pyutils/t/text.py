#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : text.py
@Time    : 2021/8/26 9:26
@Author  : ZENKR
@Email   : zenkr@qq.com
@Software: PyCharm
@Desc    :
@license : Copyright (c) 2021 WingEase Technology Co.,Ltd. All Rights Reserved.
"""
import re


class VariablesReplaceHandler:
    _var_dict: dict = {}
    _content_replaced: str = None

    def __init__(self, content: str, pattern, var_dict: dict, empty_replace: str = ''):
        """
        变量替换处理器
        :param content: 内容文本
        :param pattern: 正则匹配规则
        :param var_dict: 变量字典
        :param empty_replace: 变量不存在替换为
        """
        self._content: str = content
        self._pattern = pattern
        self._var_dict: dict = var_dict if var_dict else {}
        self._empty_replace: str = empty_replace

    def replace(self) -> str:
        self._content_replaced = re.sub(self._pattern, self.replace_methods, self._content)
        return self._content_replaced

    def replace_methods(self, matched) -> str:
        var_name = matched.group('var_name')
        if var_name in self._var_dict:
            return self._var_dict[var_name]
        elif self._empty_replace is not None:
            return self._empty_replace
        else:
            return f'{{{{ {var_name} }}}}'
