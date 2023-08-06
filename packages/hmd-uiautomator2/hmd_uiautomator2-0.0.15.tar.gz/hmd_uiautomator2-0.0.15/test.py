#!/usr/bin/env python
# -*- coding: utf-8 -*-
# --------------------------------------------------------------
# ProjectName: HmdUIAutomator
# Author: gentliu
# CreateTime: 2022/1/4 11:19
# File Name: test
# Description:
# --------------------------------------------------------------
import logging

import adbutils

import uiautomator2 as u2
from uiautomator2 import Initer

if __name__ == '__main__':
    for device in adbutils.adb.iter_device():
        init = Initer(device, loglevel=logging.DEBUG)
        init.install()

    serial = "E286720782C32100200"
    d = u2.connect(serial)
    d.debug = True
    d.swipe_ext("up", scale=0.9)

