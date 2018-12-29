# -*- coding: utf-8 -*-
__author__ = 'bobby'

from scrapy.cmdline import execute

import sys
import os

"""
-------------------------------------------------
jobbole
-------------------------------------------------
"""
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# execute(["scrapy", "crawl", "jobbole"])

"""
-------------------------------------------------
dxy
-------------------------------------------------
"""
# sys.path.append(os.path.dirname(os.path.abspath(__file__)))
execute(["scrapy", "crawl", "dxy"])
