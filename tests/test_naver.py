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

import pytest
from yhistory.providers.base import NotFoundError
from yhistory.providers import Naver


def test_invalid_symbol():
    symbol = 'WRONG!'

    sut = Naver()
    with pytest.raises(NotFoundError):
        next(sut.fetch(symbol))


def test_first_page():
    symbol = '005930'

    sut = Naver()
    text = next(sut.fetch(symbol))
    assert '네이버 금융' in text

    records = list(sut.parse(text))
    assert 10 == len(records)
