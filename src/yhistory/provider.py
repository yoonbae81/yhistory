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
from abc import ABC, abstractmethod, abstractproperty
from dataclasses import dataclass
from datetime import date

logger = logging.getLogger(__name__)


class NotFoundError(RuntimeError):
    pass


@dataclass
class Record():
    date: date
    open: float
    high: float
    low: float
    close: float
    volume: int


class Provider(ABC):

    @abstractproperty
    def headers(self) -> dict:
        pass

    @abstractproperty
    def base_url(self) -> str:
        pass

    @abstractmethod
    def request(self, symbol: str) -> t.Generator[str, None, None]:
        pass

    @abstractmethod
    def parse(self, text: str) -> t.Generator[Record, None, None]:
        pass

    def download(self, symbol: str, start: date, end: date) -> list[Record]:
        records = []
        try:
            for text in self.request(symbol):
                for record in self.parse(text):
                    records.append(record)

                # if self.start > record['Date']:
                #     self.last_page = True
                #     break

                # if self.end < record['Date']:
                #     continue

        except NotFoundError:
            logger.error('No data found')

        return records
