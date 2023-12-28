import pyautogui

import pyperclip

def inputContent(str):
    pyperclip.copy(str)
    # 模拟按下Ctrl+V粘贴
    pyautogui.hotkey('Ctrl', 'V')
    # 回车
    pyautogui.typewrite("\n", interval=2)
