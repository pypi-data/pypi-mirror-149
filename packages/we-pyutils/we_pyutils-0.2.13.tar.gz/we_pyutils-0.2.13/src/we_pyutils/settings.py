#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : settings.py
@Time    : 2022/3/14 19:22
@Author  : ZENKR
@Email   : zenkr@qq.com
@Software: PyCharm
@Desc    :
@license : Copyright (c) 2022 WingEase Technology Co.,Ltd. All Rights Reserved.
"""

WEPYUTILS_DEFAULTS = {
    'get_my_ip_url': 'https://itool.co/get_ip',
}


def get_wepyutils_setting(name, default=None):
    """Read a setting."""
    # Start with a copy of default settings
    WEPYUTILS = WEPYUTILS_DEFAULTS.copy()

    # Override with user settings from settings.py
    # BOOTSTRAP4.update(getattr(settings, "BOOTSTRAP4", {}))

    # Update use_i18n
    # WEPYUTILS["use_i18n"] = i18n_enabled()

    return WEPYUTILS.get(name, default)
