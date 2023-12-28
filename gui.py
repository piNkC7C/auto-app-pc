# -*- coding:utf-8 -*-
import math
import time
# author：鹦秒科技
import tkinter as tk
from datetime import datetime

import pyautogui
import win32con
import win32gui

import threading

import tkinter.font as tkFont

from common.keyword import inputContent

from pynput import keyboard

from log.log_record import debugLog, initLog
from request.qyrequest import QyRequest
from tools.socketHandle import socketHandle


def movePosition(x, y):
    ins = 100
    debugLog(pyautogui.position())
    cx, cy = pyautogui.position()
    xd = x - cx
    yd = y - cy
    debugLog(xd)
    debugLog(yd)
    if math.fabs(xd) > math.fabs(yd):
        pb = ins
        if yd != 0:
            pb = int(math.fabs(xd) / math.fabs(yd))
        if xd > 0:
            xi = pb
        else:
            xi = -pb
        if yd > 0:
            yi = 1
        else:
            yi = -1
        if ins / math.fabs(xi) >= 1:
            yi = yi * int(ins / math.fabs(xi))
            xi = xi * int(ins / math.fabs(xi))
    else:
        pb = ins
        if xd != 0:
            pb = int(math.fabs(yd) / math.fabs(xd));
        if xd > 0:
            xi = 1
        else:
            xi = -1
        if yd > 0:
            yi = pb
        else:
            yi = -pb
        if ins / math.fabs(yi) >= 1:
            xi = xi * int(ins / math.fabs(yi))
            yi = yi * int(ins / math.fabs(yi))
    debugLog(xi)
    debugLog(yi)
    while cy != y or cx != x:
        if (yd < 0 and cy + yi < y) or (yd > 0 and cy + yi > y) or yd == 0:
            cy = y
        else:
            cy = cy + yi
        if (xd < 0 and cx + xi < x) or (xd > 0 and cx + xi > x) or xd == 0:
            cx = x
        else:
            cx = cx + xi
        pyautogui.moveTo(cx, cy)


