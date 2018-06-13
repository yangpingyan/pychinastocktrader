#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author : yangpingyan

from log import log
import pywinauto
import time

# path = ['查询[F4]', '资金股票']

# path = ['卖出[F2]']
# path = ['查询[F4]']

log.info("Mission start")

class CommonConfig:
    DEFAULT_EXE_PATH = r'C:\同花顺软件\同花顺\xiadan.exe'
    TITLE = '网上股票交易系统5.0'

config = CommonConfig
connect_path = config.DEFAULT_EXE_PATH

app = pywinauto.Application().connect(path=connect_path, timeout=3)
main = app.top_window()


# 找到左侧菜单
while True:
    try:
        handle = main.child_window(control_id=129, class_name='SysTreeView32')
        # sometime can't find handle ready, must retry
        handle.wait('ready', 2)
        break
    except:
        pass

path = ['买入[F1]']
handle.get_item(path).click()
time.sleep(0.2)
security = "002413"
code = security[-6:]

main.window(control_id=1032, class_name='Edit').set_edit_text(code)
# wait security input finish
time.sleep(0.1)
main.window(control_id=1033, class_name='Edit').set_edit_text("5.33")
main.window(control_id=1034, class_name='Edit').set_edit_text("200")

time.sleep(0.05)
main.window(control_id=1006, class_name='Button').click()
#
# while main.wrapper_object() != app.top_window().wrapper_object():
#     time.sleep(0.2)
#     title = app.top_window().window(control_id=config.POP_DIALOD_TITLE_CONTROL_ID).window_text()
#
#     app.top_window().type_keys('%Y')
#     time.sleep(0.2)
#     app.top_window()['确定'].click()

log.info("Mission Complete")

# # close_prompt_windows()
# time.sleep(1)
# for w in app.windows(class_name='#32770'):
#     if w.window_text() != config.TITLE:
#         w.close()
# time.sleep(1)
#

#

#
#

# 可用金额
# fund_available = main.child_window(control_id=1016, class_name='Static')
# fund_available.print_control_identifiers()



