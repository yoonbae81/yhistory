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

import pytest
from nfinance.intraday import Intraday


def test_ctor():
    symbol = 'UNKNOWN'
    sut = Intraday(symbol)
    assert sut.symbol == symbol


def test_invalid_symbol():
    symbol = 'WRONG!'
    sut = Intraday(symbol)
    with pytest.raises(StopIteration):
        next(sut)


def test_first_page():
    symbol = '005930'
    sut = Intraday(symbol)

    page = next(sut)
    assert 10 == len(list(page))
