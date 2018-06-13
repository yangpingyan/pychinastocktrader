#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/6/13 14:26 
# @Author : yangpingyan

import clientconfig

class ClientTrader():
    def __init__(self):
        self._app = None
        self._main = None
        self.config = clientconfig.create(self.broker_type)

    @property
    def broker_type(self):
        return 'ths'

    def buy(self, secuirity, price, amount, **kwargs):
        pass

    def sell(self, security, price, amount, **kwargs):
        pass

    def cancel_all_entrusts(self):
        pass


