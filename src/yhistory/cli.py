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

from .naver import Naver
from .load import load

logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('provider')
    parser.add_argument('symbol')

    args = parser.parse_args()
    logger.debug(f"parsed arguments: {args}")

    return args


def main():
    args = parse_args()

    match args.provider.upper():
        case 'NAVER':
            provider = Naver()
        case 'DAUM':
            raise NotImplementedError()

    df = load(provider, args.symbol)
    print(df)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG,
                        format='%(levelname)-5.5s %(name)s %(message)s')

    main()
