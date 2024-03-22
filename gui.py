# -*- coding:utf-8 -*-
import math
import time

import win32api
import wx
# author：鹦秒科技
import tkinter as tk
from datetime import datetime

import pyautogui
import win32con
import win32gui

import threading

import tkinter.font as tkFont

from pynput import keyboard

# 访问其他文件
from common.keyword import inputContent
from log.log_record import debugLog
from request.qyrequest import QyRequest
from tools.socketHandle import socketHandle
from tools.fileOperate import File
from tools.error import ImageNotFoundException


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


class APP(wx.Frame):
    def __init__(self):
        super().__init__(None, title="")
        self.is_human = True

    def deal_task(self, task):
        debugLog(task)
        debugLog(task['image']['picName'])
        # 图片
        if task['actObjType'] == 'image':
            # 点击图片
            if task['action'] == 'move_click':
                # 点击工具栏
                if task['image']['picName'] == 'help':
                    xiaofei_notact = self.wait_pic('res/xiaofei_notact.png', 0.6, 1, 4, 2)
                    type_target = type(xiaofei_notact)
                    if type_target == dict:
                        help_notact = self.find_pic('res/help_notact.png', 0.9)
                        type_target = type(help_notact)
                        if type_target == dict:
                            return help_notact
                        else:
                            return self.move_click_pic(help_notact)
                    else:
                        return True

                # |点击小飞助理
                if task['image']['picName'] == 'xiaofei':
                    zixun = self.wait_pic('res/zixun.png', 0.9, 1, 4, 2)
                    type_target = type(zixun)
                    if type_target == dict:
                        xiaofei_notact = self.find_pic('res/xiaofei_notact.png', 0.9)
                        type_target = type(xiaofei_notact)
                        if type_target == dict:
                            return xiaofei_notact
                        else:
                            return self.move_click_pic(xiaofei_notact)
                    else:
                        return True

                # |点击小飞助理
                if task['image']['picName'] == 'zixun':
                    # 找激活状态的工具栏图标
                    zixun = self.wait_pic('res/zixun.png', 0.9, 1, 4, 2)
                    type_target = type(zixun)
                    if type_target == dict:
                        # 工具栏未激活
                        # 找未激活的工具栏图标
                        zixun_notact = self.find_pic('res/zixun_notact.png', 0.9)
                        type_target = type(zixun_notact)
                        if type_target == dict:
                            return zixun_notact
                        else:
                            return self.move_click_pic(zixun_notact)
                    else:
                        return True

                # 点击工具栏
                if task['image']['picName'] == 'external':
                    debugLog('点击客户')
                    movePosition(166, 130)
                    time.sleep(2)
                    self.is_human = False
                    pyautogui.click(166, 130)
                    self.is_human = True
                    return True

                # target_pic = None
                target_pic = self.wait_pic(f"res/{task['image']['picName']}.png", 0.9, 1, 4, 2)
                # target_pic = self.wait_pic(f"res/xiaofei.png", 0.9, 1, 4, 2)
                type_target = type(target_pic)
                if type_target == dict:
                    return target_pic
                else:
                    if task['isCircle'] == 1:
                        return self.circle_move_click_pic(target_pic, 1, 3, 3)
                    else:
                        return self.move_click_pic(target_pic)
        elif task['actObjType'] == 'text':
            if task['action'] == 'paste':
                self.is_human = False
                inputContent(task['text']['content'])
                self.is_human = True
                return True
            else:
                return "未识别的类型"
        else:
            return "未识别的任务"

    def openQW(self, open_num, max_num, wait_time):
        debugLog("打开企业微信")
        # 在下面的代码行中使用断点来调试脚本。
        # self.add("宽度：" +
        #          str(pyautogui.size().width) + ",高度：" +
        #          str(pyautogui.size().height))
        # 获取屏幕的宽度和高度
        width = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
        height = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

        # 查找窗口并将其设置为全屏大小
        hwnd = win32gui.FindWindow(None, "企业微信")
        win32gui.SetForegroundWindow(hwnd)
        win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, int(width / 2), int(height / 1.5),
                              win32con.SWP_SHOWWINDOW)
        time.sleep(2)
        debugLog("查看当前企业")
        cur_company = self.wait_pic('res/cur_company.png', 0.9, 1, 2, 2)
        if cur_company:
            self.move_click_pic(cur_company)
            cur_company_act = self.wait_pic('res/cur_company_act.png', 0.9, 1, 3, 2)
            if not cur_company_act:
                cur_company_notact = self.wait_pic('res/cur_company_notact.png', 0.9, 1, 3, 2)
                if cur_company_notact:
                    self.move_click_pic(cur_company_notact)
                else:
                    # 请手动切换企业
                    return False
            else:
                return True
        else:
            open_num += 1
            if open_num > max_num:
                # 请手动打开企业微信
                return False
            self.openQW(open_num, max_num, wait_time)

    def find_pic(self, pic_url, pic_confidence):
        try:
            target_pic = pyautogui.locateOnScreen(pic_url, confidence=pic_confidence)
            return target_pic
        except pyautogui.ImageNotFoundException:
            debugLog(f"未找到目标图片{pic_url}")
            # raise ImageNotFoundException(f"未找到目标图片{pic_url}")
            return {
                "left": False,
                "info": f"未找到目标图片{pic_url}",
            }
        except Exception as e:
            debugLog("寻找目标图片报错：" + str(e))
            return {
                "left": False,
                "info": "寻找目标图片报错：" + str(e),
            }

    def move_click_pic(self, target_pic):
        try:
            movePosition(target_pic.left + target_pic.width / 2, target_pic.top + target_pic.height / 2)
            time.sleep(2)
            self.is_human = False
            pyautogui.click(target_pic.left + target_pic.width / 2,
                            target_pic.top + target_pic.height / 2)
            self.is_human = True
            return True
        except Exception as e:
            debugLog("移动点击报错：" + str(e))
            return "移动点击报错：" + str(e)

    def circle_move_click_pic(self, target_pic, click_num, max_num, wait_time):
        try:
            click_num += 1
            if click_num > max_num:
                return True
            else:
                click_res = self.move_click_pic(target_pic)
                if click_res:
                    time.sleep(wait_time)
                    return self.circle_move_click_pic(target_pic, click_num, max_num, wait_time)
                else:
                    return click_res
        except Exception as e:
            debugLog("循环移动点击报错：" + str(e))
            return "循环移动点击报错：" + str(e)

    def wait_pic(self, pic_url, pic_confidence, wait_num, max_num, wait_time):
        try:
            target_pic = pyautogui.locateOnScreen(pic_url, confidence=pic_confidence)
            return target_pic
        except pyautogui.ImageNotFoundException:
            debugLog(f"循环找图未找到目标图片{pic_url}")
            wait_num += 1
            if wait_num > max_num:
                return {
                    "left": False,
                    "info": f"循环找图未找到目标图片{pic_url}",
                }
            time.sleep(wait_time)
            target_pic = self.wait_pic(pic_url, pic_confidence, wait_num, max_num, wait_time)
            return target_pic
        except Exception as e:
            debugLog("循环找图报错：" + str(e))
            return {
                "left": False,
                "info": "循环找图报错：" + str(e),
            }

    def find_tools(self):
        xiaofei_notact_pic = self.find_pic('res/xiaofei_notact.png', 0.9)
        if xiaofei_notact_pic:
            return True
        else:
            xiaofei_pic = self.wait_pic('res/xiaofei.png', 0.9, 1, 5, 2)
            if xiaofei_pic:
                return True
            else:
                return xiaofei_pic

    def find_xiaofei(self):
        xiaofei_pic = self.find_pic('res/xiaofei.png', 1)
        if xiaofei_pic:
            self.move_click_pic(xiaofei_pic)
            time.sleep(2)
            return True
        else:
            xiaofei_notact_pic = self.wait_pic('res/xiaofei_notact.png', 0.8, 1, 5, 2)
            if xiaofei_notact_pic:
                self.move_click_pic(xiaofei_notact_pic)
                time.sleep(2)
                return True
            else:
                return xiaofei_notact_pic

    def wait_xiaofei(self):
        zixun_pic = self.wait_pic('res/zixun.png', 0.9, 1, 10, 10)
        if zixun_pic:
            return True
        else:
            zixun_notact_pic = self.find_pic('res/zixun_notact.png', 0.9)
            if zixun_notact_pic:
                return True
            else:
                return zixun_notact_pic

    def common_operation(self, name):
        debugLog('找搜索框')
        search_pic = self.find_pic('res/search.png', 0.8)
        if search_pic:
            debugLog('点击搜索框')
            self.move_click_pic(search_pic)
            time.sleep(2)
            debugLog('输入客户名')
            self.is_human = False
            inputContent(name)
            self.is_human = True
            time.sleep(2)
            debugLog('点击客户')
            movePosition(166, 130)
            time.sleep(2)
            self.is_human = False
            pyautogui.click(166, 130)
            self.is_human = True
            time.sleep(2)
            debugLog('找聊天框')
            chat_room_pic = self.wait_pic('res/sendmsg.png', 0.9, 1, 10, 5)
            if chat_room_pic:
                debugLog('找工具栏')
                tools_res = self.find_tools()
                if not tools_res:
                    debugLog('找工具栏图标')
                    help_pic = self.find_pic('res/help.png', 0.9)
                    if help_pic:
                        self.move_click_pic(help_pic)
                        time.sleep(2)
                    else:
                        debugLog('未找到工具栏图标')
                        return help_pic
                debugLog('找小飞图标')
                xiaofei_res = self.find_xiaofei()
                if xiaofei_res:
                    debugLog('等待小飞加载')
                    zixun_res = self.wait_xiaofei()
                    debugLog(zixun_res)
                    if zixun_res:
                        debugLog('小飞加载成功')
                        time.sleep(3)
                        return True
                    else:
                        debugLog('小飞加载失败')
                        return zixun_res
            else:
                debugLog('未找到聊天框')
                return chat_room_pic
        else:
            self.openQW()
            time.sleep(5)
            common_res = self.common_operation(name)
            if common_res:
                return True
            else:
                return False

    def clickLine(self):
        line_pic = self.find_pic('res/line.png', 0.7)
        if line_pic:
            self.move_click_pic(line_pic)
            time.sleep(10)
            self.clicksendmsg(1)
            return True
        else:
            return False

    def clickJihe(self):
        jihetu_pic = self.find_pic('res/jihetu.png', 0.7)
        if jihetu_pic:
            self.move_click_pic(jihetu_pic)
            time.sleep(10)
            self.clicksendmsg(1)
            return True
        else:
            return False

    def clickPhone(self):
        phone_pic = self.find_pic('res/phone.png', 0.7)
        if phone_pic:
            self.move_click_pic(phone_pic)
            time.sleep(10)
            self.clicksendmsg(1)
            return True
        else:
            return False

    def clickCompany(self):
        company_pic = self.find_pic('res/company.png', 0.7)
        if company_pic:
            self.move_click_pic(company_pic)
            time.sleep(10)
            self.clicksendmsg(1)
            return True
        else:
            return False

    def clickOrder(self):
        addorder_pic = self.find_pic('res/addorder.png', 0.9)
        if addorder_pic:
            self.move_click_pic(addorder_pic)
            time.sleep(10)
            self.clicksendmsg(1)
            return True
        else:
            return False

    def clickqianyue(self):
        qianyue_pic = self.find_pic('res/qianyue.png', 0.9)
        if qianyue_pic:
            self.move_click_pic(qianyue_pic)
            time.sleep(10)
            self.clicksendmsg(1)
            return True
        else:
            return False

    def clickzixuntab(self):
        zixun_pic = self.find_pic('res/zixun.png', 0.9)
        if zixun_pic:
            return True
        else:
            zixun_notact_pic = self.find_pic('res/zixun_notact.png', 0.9)
            if zixun_notact_pic:
                self.move_click_pic(zixun_notact_pic)
                time.sleep(2)
                return True
            else:
                return zixun_notact_pic

    def clickordertab(self):
        button7location = pyautogui.locateOnScreen('res/order.png', confidence=0.7)
        if button7location is not None:
            movePosition(button7location.left + button7location.width / 2,
                         button7location.top + button7location.height / 2)
            pyautogui.click(button7location.left + button7location.width / 2,
                            button7location.top + button7location.height / 2)
            time.sleep(2)

    def clickqianyuetab(self):
        button7location = pyautogui.locateOnScreen('res/qianyuetab.png', confidence=0.7)
        if button7location is not None:
            movePosition(button7location.left + button7location.width / 2,
                         button7location.top + button7location.height / 2)
            pyautogui.click(button7location.left + button7location.width / 2,
                            button7location.top + button7location.height / 2)
            time.sleep(2)

    def clicksendmsg(self, click_num):
        sendmsg_pic = self.find_pic('res/sendmsg.png', 0.9)
        if sendmsg_pic:
            self.move_click_pic(sendmsg_pic)
            return
        click_num += 1
        if click_num > 5:
            return
        sendmsg_empty_pic = self.find_pic('res/sendmsg_empty.png', 0.9)
        if sendmsg_empty_pic:
            debugLog("发送为空")
            time.sleep(2)
            self.clicksendmsg(click_num)
        else:
            time.sleep(2)
            self.clicksendmsg(click_num)

    # def deal_task(self, task):
    #     debugLog(task)
    #     common_res = self.common_operation(task["externalName"])
    #     debugLog('公共操作结果')
    #     debugLog(common_res)
    #     if common_res:
    #         if task["tab"] == "咨询":
    #             zixun_res = self.clickzixuntab()
    #             debugLog('点击咨询tab结果')
    #             debugLog(common_res)
    #             if zixun_res:
    #                 if task["button"] == "行程":
    #                     line_res = self.clickLine()
    #                     if line_res:
    #                         return True
    #                     else:
    #                         return line_res
    #                 elif task["button"] == "销售手机":
    #                     phone_res = self.clickPhone()
    #                     if phone_res:
    #                         return True
    #                     else:
    #                         return phone_res
    #                 elif task["button"] == "公司信息":
    #                     company_res = self.clickCompany()
    #                     if company_res:
    #                         return True
    #                     else:
    #                         return company_res
    #             else:
    #                 return zixun_res
    #     else:
    #         return common_res

    def close(self):
        self.Destroy()

    # def __init__(self):
    #     self.positionheight = 100
    #     self.label = tk.Label(text='小飞chat助理托管中', font=('方正兰亭粗黑简体', '35'), fg='red', bg='white')
    #     debugLog(list(tkFont.families()))
    #     self.label.master.overrideredirect(True)
    #     # self.label.master.geometry("+900+150")
    #     self.label.master.lift()
    #     self.label.master.wm_attributes("-topmost", True)
    #     self.label.master.wm_attributes("-disabled", True)
    #     self.label.master.wm_attributes("-transparentcolor", "white")
    #     self.label.pack(fill=tk.BOTH)
    #     # label1 = tk.Label(text='请不要移动鼠标', font=('方正大标宋简体', '35'), fg='red', bg='white')
    #     # label1.pack(fill=tk.BOTH)
    #     self.str_var = tk.StringVar()  # 创建字符串变量
    #     self.str_var.set("鼠标坐标")  # 初始化字符串变量
    #     label2 = tk.Label(textvariable=self.str_var, font=('方正大标宋简体', '30'), fg='red', bg='white')
    #     label2.pack(fill=tk.BOTH)
    #     self.index = 1

    # def update_position(self, event):
    #     current_position = pyautogui.position()
    #     self.label.SetLabel(f"小飞助理托管中\n鼠标坐标: X={current_position.x}, Y={current_position.y}")
    #
    # def add(self, text):
    #     label2 = tk.Label(text=text, font=('Times', '10'), fg='black', bg='white')
    #     label2.pack(fill=tk.BOTH)
    #
    # def keyListener(self):
    #     listener = keyboard.Listener(on_press=self.bindKey)
    #     # 启动监听器
    #     listener.start()
    #     # 进入主循环
    #     listener.join()
    #
    # def auto_op(self, open_flag):
    #     # thread1 = MyThread(target_function=self.openQW)
    #     #
    #     # thread2 = MyThread(target_function=self.position)
    #     #
    #     # # thread3 = threading.Thread(target=self.openSocket)
    #     # # thread3.start()
    #     # #
    #     # # thread3 = threading.Thread(target=self.keyListener)
    #     # # thread3.start()
    #     # if open:
    #     #     thread1.start()
    #     #     thread2.start()
    #     # else:
    #     #     thread1.stop()
    #     #     thread2.stop()
    #     # if open_flag:
    #     # self.thread1 = MyThread(target_function=self.openQW, args=())
    #     # self.thread2 = threading.Thread(target=self.position)
    #     # self.thread1.start()
    #     # self.thread2.start()
    #     # else:
    #     # self.thread1.stop()
    #     # debugLog("关闭进程")
    #     # self.thread2.stop()
    #     pass
    #
    # # def position(self):
    # #     # 在下面的代码行中使用断点来调试脚本。
    # #     x = 0
    # #     y = 0
    # #     try:
    # #         while True:
    # #             if x != pyautogui.position().x or y != pyautogui.position().y:
    # #                 x, y = pyautogui.position()
    # #                 positionStr = 'X: ' + str(x).rjust(4) + ' Y: ' + str(y).rjust(4)
    # #                 self.str_var.set('鼠标坐标:' + positionStr)
    # #     except KeyboardInterrupt:
    # #         debugLog('\n')
    # def position(self):
    #     def update_position():
    #         nonlocal last_position
    #         current_position = pyautogui.position()
    #         if current_position != last_position:
    #             position_str = 'X: ' + str(current_position.x).rjust(4) + ' Y: ' + str(current_position.y).rjust(4)
    #             self.str_var.set('鼠标坐标:' + position_str)
    #             last_position = current_position
    #         self.label.master.after(100, update_position)  # 使用 after() 方法定时调用 update_position()
    #
    #     last_position = pyautogui.position()
    #     update_position()  # 第一次调用更新函数
    #
    # def commonClick(self):
    #     try:
    #         # 查找帮助图片
    #         fei_assist = pyautogui.locateOnScreen('res/xiaofei.png')
    #         if fei_assist:
    #             movePosition(fei_assist.left, fei_assist.top)
    #             pyautogui.click(fei_assist.left, fei_assist.top)
    #             time.sleep(2)
    #
    #     except pyautogui.ImageNotFoundException:
    #         debugLog("未找到聊天工具栏图片")
    #     try:
    #         # 查找帮助图片
    #         fei_assist = pyautogui.locateOnScreen('res/help.png')
    #         if fei_assist:
    #             movePosition(fei_assist.left, fei_assist.top)
    #             pyautogui.click(fei_assist.left, fei_assist.top)
    #             time.sleep(2)
    #
    #     except pyautogui.ImageNotFoundException:
    #         debugLog("未找到聊天工具栏图片")
    #
    # def bindKey(self, key):
    #     debugLog(key)
    #     if key == keyboard.Key.f1:
    #         self.findChatRoom()
    #     elif key == keyboard.Key.f2:
    #         self.clickLine()
    #     elif key == keyboard.Key.f3:
    #         self.clickJihe()
    #     elif key == keyboard.Key.f4:
    #         self.clickPhone()
    #     elif key == keyboard.Key.f5:
    #         self.clickCompany()
    #     elif key == keyboard.Key.f6:
    #         self.clickOrder()
    #     elif key == keyboard.Key.f7:
    #         self.clickqianyue()
    #
    # def findChatRoom(self, name):
    #     try:
    #         button7location = pyautogui.locateOnScreen('res/search.png', confidence=0.8)
    #     except pyautogui.ImageNotFoundException:
    #         debugLog("未找到搜索图片")
    #         self.openQW()
    #         time.sleep(2)
    #         button7location = pyautogui.locateOnScreen('res/search.png', confidence=0.8)
    #     movePosition(button7location.left + button7location.width / 2, button7location.top + button7location.height / 2)
    #     pyautogui.click(button7location.left + button7location.width / 2,
    #                     button7location.top + button7location.height / 2)
    #     time.sleep(2)
    #     inputContent(name)
    #     time.sleep(2)
    #     movePosition(140, 130)
    #     time.sleep(2)
    #     pyautogui.click(140, 130)
    #     time.sleep(3)
    #     # button1location = pyautogui.locateOnScreen('res/sendaddress.png', confidence=0.8)
    #     # movePosition(button1location.left + button1location.width / 2,
    #     #              button1location.top + button1location.height / 2)
    #     # pyautogui.click(button1location.left + button1location.width / 2,
    #     #                 button1location.top + button1location.height / 2)
    #     # time.sleep(2)
    #     # inputContent("您好")
    #     # time.sleep(2)
    #     try:
    #         pyautogui.locateOnScreen('res/zidingyi.png')
    #     except pyautogui.ImageNotFoundException:
    #         debugLog("未找到自定义图片")
    #         helplocation = pyautogui.locateOnScreen('res/help.png')
    #         movePosition(helplocation.left + helplocation.width / 2, helplocation.top + helplocation.height / 2)
    #         pyautogui.click(helplocation.left + helplocation.width / 2, helplocation.top + helplocation.height / 2)
    #         time.sleep(2)
    #     try:
    #         xiaofeilocation = pyautogui.locateOnScreen('res/xiaofei.png', confidence=0.9)
    #         movePosition(xiaofeilocation.left + xiaofeilocation.width / 2,
    #                      xiaofeilocation.top + xiaofeilocation.height / 2)
    #         pyautogui.click(xiaofeilocation.left + xiaofeilocation.width / 2,
    #                         xiaofeilocation.top + xiaofeilocation.height / 2)
    #         time.sleep(2)
    #     except Exception as e:
    #         debugLog(str(e))
    #     self.wait_fei_open(1)
    #
    # def wait_fei_open(self, wait_num):
    #     try:
    #         pyautogui.locateOnScreen('res/zixun.png', confidence=0.9)
    #     except pyautogui.ImageNotFoundException:
    #         debugLog("未找到激活咨询图片")
    #         try:
    #             pyautogui.locateOnScreen('res/zixun_notact.png', confidence=0.9)
    #         except pyautogui.ImageNotFoundException:
    #             debugLog("未找到咨询图片")
    #             debugLog("等待小飞助理加载")
    #             wait_num += 1
    #             if wait_num > 6:
    #                 pass
    #             else:
    #                 time.sleep(10)
    #                 self.wait_fei_open(wait_num)
    #
    # def handlemsg(self, msg):
    #     debugLog("获取客户聊天信息：" + msg)
    #     QyRequest().get_qychat_intent(msg)
    #
    # def scoketOp(self, data):
    #     debugLog(data)
    #     if data["data"]["type"] == 1 and data["data"]["subType"] == 1:
    #         self.clickLine()
    #         self.clickJihe()
    #     # elif data["data"]["type"] == 1 and data["data"]["subType"] == 2:
    #     elif data["data"]["type"] == 1 and data["data"]["subType"] == 3:
    #         self.clickPhone()
    #     elif data["data"]["type"] == 1 and data["data"]["subType"] == 4:
    #         self.clickCompany()
    #     elif data["data"]["type"] == 2 and data["data"]["subType"] == 1:
    #         self.clickOrder()
    #     elif data["data"]["type"] == 2 and data["data"]["subType"] == 2:
    #         self.clicksendmsg(1)
    #     elif data["data"]["type"] == 3:
    #         self.clickqianyue()
    #     elif data["data"]["type"] == 4:
    #         msg = data["data"]["msg"]
    #         self.handlemsg(msg)
    #
    # def openSocket(self):
    #     # pass
    #     socketHandle('123').openSocket(self.scoketOp)
    #
    # def center(self):
    #     ws = self.label.master.winfo_screenwidth()
    #     hs = self.label.master.winfo_screenheight()
    #     x = int((ws) - 700)
    #     y = 100
    #     self.label.master.geometry('+{}+{}'.format(x, y))
    #
    # """
    # 函数说明:loop等待用户事件
    # """
    #
    # # def loop(self):
    # #     # 禁止修改窗口大小
    # #     # self.root.resizable(False, False)
    # #     # # 窗口居中
    # #     self.center()
    # #     self.label.mainloop()
