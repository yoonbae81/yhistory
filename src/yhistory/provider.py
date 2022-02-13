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
from abc import ABC, abstractmethod, abstractproperty
from datetime import date, time, datetime

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

logger = logging.getLogger(__name__)


class Provider(ABC):
    def __init__(self):
        self.session = self._session()

    def __iter__(self) -> t.Iterable:
        return self

    @abstractproperty
    def base_url(self) -> str:
        pass

    @abstractproperty
    def header(self) -> dict:
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

    def _session(self):
        r = Retry(total=5,
                  backoff_factor=0.2,
                  status_forcelist=[413, 429, 500, 502, 503, 504])
        a = HTTPAdapter(max_retries=r)

        session = requests.session()
        session.mount('http://', a)
        session.mount('https://', a)

        return session

    def download(self,
                 symbol: str,
                 start: t.Optional[date] = date.min,
                 end: t.Optional[date] = date.max) -> t.Iterable:

        for i in range(3):
            yield {'Value'}

    # todo merge __next__ into download above
    def __next__(self) -> dict:
        res = self.session.get(self.base_url,
                               headers=self.header,
                               params=self.next_params())

        if res.status_code != 200 or not self.is_valid(res.text):
            raise StopIteration()

        for record in self.parse(res.text):

            if self.start > record['Date']:
                self.last_page = True
                break

            if self.end < record['Date']:
                continue

            yield record


    def get_datetime(data: t.Union[str, date, time]) -> t.Union[date, time]:
        if isinstance(data, str):
            return datetime.fromisoformat(data)

        return data
