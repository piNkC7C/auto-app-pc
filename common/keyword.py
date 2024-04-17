import pyautogui

import pyperclip

import time

from log.log_record import debugLog


def inputContent(str):
    debugLog(f"粘贴文字事件:{str}")
    pyperclip.copy(str)
    time.sleep(0.5)
    # 模拟按下Ctrl+V粘贴
    pyautogui.hotkey('Ctrl', 'V')
    # 回车
    # pyautogui.typewrite("\n", interval=2)
