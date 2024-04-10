# -*- coding:utf-8 -*-
import wx
import sys
import win32event
import win32api
import winerror

# 访问其他文件
from log.log_record import initLog, debugLog
from views.index import IndexPage

if __name__ == '__main__':
    mutex = None
    try:
        mutex = win32event.CreateMutex(None, 1, "assistant")
        if win32api.GetLastError() == winerror.ERROR_ALREADY_EXISTS:
            debugLog("Another instance of this program is already running.")
            sys.exit(1)
        else:
            initLog()
            app = wx.App()  # 实例化APP对象
            frame = IndexPage()
            # consume_queue_thread = MyThread(target_function=consume_message, args=("feiTest",))
            # consume_queue_thread.start()
            app.MainLoop()
    finally:
        if mutex:
            win32api.CloseHandle(mutex)
