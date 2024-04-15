from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener
from log.log_record import debugLog
import pyautogui
import time
from gui import APP


class GlobalListener:
    def __init__(self, func, args=(), gui_frame=None):
        self.is_listening = False
        self.func = func
        self.args = args
        self.gui_frame = gui_frame
        self.has_called_func = False  # 添加标志来标记是否已调用函数
        self.mouse_stop = False
        self.key_stop = False  # 添加标志来标记是否已调用函数
        self.last_action_time = time.time()
        # self.key_direction = 'down'

    def on_mouse_click(self, x, y, button, pressed):
        self.last_action_time = time.time()
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
        self.last_action_time = time.time()
        debugLog("鼠标移动事件")
        debugLog(self.gui_frame.is_human)
        if self.gui_frame.is_human:
            self.mouse_stop = True
            if not self.key_stop:
                pyautogui.press('Ctrl')
                # self.on_key_press(None)
            self.stop_listening()
            return False  # 返回 False 停止监听

    def on_key_press(self, key):
        self.last_action_time = time.time()
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

    def move_mouse_if_idle(self):
        # debugLog("上次移动鼠标时间")
        # debugLog(self.last_action_time)
        current_time = time.time()
        if current_time - self.last_action_time > 60:
            debugLog("超过60秒没有动作")
            # # 获取屏幕的宽度和高度
            # screen_width, screen_height = pyautogui.size()
            # # 获取当前鼠标位置
            # current_x, current_y = pyautogui.position()
            # # 计算对称位置的坐标
            # symmetric_x = screen_width - current_x
            # symmetric_y = screen_height - current_y  # 假设以屏幕中心为对称轴
            # 移动鼠标至对称位置
            self.gui_frame.is_human = False
            time.sleep(0.5)
            # pyautogui.moveTo(symmetric_x, symmetric_y, duration=0.5)
            # if self.key_direction == 'up':
            #     self.key_direction = 'down'
            # else:
            #     self.key_direction = 'up'
            pyautogui.press('Ctrl')
            self.gui_frame.is_human = True
            self.last_action_time = current_time

    def start_listening(self):
        self.is_listening = True
        # 开始监听全局鼠标点击事件
        with MouseListener(on_click=self.on_mouse_click, on_move=self.on_mouse_move) as mouse_listener:
            # 开始监听全局键盘点击事件
            with KeyboardListener(on_press=self.on_key_press) as keyboard_listener:
                while self.is_listening:
                    self.move_mouse_if_idle()
                    time.sleep(1)
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


class KeyListener:
    def __init__(self, key_list, instruction_list):
        self.is_listening = False
        debugLog(key_list)
        self.key_list = key_list
        # self.key_num = key_list.__len__()
        self.instruction_list = instruction_list
        # self.pre_key = None
        self.app_instance = APP()

    def on_key_press(self, key):
        # debugLog("前一个键")
        # debugLog(self.pre_key)
        # debugLog("当前键")
        # debugLog(str(key))
        if str(key) in self.key_list:
            # if self.pre_key is None:
            #     self.pre_key = str(key)
            # if self.key_num == 1:
            debugLog(f"用户按了{str(key)}键")
            self.app_instance.deal_task_list(self.instruction_list, 1, 2)
            # else:
            #     if self.pre_key in self.key_list:
            #         debugLog(f"用户按了{self.pre_key}加{str(key)}组合键")
        # else:
        #     self.pre_key = None
        if self.is_listening is False:
            return False  # 返回 False 停止监听

    def start_listening(self):
        self.is_listening = True
        # 开始监听全局键盘点击事件
        with KeyboardListener(on_press=self.on_key_press) as keyboard_listener:
            # 持续监听鼠标和键盘事件，直到手动停止
            keyboard_listener.join()

    def stop_listening(self):
        self.is_listening = False
        time.sleep(0.5)
        pyautogui.press('Ctrl')
