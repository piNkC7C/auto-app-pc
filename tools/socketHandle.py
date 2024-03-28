import time

import socketio

from log.log_record import debugLog


class socketHandle:
    def __init__(self, socket_id, deal_no_web):
        self.is_human = False
        self.socket_id = socket_id
        self.sio = socketio.Client()

        @self.sio.on('connect')
        def on_connect():
            debugLog(f"client {self.socket_id} connect")
            self.sio.emit("UserId", self.socket_id)

        @self.sio.on('disconnect')
        def on_disconnect():
            if self.is_human:
                debugLog('手动断开')
                debugLog(f'{self.socket_id} disconnected from server')
            else:
                debugLog('断网了')
                debugLog(f'{self.socket_id} disconnected from server')
                if deal_no_web:
                    deal_no_web(False)

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
        self.is_human = True
        # 断开 socket 连接
        self.sio.disconnect()

# socket_handler = socketHandle()
# def handle_message(data):
#     debugLog("Received message:", data)
#
# socket_handler.openSocket(handle_message)