class APP:
    def __init__(self):
        self.positionheight = 100
        self.label = tk.Label(text='小飞chat助理托管中', font=('方正兰亭粗黑简体', '35'), fg='red', bg='white')
        debugLog(list(tkFont.families()))
        self.label.master.overrideredirect(True)
        # self.label.master.geometry("+900+150")
        self.label.master.lift()
        self.label.master.wm_attributes("-topmost", True)
        self.label.master.wm_attributes("-disabled", True)
        self.label.master.wm_attributes("-transparentcolor", "white")
        self.label.pack(fill=tk.BOTH)
        label1 = tk.Label(text='请不要移动鼠标', font=('方正大标宋简体', '35'), fg='red', bg='white')
        label1.pack(fill=tk.BOTH)
        self.str_var = tk.StringVar()  # 创建字符串变量
        self.str_var.set("鼠标坐标")  # 初始化字符串变量
        label2 = tk.Label(textvariable=self.str_var, font=('方正大标宋简体', '30'), fg='red', bg='white')
        label2.pack(fill=tk.BOTH)
        self.index = 1

    def add(self, text):
        label2 = tk.Label(text=text, font=('Times', '10'), fg='black', bg='white')
        label2.pack(fill=tk.BOTH)

    def keyListener(self):
        listener = keyboard.Listener(on_press=self.bindKey)
        # 启动监听器
        listener.start()
        # 进入主循环
        listener.join()

    def auto_op(self):
        thread1 = threading.Thread(target=self.openQW)
        thread1.start()

        thread2 = threading.Thread(target=self.position)
        thread2.start()

        thread3 = threading.Thread(target=self.openSocket)
        thread3.start()

        thread3 = threading.Thread(target=self.keyListener)
        thread3.start()

    def position(self):
        # 在下面的代码行中使用断点来调试脚本。
        x = 0
        y = 0
        try:
            while True:
                if x != pyautogui.position().x or y != pyautogui.position().y:
                    x, y = pyautogui.position()
                    positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
                    self.str_var.set('鼠标坐标:' + positionStr)
        except KeyboardInterrupt:
            debugLog('\n')

    def commonClick(self):
        movePosition(600, 900)
        pyautogui.click(600, 900)
        time.sleep(2)

    def bindKey(self, key):
        debugLog(key)
        if key == keyboard.Key.f1:
            self.findChatRoom()
        elif key == keyboard.Key.f2:
            self.clickLine()
        elif key == keyboard.Key.f3:
            self.clickJihe()
        elif key == keyboard.Key.f4:
            self.clickPhone()
        elif key == keyboard.Key.f5:
            self.clickCompany()
        elif key == keyboard.Key.f6:
            self.clickOrder()
        elif key == keyboard.Key.f7:
            self.clickqianyue()

    def openQW(self):
        debugLog("打开企业微信")
        # 在下面的代码行中使用断点来调试脚本。
        # self.add("宽度：" +
        #          str(pyautogui.size().width) + ",高度：" +
        #          str(pyautogui.size().height))
        hwnd = win32gui.FindWindow(None, "企业微信")
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 800, 1035, win32con.SWP_SHOWWINDOW)
        self.commonClick()

    def findChatRoom(self, name="美国旅游"):
        button7location = pyautogui.locateOnScreen('res/search.png', confidence=0.8)
        time.sleep(2)
        movePosition(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
        pyautogui.click(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
        time.sleep(2)
        inputContent(name)
        time.sleep(3)
        movePosition(140, 130)
        pyautogui.click(140, 130)
        time.sleep(2)
        movePosition(500, 550)
        pyautogui.click(500, 550)
        time.sleep(2)
        inputContent("您好")
        debugLog(button7location)
        time.sleep(2)
        try:
            zdylocation = pyautogui.locateOnScreen('res/zidingyi.png')
            if zdylocation is None:
                helplocation = pyautogui.locateOnScreen('res/help.png')
                time.sleep(2)
                movePosition(helplocation.left + helplocation.width / 2, helplocation.top + helplocation.height / 2)
                pyautogui.click(helplocation.left + helplocation.width / 2, helplocation.top + helplocation.height / 2)
        except Exception as e:
            debugLog(e)
        try:
            xiaofeilocation = pyautogui.locateOnScreen('res/xiaofei.png', confidence=0.9)
            time.sleep(2)
            movePosition(xiaofeilocation.left + xiaofeilocation.width / 2, xiaofeilocation.top + xiaofeilocation.height / 2)
            pyautogui.click(xiaofeilocation.left + xiaofeilocation.width / 2, xiaofeilocation.top + xiaofeilocation.height / 2)
        except Exception as e:
            debugLog(e)
        self.commonClick()

    def clickLine(self):
        self.clickzixuntab()
        button7location = pyautogui.locateOnScreen('res/line.png', confidence=0.7)
        time.sleep(2)
        movePosition(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
        pyautogui.click(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
        time.sleep(2)
        self.clicksendmsg()
        # movePosition(500, 550)
        # pyautogui.click(500, 550)
        # pyautogui.hotkey("enter")
        # self.commonClick()

    def clickJihe(self):
        self.clickzixuntab()
        button7location = pyautogui.locateOnScreen('res/jihetu.png', confidence=0.7)
        time.sleep(2)
        movePosition(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
        pyautogui.click(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
        time.sleep(3)
        self.clicksendmsg()
        # movePosition(500, 550)
        # pyautogui.click(500, 550)
        # pyautogui.hotkey("enter")
        # self.commonClick()

    def clickPhone(self):
        self.clickzixuntab()
        button7location = pyautogui.locateOnScreen('res/phone.png', confidence=0.7)
        time.sleep(2)
        movePosition(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
        pyautogui.click(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
        time.sleep(2)
        self.clicksendmsg()
        # movePosition(500, 550)
        # pyautogui.click(500, 550)
        # pyautogui.hotkey("enter")
        # self.commonClick()

    def clickCompany(self):
        self.clickzixuntab()
        button7location = pyautogui.locateOnScreen('res/company.png', confidence=0.7)
        time.sleep(2)
        movePosition(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
        pyautogui.click(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
        time.sleep(2)
        self.clicksendmsg()
        # movePosition(500, 550)
        # pyautogui.click(500, 550)
        # pyautogui.hotkey("enter")
        # self.commonClick()

    def clickOrder(self):
        self.clickordertab()
        button7location = pyautogui.locateOnScreen('res/addorder.png', confidence=0.7)
        time.sleep(2)
        movePosition(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
        pyautogui.click(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
        time.sleep(2)
        self.clicksendmsg()
        # movePosition(500, 550)
        # pyautogui.click(500, 550)
        # pyautogui.hotkey("enter")
        # self.commonClick()

    def clickqianyue(self):
        self.clickqianyuetab()
        button7location = pyautogui.locateOnScreen('res/qianyue.png', confidence=0.7)
        time.sleep(2)
        movePosition(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
        pyautogui.click(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
        time.sleep(2)
        self.clicksendmsg()
        # movePosition(500, 550)
        # pyautogui.click(500, 550)
        # pyautogui.hotkey("enter")
        # self.commonClick()

    def clickzixuntab(self):
        button7location = pyautogui.locateOnScreen('res/zixun.png', confidence=0.7)
        if button7location is not None:
            movePosition(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
            pyautogui.click(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
            time.sleep(2)

    def clickordertab(self):
        button7location = pyautogui.locateOnScreen('res/order.png', confidence=0.7)
        if button7location is not None:
            movePosition(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
            pyautogui.click(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
            time.sleep(2)

    def clickqianyuetab(self):
        button7location = pyautogui.locateOnScreen('res/qianyuetab.png', confidence=0.7)
        if button7location is not None:
            movePosition(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
            pyautogui.click(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
            time.sleep(2)

    def clicksendmsg(self):
        movePosition(400, 900)
        pyautogui.click(400, 900)
        pyautogui.hotkey("enter")
        self.commonClick()

    def handlemsg(self, msg):
        debugLog("获取客户聊天信息：" + msg)
        QyRequest().get_qychat_intent(msg)

    def scoketOp(self, data):
        debugLog(data)
        if data["data"]["type"] == 1 and data["data"]["subType"] == 1:
            self.clickLine()
            self.clickJihe()
        # elif data["data"]["type"] == 1 and data["data"]["subType"] == 2:
        elif data["data"]["type"] == 1 and data["data"]["subType"] == 3:
            self.clickPhone()
        elif data["data"]["type"] == 1 and data["data"]["subType"] == 4:
            self.clickCompany()
        elif data["data"]["type"] == 2 and data["data"]["subType"] == 1:
            self.clickOrder()
        elif data["data"]["type"] == 2 and data["data"]["subType"] == 2:
            self.clicksendmsg()
        elif data["data"]["type"] == 3:
            self.clickqianyue()
        elif data["data"]["type"] == 4:
            msg = data["data"]["msg"]
            self.handlemsg(msg)

    def openSocket(self):
        # pass
        socketHandle().openSocket(self.scoketOp)

    def center(self):
        ws = self.label.master.winfo_screenwidth()
        hs = self.label.master.winfo_screenheight()
        x = int((ws) - 700)
        y = 100
        self.label.master.geometry('+{}+{}'.format(x, y))

    """
    函数说明:loop等待用户事件
    """

    def loop(self):
        # 禁止修改窗口大小
        # self.root.resizable(False, False)
        # # 窗口居中
        self.center()
        self.label.mainloop()


if __name__ == '__main__':
    initLog()
    app = APP()  # 实例化APP对象
    app.auto_op()
    app.loop()  # loop等待用户事件
