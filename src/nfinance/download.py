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

import pandas as pd
from pandas.core.frame import DataFrame

from . import Intraday

logger = logging.getLogger(__name__)


def download(symbol, start=None, end=None, interval='1d') -> DataFrame:
    logger.info('starting...')

    match interval:
        case '1d':
            pages = Intraday(symbol, start, end)
        case '1m':
            raise NotImplementedError()

    records = []
    for page in pages:
        for record in page:
            records.append(record)

    df = pd.DataFrame(records)
    df.set_index('Date')

    return df

if __name__ == '__main__':
    print(download('005930'))
