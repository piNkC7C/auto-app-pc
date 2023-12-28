# 这是一个示例 Python 脚本。
import time

# 按 Shift+F10 执行或将其替换为您的代码。
# 按 双击 Shift 在所有地方搜索类、文件、工具窗口、操作和设置。
import pyautogui, sys

import psutil
import win32con

import win32gui
import pyperclip;


def is_program_in_foreground(program_name):
    for proc in psutil.process_iter():
        try:
            process_info = proc.as_dict(attrs=['name', 'status'])
            if process_info['name'] == program_name and process_info['status'] == 'running':
                return True
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            pass
    return False


def print_hi(name):
    # 在下面的代码行中使用断点来调试脚本。
    print(f'Hi, {name}')  # 按 Ctrl+F8 切换断点。
    print(pyautogui.size())
    try:
        while True:
            if x != pyautogui.position().x or y != pyautogui.position().y:
                x, y = pyautogui.position()
                positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
                print(positionStr, end='')
                print('\b' * len(positionStr), end='', flush=True)
    except KeyboardInterrupt:
        print('\n')


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')
