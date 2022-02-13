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

import argparse
import logging

from .download import download

logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)-5.5s %(name)s %(message)s')

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('symbol')

    args = parser.parse_args()
    logger.debug(f"parsed arguments: {args}")

    data = download(args.symbol)
    logger.info(data)


if __name__ == '__main__':
    main()