#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : country.py
@Time    : 2021/8/26 14:26
@Author  : ZENKR
@Email   : zenkr@qq.com
@Software: PyCharm
@Desc    :
@license : Copyright (c) 2021 WingEase Technology Co.,Ltd. All Rights Reserved.
"""
import csv
from pathlib import Path


class Country:
    id: str = None
    marketplace_id: str = None
    name: str = None
    continent: str = None
    url: str = None
    url_seller: str = None
    timezone: str = None
    currency: str = None
    mws_endpoint: str = None

    def __init__(self, country: dict):
        self.__dict__.update(country)
        self._dict: dict = country

    @property
    def dict(self):
        return self._dict


class Countries:
    # North America
    BR: Country = None
    CA: Country = None
    MX: Country = None
    US: Country = None
    # Europe region
    AE: Country = None
    DE: Country = None
    EG: Country = None
    ES: Country = None
    FR: Country = None
    GB: Country = None
    IN: Country = None
    IT: Country = None
    NL: Country = None
    PL: Country = None
    SA: Country = None
    SE: Country = None
    TR: Country = None
    # Far East region
    SG: Country = None
    AU: Country = None
    JP: Country = None
    # China
    CN: Country = None
    _ids: list = []
    _dict: dict = {}

    def __init__(self):
        self._load_countries()

    def _load_countries(self):
        folder_path = Path(__file__).parent
        with open(folder_path / 'country.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            items = list(reader)
        for item in items:
            self.__dict__.update({item['id']: Country(item)})
            self._ids.append(item['id'])
            self._dict.update({item['id']: Country(item).dict})
        # from we_pyutils.t.file import load_yaml_file
        # f = load_yaml_file('country.yaml', multiple=True)

    @property
    def ids(self) -> list:
        return self._ids

    @property
    def marketplace_ids_kv(self) -> dict:
        data = {}
        for id in self._ids:
            data[id] = getattr(self, id).marketplace_id
        return data

    @property
    def marketplace_ids(self) -> list:
        data = []
        for id in self._ids:
            data.append(getattr(self, id).marketplace_id)
        return data

    @property
    def mws_endpoints_kv(self) -> dict:
        data = {}
        for id in self._ids:
            data[id] = getattr(self, id).mws_endpoint
        return data

    @property
    def mws_endpoints(self) -> list:
        data = []
        for id in self._ids:
            data.append(getattr(self, id).mws_endpoint)
        return data

    @property
    def domains(self):
        data = []
        for id in self._ids:
            url = getattr(self, id).url
            if url:
                data.append(url)
        return data

    @property
    def domains_kv(self):
        data = {}
        for id in self._ids:
            if (url := getattr(self, id).url):
                data[id] = url
        return data


if __name__ == '__main__':
    countries = Countries()
    us = countries.US.marketplace_id
    e = countries.mws_endpoints_kv
    e2 = countries.marketplace_ids_kv
    pass
