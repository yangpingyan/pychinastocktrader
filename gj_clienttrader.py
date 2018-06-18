# coding:utf8
from __future__ import division

import re
import tempfile
import time

import pywinauto
import pywinauto.clipboard

from clienttrader import ClientTrader
import helpers

class GJClientTrader(ClientTrader):
    @property
    def broker_type(self):
        return 'gj'

    def login(self, user, password, exe_path, comm_password=None, **kwargs):
        try:
            self._app = pywinauto.Application().connect(path=self._run_exe_path(exe_path), timeout=1)
        except Exception:
            self._app = pywinauto.Application().start(exe_path)

            # wait login window ready
            while True:
                try:
                    self._app.top_window().Edit1.wait('ready')
                    break
                except RuntimeError:
                    pass

            self._app.top_window().Edit1.type_keys(user)
            self._app.top_window().Edit2.type_keys(password)
            edit3 = self._app.top_window().window(control_id=1003)
            while True:
                try:
                    code = self._handle_verify_code()
                    edit3.type_keys(code)
                    time.sleep(1)
                    self._app.top_window()['确定(Y)'].click()
                    try:
                        self._app.top_window().wait_not('exists', 5)
                        break
                    except:
                        self._app.top_window()['确定'].click()
                        pass
                except Exception as e:
                    pass

            self._app = pywinauto.Application().connect(path=self._run_exe_path(exe_path), timeout=10)

        self._main = self._app.window(title='网上股票交易系统5.0')

    def _handle_verify_code(self):
        control = self._app.top_window().window(control_id=1499)
        control.click()
        time.sleep(0.2)
        file_path = tempfile.mktemp() + '.jpg'
        control.capture_as_image().save(file_path)
        time.sleep(0.2)
        vcode = helpers.recognize_verify_code(file_path, 'gj_client')
        return ''.join(re.findall('[a-zA-Z0-9]+', vcode))