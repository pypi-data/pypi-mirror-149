#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@File    : ieee_ra.py
@Time    : 2022/4/6 21:10
@Author  : ZENKR
@Email   : zenkr@qq.com
@Software: PyCharm
@Desc    :
@license : Copyright (c) 2022 WingEase Technology Co.,Ltd. All Rights Reserved.
"""
import csv
import re
from pathlib import Path
from typing import Dict, List

from django.db import models


class OuiRegistry(models.TextChoices):
    MA_L = 'MA-L'
    MA_M = 'MA-M'
    MA_S = 'MA-S'
    IAB = 'IAB'
    CID = 'CID'


class OuiParser:
    headers = [
        'registry', 'assignment', 'organization_name',
        'organization_address_1', 'organization_address_2', 'organization_address_3'
    ]
    default_files: Dict[OuiRegistry, list] = {
        OuiRegistry.MA_L: 'oui.txt',
        OuiRegistry.MA_M: 'mam.txt',
        OuiRegistry.MA_S: 'oui36.txt',
        OuiRegistry.IAB: 'iab.txt',
        OuiRegistry.CID: 'cid.txt',
    }

    default_registries = [
        OuiRegistry.MA_L, OuiRegistry.MA_M, OuiRegistry.MA_S, OuiRegistry.IAB, OuiRegistry.CID
    ]

    def txt_content_parser(self,
                           content: str, /, *,
                           registry: OuiRegistry = None,
                           deduplicate: bool = True
                           ) -> list:
        _rows = []
        _dict = {}
        try:
            for mg in content.split('\n\n')[1:]:
                splitlines = mg.splitlines()
                # hex_str = re.search(r'^[A-Z0-9]{2}-[A-Z0-9]{2}-[A-Z0-9]{2}', splitlines[0].strip()).group().strip()
                [hex_str, organization] = [_x.strip() for _x in splitlines[0].split('(hex)')]
                base16_str = re.search(r'^[A-Z0-9-]+', splitlines[1].strip()).group().strip()
                if registry in [OuiRegistry.MA_L, OuiRegistry.CID]:
                    assignment = base16_str
                elif registry == OuiRegistry.MA_M:
                    assignment = hex_str.replace('-', '') + base16_str[0]
                elif registry in [OuiRegistry.MA_S, OuiRegistry.IAB]:
                    assignment = hex_str.replace('-', '') + base16_str[0:3]
                else:
                    assignment = ''
                # organization = re.search(r'\t.+$', splitlines[0].strip()).group().strip()
                address_new: list = [a.strip() for a in splitlines[2:]]
                item = [registry.value, assignment, organization] + address_new
                if deduplicate:
                    _dict[f'{registry.name}-{assignment}'] = item
                else:
                    _rows.append(item)
            if deduplicate:
                _rows = list(_dict.values())
            _rows.sort()
        except Exception as e:
            pass
        finally:
            return _rows

    def load_txt_files(self,
                       folder: Path = None,
                       registries: List[OuiRegistry] = None,
                       files: Dict[OuiRegistry, list] = None
                       ) -> Dict[OuiRegistry, list]:
        _registries = self.default_registries if not registries else registries
        _files = self.default_files if not files else self.default_files.copy().update(files)
        _dict = {}
        for registry in _registries:
            oui_path = folder / _files.get(registry, '')
            with oui_path.open(mode='r', encoding='utf-8') as f:
                content = f.read()
                _dict[registry] = self.txt_content_parser(content, registry=registry)
        return _dict

    def save_csv(self, path: Path, /, data: Dict[OuiRegistry, list]):
        with open(str(path), 'w', encoding='utf-8', newline='') as f:
            f_csv = csv.writer(f)
            f_csv.writerow(self.headers)
            for l in data.values():
                f_csv.writerows(l)

    def load_csv(self, path: Path, /):
        with open(str(path), encoding='utf-8') as f:
            # rows = csv.DictReader(f)
            # return list(rows)
            row = csv.reader(f)
            headers = next(row)
            pass

    def compare(self, latest: Path, older: Path):
        latest_dict = {}
        older_dict = {}
        items_new = []  # new
        items_deleted = []  # deleted
        items_same = []  # same
        items_updated = []  # update
        with open(str(latest), encoding='utf-8') as f:
            row = csv.reader(f)
            headers = next(row)
            for _r in row:
                latest_dict[f'{_r[0]}-{_r[1]}'] = _r
            pass
        with open(str(older), encoding='utf-8') as f:
            row = csv.reader(f)
            headers = next(row)
            for _r in row:
                older_dict[f'{_r[0]}-{_r[1]}'] = _r
            pass
        for _latest_k, _latest_v in latest_dict.items():
            if _latest_k in older_dict:  # 若新列表中存在于旧列表
                if _latest_v == older_dict.get(_latest_k):  # 如果值相同
                    items_same.append(_latest_v)
                else:  # 如果值不同
                    items_updated.append(_latest_v)
                older_dict.pop(_latest_k)
            else:  # 若新列表键名不存在于旧列表
                items_new.append(_latest_v)
        items_deleted.extend(older_dict.values())
        return items_new, items_updated, items_same, items_deleted


def oui_list_compare(latest, older: list = None):
    pass


if __name__ == '__main__':
    # MA-L 有重复的项目 如：0001C8、080030。需要特别注意。
    data_dir: Path = Path(__file__).parent.parent / 'tests' / 'parsers' / 'data'
    ieee_dir: Path = data_dir / 'standards-oui.ieee.org'
    sl = list(ieee_dir.iterdir())
    sl.sort(reverse=True)
    last_dir: Path = sl[0]
    older_dir: Path = sl[1]
    parser = OuiParser()
    # rows_latest = parser.load_txt_files(folder=last_dir, registries=[OuiRegistry.MA_L])
    # r1 = parser.save_csv(last_dir / 'ieee_ra.csv', rows_latest)
    # rows_older = parser.load_txt_files(folder=older_dir, registries=[OuiRegistry.MA_L])
    # r2 = parser.save_csv(older_dir / 'ieee_ra.csv', rows_older)

    # latest_rows = parser.load_csv(last_dir / 'ieee_ra.csv')

    items_new, items_updated, items_same, items_deleted = parser.compare(last_dir / 'ieee_ra.csv',
                                                                         older_dir / 'ieee_ra.csv')
    pass
