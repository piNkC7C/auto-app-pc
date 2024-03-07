# -*- coding:utf-8 -*-
import wx

# 访问其他文件
from log.log_record import initLog
from views.index import IndexPage
from tools.messageQueue import MessageQueueManager
from tools.tools import MyThread


def consume_message(queue):
    message_queue_manager = MessageQueueManager()
    message_queue_manager.consume_message_task(queue)


if __name__ == '__main__':
    initLog()
    app = wx.App()  # 实例化APP对象
    frame = IndexPage()
    # consume_queue_thread = MyThread(target_function=consume_message, args=("feiTest",))
    # consume_queue_thread.start()
    app.MainLoop()
