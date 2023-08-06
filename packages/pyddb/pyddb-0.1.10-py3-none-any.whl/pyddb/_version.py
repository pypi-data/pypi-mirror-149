# -*- coding: utf-8 -*- 
# @Time : 2022/4/6 0006 10:40 
# @Author : ruomubingfeng
# @File : _version.py

import pkg_resources
from _proto import PROGRAM_NAME
try:
    __version__ = pkg_resources.get_distribution(PROGRAM_NAME).version
except pkg_resources.DistributionNotFound:
    __version__ = "unknown"
