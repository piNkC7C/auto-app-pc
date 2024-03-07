from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener


class GlobalListener:
    def __init__(self, func, args=()):
        self.is_listening = False
        self.func = func
        self.args = args

    def on_mouse_click(self, x, y, button, pressed):
        if pressed:
            self.stop_listening()
            return False  # 返回 False 停止监听

    def on_mouse_move(self, x, y):
        self.stop_listening()
        return False  # 返回 False 停止监听

    def on_key_press(self, key):
        self.stop_listening()
        return False  # 返回 False 停止监听

    def start_listening(self):
        self.is_listening = True
        # 开始监听全局鼠标点击事件
        with MouseListener(on_click=self.on_mouse_click, on_move=self.on_mouse_move) as mouse_listener:
            # 开始监听全局键盘点击事件
            with KeyboardListener(on_press=self.on_key_press) as keyboard_listener:
                # 持续监听鼠标和键盘事件，直到手动停止
                mouse_listener.join()
                keyboard_listener.join()

    def stop_listening(self):
        self.is_listening = False
        self.func(*self.args)
