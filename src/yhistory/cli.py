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


import argparse
import logging

from nfinance.intraday import Intraday

from .download import download

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('symbol')

    args = parser.parse_args()
    logger.debug(f"parsed arguments: {args}")

    # data = download(args.symbol)
    # print(data)

    i = Intraday('015760', start='2022-02-07', end='2022-02-10')
    print(list(next(i)))

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-5.5s %(name)s %(message)s')

    main()
