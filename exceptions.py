#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/6/13 22:42 
# @Author : yangpingyan

class TradeError(IOError):
    pass


class NotLoginError(Exception):
    def __init__(self, result=None):
        super(NotLoginError, self).__init__()
        self.result = result