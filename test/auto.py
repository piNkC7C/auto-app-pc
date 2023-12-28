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

def inputContent(str):
    pyperclip.copy(str)
    # 模拟按下Ctrl+V粘贴
    pyautogui.hotkey('Ctrl', 'V')
    # 回车
    pyautogui.typewrite("\n", interval=2)

def print_hi():
    # 在下面的代码行中使用断点来调试脚本。
    print(pyautogui.size())

    program_name = 'WXWork.exe'  # 替换为你要判断的程序名称
    while is_program_in_foreground(program_name) is False:
        print(f"{program_name} 不在最前面")
    print(f"{program_name} 在最前面")

    hwnd = win32gui.FindWindow(None, "企业微信")
    win32gui.SetForegroundWindow(hwnd)
    win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 800, 600, win32con.SWP_SHOWWINDOW)
    pyautogui.click(400,20)
    time.sleep(2)
    button7location = pyautogui.locateOnScreen('1702275863313.png')
    time.sleep(2)
    pyautogui.click(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
    time.sleep(2)
    inputContent("联联")
    time.sleep(2)
    pyautogui.click(140,130)
    time.sleep(2)
    pyautogui.click(500,550)
    time.sleep(2)
    # pyautogui.write('联联', interval=0.25)
    inputContent("您好")
    print(button7location)
    time.sleep(2)

    # try:
    #     while True:
    #         x, y = pyautogui.position()
    #         positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
    #         print(positionStr, end='')
    #         print('\b' * len(positionStr), end='', flush=True)
    # except KeyboardInterrupt:
    #     print('\n')


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    print_hi('PyCharm')

# 访问 https://www.jetbrains.com/help/pycharm/ 获取 PyCharm 帮助
