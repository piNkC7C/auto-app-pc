# -*- coding:utf-8 -*-
import os

import wx
import sys
import win32event
import win32api
import winerror
import ctypes

# 访问其他文件
from log.log_record import initLog, debugLog
from views.index import IndexPage
from config.config import Configs
from tools.startup import get_to_startup

if __name__ == '__main__':
    mutex = None
    try:
        mutex = win32event.CreateMutex(None, 1, "assistant")
        if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
            sys.exit(1)
        else:
            config_data = Configs()
            app_pos = get_to_startup(config_data.app_name)
            if app_pos:
                # 提取文件名（不包括扩展名）
                work_dir = os.path.dirname(app_pos)
                os.chdir(work_dir)
            initLog()
            app = wx.App()  # 实例化APP对象
            frame = IndexPage()
            # consume_queue_thread = MyThread(target_function=consume_message, args=("feiTest",))
            # consume_queue_thread.start()
            app.MainLoop()
    except Exception as e:
        debugLog("应用程序报错")
        debugLog(str(e))
        # sys.exit()
    finally:
        if mutex:
            win32api.CloseHandle(mutex)
