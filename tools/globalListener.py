from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from log.log_record import debugLog
import pyautogui


class GlobalListener:
    def __init__(self, func, args=(), gui_frame=None):
        self.is_listening = False
        self.func = func
        self.args = args
        self.gui_frame = gui_frame
        self.has_called_func = False  # 添加标志来标记是否已调用函数
        self.mouse_stop = False
        self.key_stop = False  # 添加标志来标记是否已调用函数

    def on_mouse_click(self, x, y, button, pressed):
        debugLog("鼠标点击事件")
        debugLog(self.gui_frame.is_human)
        if pressed & self.gui_frame.is_human:
            self.mouse_stop = True
            if not self.key_stop:
                pyautogui.press('1')
                # self.on_key_press(None)
            self.stop_listening()
            return False  # 返回 False 停止监听

    def on_mouse_move(self, x, y):
        debugLog("鼠标移动事件")
        debugLog(self.gui_frame.is_human)
        if self.gui_frame.is_human:
            self.mouse_stop = True
            if not self.key_stop:
                pyautogui.press('1')
                # self.on_key_press(None)
            self.stop_listening()
            return False  # 返回 False 停止监听

    def on_key_press(self, key):
        debugLog("键盘事件")
        debugLog(self.gui_frame.is_human)
        if self.gui_frame.is_human:
            self.key_stop = True
            # if not self.mouse_stop:
                # pyautogui.moveTo(0, 0, duration=1.0)
                # pyautogui.click()
                # self.on_mouse_move(0, 0)
                # self.on_mouse_click(0, 0, None, True)
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
        if not self.has_called_func:  # 只有在未调用过函数时才调用
            self.has_called_func = True
            self.func(*self.args)

    def stop_only_listening(self):
        self.is_listening = False
