#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# yHistory, provides cached market data from providers
# https://github.com/yoonbae81/yhistory
#
# Copyright 2022 Yoonbae Cho
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import logging
import typing as t
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .base import NotFoundError, Provider, Record

logger = logging.getLogger(__name__)


class Naver(Provider):

    @property
    def headers(self) -> dict:
        return {
            'User-Agent':
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43'
        }

    @property
    def base_url(self) -> str:
        return 'https://finance.naver.com/item/sise_day.nhn'

    @staticmethod
    def session() -> requests.Session:
        r = Retry(total=5,
                  backoff_factor=0.2,
                  status_forcelist=[413, 429, 500, 502, 503, 504])
        a = HTTPAdapter(max_retries=r)

        s = requests.session()
        s.mount('http://', a)
        s.mount('https://', a)

        return s

    def fetch(self, symbol: str) -> t.Generator[str, None, None]:
        s = self.__class__.session()
        p = {'code': symbol, 'page': 1}
        r = s.get(self.base_url, params=p, headers=self.headers)

        if '&amp;page=1"  >1</a>\n				</td>\n\n' in r.text:
            logger.warn("Couldn't find any data due to invalid symbol")
            raise NotFoundError

        yield r.text

        while '맨뒤' in r.text:
            p['page'] += 1
            r = s.get(self.base_url, params=p, headers=self.headers)
            yield r.text


    @staticmethod
    def partition(line: str, n: int) -> t.Generator[list[str], None, None]:
        for i in range(0, len(line), n):
            yield line[i:i + n]

    def parse(self, text: str) -> t.Generator[Record, None, None]:
        bs = BeautifulSoup(text, 'html.parser')

        values = [span.text for span in bs.findAll('span', class_='tah')]
        values = list(map(lambda v: v.strip().replace(',', ''), values))
        values = [int(v) if v.isnumeric() else v for v in values]

        # ['date', 'close', 'delta', 'open', 'high', 'low', 'volume']
        for v in self.__class__.partition(values, 7):
            yield Record(date=datetime.strptime(v[0], '%Y.%m.%d'),
                         open=v[3],
                         high=v[4],
                         low=v[5],
                         close=v[1],
                         volume=v[6])
