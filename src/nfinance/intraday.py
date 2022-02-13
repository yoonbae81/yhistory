#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# nfinance, market data downloader
# https://github.com/yoonbae81/nfinance
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
import re
import typing as t
from abc import ABC, abstractmethod, abstractproperty
from datetime import date, datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43'
}


class OutOfPeriod(Exception):
    pass


class Pages(ABC):
    def __init__(self,
                 symbol: str,
                 start: t.Optional[date] = date.min,
                 end: t.Optional[date] = date.max):
        self.session = self._session()
        self.symbol = symbol
        self.start = start if isinstance(
            start, date) else datetime.fromisoformat(start)
        self.end = end if isinstance(
            end, date) else datetime.fromisoformat(end)
        self.last_page = False

    def _session(self):
        r = Retry(total=5,
                  backoff_factor=0.2,
                  status_forcelist=[413, 429, 500, 502, 503, 504])
        a = HTTPAdapter(max_retries=r)

        session = requests.session()
        session.mount('http://', a)
        session.mount('https://', a)

        return session

    def __next__(self) -> t.Generator:
        if self.last_page:
            raise StopIteration

        res = self.session.get(self.base_url,
                               params=self.next_params(),
                               headers=HEADERS)

        if res.status_code != 200 or not self.is_valid(res.text):
            raise StopIteration()

        return self.parse(res.text)

    def __iter__(self) -> t.Iterable:
        return self

    @abstractproperty
    def base_url(self) -> str:
        pass

    @abstractmethod
    def next_params(self) -> dict:
        pass

    @abstractmethod
    def is_valid(self, text: str) -> bool:
        pass

    @abstractmethod
    def parse(self, text: str) -> t.Generator:
        pass


class Intraday(Pages):
    def __init__(self,
                 symbol: str,
                 start: t.Optional[date] = date.min,
                 end: t.Optional[date] = date.max):
        super().__init__(symbol, start, end)
        self.page = 0

    @property
    def base_url(self) -> str:
        return 'https://finance.naver.com/item/sise_day.nhn'

    def next_params(self) -> dict:
        self.page += 1
        return {'code': self.symbol, 'page': self.page}

    def is_valid(self, text: str) -> bool:
        if '&amp;page=1"  >1</a>\n				</td>\n\n' in text:
            logger.warn('Invalid symbol')
            return False

        return True

    def parse(self, text: str) -> t.Generator:
        def partition(line: str, n: int):
            for i in range(0, len(line), n):
                yield line[i:i + n]

        # ['date', 'close', 'delta', 'open', 'high', 'low', 'volume']
        bs = BeautifulSoup(text, 'html.parser')
        values = [span.text for span in bs.findAll('span', class_='tah')]
        values = list(map(lambda v: v.strip().replace(',', ''), values))
        values = [int(v) if v.isnumeric() else v for v in values]

        for v in partition(values, 7):
            d = datetime.strptime(v[0], '%Y.%M.%d')

            if self.start > d:
                self.last_page = True
                break

            if self.end < d:
                continue

            yield {
                'Date': d,
                'Open': v[3],
                'High': v[4],
                'Low': v[5],
                'Close': v[1],
                'Adj Close': v[1],
                'Volume': v[6],
            }
