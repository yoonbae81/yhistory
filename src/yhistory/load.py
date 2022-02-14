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
from datetime import date, datetime

import pandas as pd
from pandas.core.frame import DataFrame

from .providers.base import Provider

logger = logging.getLogger(__name__)


def load(
    provider: Provider,
    symbol: str,
    start: t.Optional[date] = date.min,
    end: t.Optional[date] = date.today()
) -> DataFrame:

    start, end = to_date(start), to_date(end)

    # todo load df from shelve and get max/min dates
    # todo examine df and given start/end dates
    # todo download only missing data in shelves

    records = provider.download(symbol, start, end)

    # todo merge downloaded dataframe into existing one in shelve

    return records


def to_date(value: t.Union[date, str]) -> date:
    if isinstance(value, date):
        return value

    return datetime.fromisoformat(value)
