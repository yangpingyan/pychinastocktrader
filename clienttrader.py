#!/usr/bin/env python 
# -*- coding: utf-8 -*- 
# @Time : 2018/6/13 14:26 
# @Author : yangpingyan
import functools
import re
import time
import exceptions
import easyutils
import pywinauto
import clientconfig


class PopDialogHandler:
    def __init__(self, app):
        self._app = app

    def handle(self, title):
        if any(s in title for s in {'提示信息', '委托确认', '网上交易用户协议'}):
            self._submit_by_shortcut()

        elif '提示' in title:
            content = self._extract_content()
            self._submit_by_click()
            return {'message': content}

        else:
            content = self._extract_content()
            self._close()
            return {'message': 'unknown message: {}'.format(content)}

    def _extract_content(self):
        return self._app.top_window().Static.window_text()

    def _extract_entrust_id(self, content):
        return re.search(r'\d+', content).group()

    def _submit_by_click(self):
        self._app.top_window()['确定'].click()

    def _submit_by_shortcut(self):
        self._app.top_window().type_keys('%Y')

    def _close(self):
        self._app.top_window().close()


class TradePopDialogHandler(PopDialogHandler):
    def handle(self, title):
        if title == '委托确认':
            self._submit_by_shortcut()

        elif title == '提示信息':
            content = self._extract_content()
            if '超出涨跌停' in content:
                self._submit_by_shortcut()
            elif '委托价格的小数价格应为' in content:
                self._submit_by_shortcut()

        elif title == '提示':
            content = self._extract_content()
            if '成功' in content:
                entrust_no = self._extract_entrust_id(content)
                self._submit_by_click()
                return {'entrust_no': entrust_no}
            else:
                self._submit_by_click()
                time.sleep(0.05)
                raise exceptions.TradeError(content)
        else:
            self._close()


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

        self._app = pywinauto.Application().connect(path=connect_path, timeout=3)
        self._close_prompt_window()
        self._main = self._app.top_window()

    def buy(self, security, price, amount, **kwargs):
        self._switch_left_menus(['买入[F1]'])

        return self.trade(security, price, amount)

    def sell(self, security, price, amount, **kwargs):
        self._switch_left_menus(['卖出[F2]'])

        return self.trade(security, price, amount)

    def cancel_all_entrusts(self):
        # self._refresh()
        self._switch_left_menus(['撤单[F3]'])
        self._main.window(
            control_id=self._config.TRADE_CANCEL_ALL_ENTRUSTS_ID,
            class_name='Button').click()
        return self._handle_pop_dialogs()

    def _close_prompt_window(self):
        self._wait(1)
        for w in self._app.windows(class_name='#32770'):
            if w.window_text() != self._config.TITLE:
                w.close()
        self._wait(1)
        pass

    @staticmethod
    def _wait(seconds):
        time.sleep(seconds)

    def _switch_left_menus(self, path, sleep=0.2):
        self._get_left_menus_handle().get_item(path).click()
        self._wait(sleep)

    @functools.lru_cache()
    def _get_left_menus_handle(self):
        while True:
            try:
                handle = self._main.window(
                    control_id=129, class_name='SysTreeView32')
                # sometime can't find handle ready, must retry
                handle.wait('ready', 2)
                return handle
            except:
                pass

    def trade(self, security, price, amount):
        self._set_trade_params(security, price, amount)
        self._submit_trade()

        return self._handle_pop_dialogs(handler_class=TradePopDialogHandler)

    def _set_trade_params(self, security, price, amount):
        code = security[-6:]
        self._type_keys(self._config.TRADE_SECURITY_CONTROL_ID, code)

        # wait security input finish
        self._wait(0.4)

        self._type_keys(self._config.TRADE_PRICE_CONTROL_ID,
                        easyutils.round_price_by_code(price, code))

        self._type_keys(self._config.TRADE_AMOUNT_CONTROL_ID, str(int(amount)))

    def _submit_trade(self):
        self._wait(0.1)
        self._main.window(
            control_id=self._config.TRADE_SUBMIT_CONTROL_ID,
            class_name='Button').click()
        pass

    def _handle_pop_dialogs(self, handler_class=PopDialogHandler):
        handler = handler_class(self._app)

        while self._is_exist_pop_dialog():
            title = self._get_pop_dialog_title()

            result = handler.handle(title)
            if result:
                return result
        return {'message': 'success'}

    def _type_keys(self, control_id, text):
        self._main.window(control_id=control_id, class_name='Edit').set_edit_text(text)

    def _is_exist_pop_dialog(self):
        self._wait(0.2)  # wait dialog display
        return self._main.wrapper_object() != self._app.top_window().wrapper_object()

    def _get_pop_dialog_title(self):
        return self._app.top_window().window(
            control_id=self._config.POP_DIALOD_TITLE_CONTROL_ID).window_text()

    def _refresh(self):
        self._switch_left_menus(['买入[F1]'], sleep=0.05)
