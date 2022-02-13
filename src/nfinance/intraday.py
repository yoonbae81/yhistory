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
from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)

BASE_URL = 'https://finance.naver.com/item/sise_day.nhn'
HEADERS = {
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.80 Safari/537.36 Edg/98.0.1108.43'
}

class OutOfPeriod(Exception):
    pass


class Pages:
    def init(self):
        r = Retry(total=5,
                  backoff_factor=0.2,
                  status_forcelist=[413, 429, 500, 502, 503, 504])
        a = HTTPAdapter(max_retries=r)

        self.session = requests.session()
        self.session.mount('http://', a)
        self.session.mount('https://', a)


class Intraday(Pages):
    def __init__(self, symbol: str):
        super().__init__()

        self.symbol = symbol
        self.page = 1

    def __next__(self):
        res = self.session.get(BASE_URL, params=params, headers=HEADERS)


        raise StopIteration()

    def __iter__(self):
        return self



"""

def parse(bs: BeautifulSoup) -> dict:
    # ['date', 'close', 'delta', 'open', 'high', 'low', 'volume']
    values = [span.text for span in bs.findAll('span', class_='tah')]
    values = list(
        map(lambda s: s.strip().replace(',', '').replace('.', '-'), values))

    def partition(line, n):
        for i in range(0, len(line), n):
            yield line[i:i + n]

    for row in partition(values, 7):
        yield {
            'Date': row[0],
            'Open': row[3],
            'High': row[4],
            'Low': row[5],
            'Close': row[1],
            'Adj Close': row[1],
            'Volume': row[6],
        }
    

def get(symbol, page):
    s = session()
    r = s.get(URL, params={'code': symbol, 'page': page}, headers=HEADERS)

    bs = BeautifulSoup(r.text, 'html.parser')
    if bs.find('span', class_='tah').text == '':
        raise FileNotFoundError()


def download(symbol: str, days: int) -> DataFrame:
    l = []
    for r in parse(bs):
        if date_from > r['Date']:
            raise OutOfPeriod()

        l.append(r)

    df = pd.DataFrame(l)
    df.set_index('Date')

    return {}
"""
