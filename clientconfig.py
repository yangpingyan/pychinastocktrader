#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/6/13 14:31 
# @Author : yangpingyan

def create(broker):
    if broker == 'ths':
        return CommonConfig
    raise NotImplemented

class CommonConfig:
    DEFAULT_EXE_PATH = r'C:\同花顺软件\同花顺\xiadan.exe'
    TITLE = '网上股票交易系统5.0'