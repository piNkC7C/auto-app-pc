import time

import socketio


class socketHandle:
    def openSocket(self, func, feiassistid):
        sio = socketio.Client()

        @sio.on('connect')
        def on_connect():
            print("client connect")
            sio.emit("UserId", feiassistid)

        @sio.on('disconnect')
        def on_disconnect():
            print('disconnected from server')

        # 注册回调函数
        @sio.on('seekAdvice')
        def on_message(data):
            print('收到服务器消息: ', data)
            func(data)

        @sio.on(feiassistid)
        def on_message(data):
            func(data)

        sio.connect('http://124.71.179.1:4745')

        sio.wait()

# socket_handler = socketHandle()
# def handle_message(data):
#     print("Received message:", data)
#
# socket_handler.openSocket(handle_message)
