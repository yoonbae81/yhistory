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

import argparse
import logging
import sys

from .load import load
from .providers import Naver

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-5.5s %(name)s %(message)s')


def parse(argv: list[str]):
    parser = argparse.ArgumentParser(description="Load intraday market data from providers")
    parser.add_argument('provider',
                        choices=['naver', 'daum', 'yahoo'],
                        help='market data provider')
    parser.add_argument('symbol',
                        help='stock symbol representing securities on an exchange')

    args = parser.parse_args(argv)
    logger.debug(f"parsed arguments: {args}")

    return args


def main():
    args = parse(sys.argv[1:])

    match args.provider.upper():
        case 'NAVER':
            provider = Naver()
        case 'DAUM':
            raise NotImplementedError()

    df = load(provider, args.symbol)
    print(*df, sep='\n')
    


if __name__ == '__main__':
    main()
