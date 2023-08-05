#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : setup.py
@Time    : 2020-01-26 17:23
@Author  : ZENKR
@Email   : zenkr@qq.com
@Software: PyCharm
@Desc    :
@license : Copyright (c) 2020 WingEase Technology Co.,Ltd. All Rights Reserved.
"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="we_pyutils",
    version="0.2.13",
    author="ZENKR",
    author_email="zenkr@qq.com",
    keywords=("pip", "pyutils"),
    description="WingEase Python Utils",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="GPLv3",
    url="https://github.com/WingEase/we_pyutils",  # 项目相关文件地址，一般是github
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    # include_package_data=True,
    package_data={
        "we_pyutils": [
            "amazonmws/country.csv",
        ],
    },
    # platforms="any",
    install_requires=[  # 这个项目需要的第三方库
        "requests",
        "requests-toolbelt",
        "Django",
        "django-environ",
        "oss2",
    ]
)
