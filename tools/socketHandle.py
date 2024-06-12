import time

import socketio

from log.log_record import debugLog
from tools.tools import get_network_status


class socketHandle:
    def __init__(self, socket_id, fei_frame=None):
        self.socket_id = socket_id
        self.fei_frame = fei_frame
        self.sio = socketio.Client()

        @self.sio.on('connect')
        def on_connect():
            debugLog(f"client {self.socket_id} connect")
            if self.fei_frame:
                if self.fei_frame.reconnect:
                    debugLog("重新打开托管...")
                    self.fei_frame.deal_web_err(True)
            self.sio.emit("UserId", self.socket_id)

        @self.sio.on('disconnect')
        def on_disconnect():
            net_status = get_network_status()
            if net_status:
                debugLog('退出应用或远程主机断连')
                debugLog(f'{self.socket_id} disconnected from server')
            else:
                debugLog('断网')
                debugLog(f'{self.socket_id} disconnected from server')
                if self.fei_frame:
                    if self.fei_frame.fei_status:
                        debugLog("托管中...执行中断操作")
                        self.fei_frame.deal_web_err(False)

        self.sio.connect('http://124.71.179.1:4745')
        # self.sio.connect('http://172.16.61.6:4745')

    def openSocket(self, func):
        # 注册回调函数
        @self.sio.on('seekAdvice')
        def on_message(data):
            debugLog('收到服务器消息: ')
            debugLog(str(data))
            func(data)

        @self.sio.on(self.socket_id)
        def on_message(data):
            debugLog(f'{self.socket_id}消息: ')
            debugLog(data)
            func(data)
            # 停止监听 feiassistid 事件
            self.sio.disconnect()

        self.sio.wait()

    def disconnect(self):
        # 断开 socket 连接
        self.sio.disconnect()

# socket_handler = socketHandle()
# def handle_message(data):
#     debugLog("Received message:", data)
#
# socket_handler.openSocket(handle_message)
