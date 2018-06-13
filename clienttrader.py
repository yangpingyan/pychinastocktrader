#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/6/13 14:26 
# @Author : yangpingyan
import time

import pywinauto

import clientconfig



class ClientTrader():
    def __init__(self):
        self._app = None
        self._main = None
        self._config = clientconfig.create(self.broker_type)

    @property
    def broker_type(self):
        return 'ths'

    def connect(self, exe_path=None, **kwargs):
        connect_path = exe_path or self._config.DEFAULT_EXE_PATH
        if connect_path is None:
            raise ValueError('请设置客户端对应的exe地址exe_path,类似 C:\\客户端安装目录\\xiadan.exe')

        self._app = pywinauto.Application.connect(path=connect_path, timeout=3)
        self._close_prompt_window()
        self._main = self._app.top_window()



    def buy(self, security, price, amount, **kwargs):
        pass

    def sell(self, security, price, amount, **kwargs):
        pass

    def cancel_all_entrusts(self):
        pass

    def _close_prompt_window(self):
        self._wait(1)
        for w in self._app.windows(class_name='#32770'):
            if w.window_text() != self._config.TITLE:
                w.close()
        self._wait(1)
        pass

    def _wait(self, seconds):
        time.sleep(seconds)

