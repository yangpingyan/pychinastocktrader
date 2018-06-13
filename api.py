#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/6/13 15:04 
# @Author : yangpingyan

from log import log
import logging
import six

if six.PY2:
    raise TypeError('不支持 Python2，请升级 Python3 ')

def use(broker, debug=True, **kwargs):
    if not debug:
        log.setLevel(logging.INFO)

    if broker.lower() in ['ths', '同花顺'] :
        from clienttrader import ClientTrader
        return ClientTrader()

    raise NotImplemented

