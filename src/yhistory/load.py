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
import typing as t
from datetime import date

import pandas as pd
from pandas.core.frame import DataFrame

from .provider import Provider

logger = logging.getLogger(__name__)


def load(provider: Provider,
         symbol: str,
         start: t.Optional[date] = date.min,
         end: t.Optional[date] = date.max) -> DataFrame:

    # todo load df from shelve and get max/min dates
    # todo examine df and given start/end dates 
    # todo download only missing data in shelves

    records = []
    for record in provider.download(symbol, start, end):
        records.append(record)

    # df = pd.DataFrame(records)
    # df.set_index('Date')

    # return df

    return records
