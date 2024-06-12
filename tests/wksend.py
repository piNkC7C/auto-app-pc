import time

import socketio

sio = socketio.Client()

@sio.on('connect')
def on_connect():
    print("client connect")

@sio.on('disconnect')
def on_disconnect():
    print('disconnected from server')

# 注册回调函数
@sio.on('seekAdvice')
def on_message(data):
    print('收到服务器消息: ', data)


sio.connect('http://172.16.61.12:4745')
sio.emit("UserId", "123456")

print('client send hello success')

time.sleep(6000)