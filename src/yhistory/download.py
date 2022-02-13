#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# yHistory, Korean stock market data downloader
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
from datetime import date, datetime

import pandas as pd
from pandas.core.frame import DataFrame

from .intraday import Intraday

logger = logging.getLogger(__name__)


def download(symbol, start=date.min, end=date.max, interval='1d') -> DataFrame:
    logger.info('starting...')

    match interval:
        case '1d':
            source = Intraday(symbol, start, end)
            index = 'Date'
        case '1m':
            raise NotImplementedError()

    records = []
    for record in source:
        records.append(record)

    df = pd.DataFrame(records)
    df.set_index(index)

    return df


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-5.5s %(name)s %(message)s')

    print(download('005930'))
