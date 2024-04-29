import wx
import asyncio
import os
import json
import urllib.parse
import threading

from api.miniwechatApi import miniwechat_get_feiassistid
from tools.qrcodeGenerator import QRCodeGenerator
from tools.socketHandle import socketHandle
from tools.fileOperate import File
from tools.tools import CustomButton, get_local_ip, generate_object_id
from log.log_record import debugLog
from config.config import Configs


class LoginPage(wx.Frame):
    def __init__(self, callback, taskbar_icon):
        self.config_data = Configs()
        app_config = self.config_data.app_info
        app_name = app_config["app_name"]
        app_ico = app_config["app_ico"]
        super().__init__(None, title=app_name, size=(280, 380), style=wx.NO_BORDER)

        self.callback = callback
        self.taskbar_show = True
        self.taskbar_icon = taskbar_icon
        self.SetBackgroundColour(wx.Colour(245, 245, 245))  # 设置窗口背景颜色为白色

        # 居中窗口
        self.Center()

        # 创建自定义标题栏
        self.title_bar = wx.Panel(self, size=(280, 25))
        self.title_bar.SetBackgroundColour(wx.Colour(245, 245, 245))  # 设置标题栏背景颜色为rgb(245,245,245)
        self.title_bar.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

        # 创建标题文本
        self.title_text = wx.StaticText(self.title_bar, label=app_name, pos=(10, 5))
        self.title_text.SetForegroundColour(wx.Colour(167, 166, 170))

        # 创建最小化按钮
        # self.Iconic_button = CustomButton(self.title_bar, label="—", pos=(215, 0), size=(35, 25), style=wx.NO_BORDER)
        # font = wx.Font(wx.FontInfo(12).Bold())
        # self.Iconic_button.SetFont(font)
        # self.Iconic_button.SetForegroundColour(wx.Colour(0, 0, 0))
        # self.Iconic_button.SetBackgroundColour(wx.Colour(245, 245, 245))
        # self.Iconic_button.Bind(wx.EVT_BUTTON, self.OnIconicButtonClick)
        # self.Iconic_button.Bind(wx.EVT_ENTER_WINDOW, self.OnIconicButtonEnter)
        # self.Iconic_button.Bind(wx.EVT_LEAVE_WINDOW, self.OnIconicButtonLeave)

        # 创建关闭按钮
        self.close_button = CustomButton(self.title_bar, label="×", pos=(250, 0), size=(35, 25), style=wx.NO_BORDER)
        font = wx.Font(wx.FontInfo(12).Bold())
        self.close_button.SetFont(font)
        self.close_button.SetForegroundColour(wx.Colour(0, 0, 0))
        self.close_button.SetBackgroundColour(wx.Colour(245, 245, 245))
        # self.close_button.Bind(wx.EVT_BUTTON, self.OnCloseButtonClick)
        self.close_button.Bind(wx.EVT_BUTTON, self.OnIconicButtonClick)
        self.close_button.Bind(wx.EVT_ENTER_WINDOW, self.OnButtonEnter)
        self.close_button.Bind(wx.EVT_LEAVE_WINDOW, self.OnButtonLeave)

        # 添加文字 "扫码登录"
        login_text = wx.StaticText(self, label="扫码登录", pos=(98, 65))
        font = wx.Font(wx.FontInfo(16).FaceName("微软雅黑"))
        login_text.SetFont(font)
        login_text.SetForegroundColour(wx.Colour(219, 41, 75))

        # 获取小飞助理id
        self.file_manager = File()
        # get_fetassistid_api_res = asyncio.run(miniwechat_get_feiassistid())
        # debugLog(get_fetassistid_api_res)
        self.feiassistid = generate_object_id()
        # debugLog(self.feiassistid)
        self.local_ip = get_local_ip()

        qr_exists = self.file_manager.check_qr_code_existence(self.feiassistid, app_config['data_dir'])
        if qr_exists:
            pass
        else:
            # 生成登录二维码
            state = json.dumps({
                "id": self.feiassistid,
                "ip": self.local_ip
            })
            link = f"http://miniwechat.iflying.com/api/externalAppHome?state={state}"
            # link = f"http://172.16.61.6:4745/api/externalAppHome?state={state}"

            # debugLog(link)
            # 创建 QRCodeGenerator 实例
            generator = QRCodeGenerator(link=link, fei_id=self.feiassistid)
            # 调用 generate_qr_code 方法生成二维码
            generator.generate_qr_code(app_config['data_dir'])

        # 实例化SocketHandler类
        self.socket_handler = socketHandle(f"{self.feiassistid}{self.local_ip}", None)

        # 创建并启动新线程以监听事件
        self.socket_thread = threading.Thread(target=self.start_socket_listener)
        self.socket_thread.start()

        # 在窗口中央放置二维码
        qr_path = f"{app_config['data_dir']}/assets/qrCode{self.feiassistid}.png"
        qr_image = wx.Image(qr_path, wx.BITMAP_TYPE_PNG)
        qr_image = qr_image.Scale(200, 200)  # 缩放二维码图像大小为150x150
        qr_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(qr_image))
        qr_bitmap.SetPosition((40, 110))

        # 绑定拖动窗口事件
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)

        self.OnIconicButtonClick("")

    def OnLeftDown(self, event):
        self.CaptureMouse()
        self.delta = event.GetPosition()

    def OnMouseMove(self, event):
        if event.Dragging() and event.LeftIsDown():
            pos = event.GetPosition()
            self.SetPosition(self.GetPosition() + (pos - self.delta))

    def OnMouseUp(self, event):
        if self.HasCapture():
            self.ReleaseMouse()

    def OnCloseButtonClick(self, event):
        self.socket_handler.disconnect()
        self.file_manager.delete_files_with_name(f"{self.config_data.app_info['data_dir']}\\assets", "qrCode")
        self.taskbar_icon.stop_key_listening()
        self.Destroy()

        # 结束应用程序的主事件循环
        wx.App.Get().ExitMainLoop()

    def OnIconicButtonClick(self, event):
        self.taskbar_show = False
        self.Show(False)

    def all_close(self):
        self.socket_handler.disconnect()
        self.file_manager.delete_files_with_name(f"{self.config_data.app_info['data_dir']}\\assets", "qrCode")

    def OnButtonEnter(self, event):
        self.close_button.SetBackgroundColour(wx.Colour(251, 115, 115))
        self.close_button.SetForegroundColour(wx.Colour(245, 245, 245))
        # cursor = wx.Cursor(wx.CURSOR_HAND)
        # self.close_button.SetCursor(cursor)

    def OnButtonLeave(self, event):
        self.close_button.SetBackgroundColour(wx.Colour(245, 245, 245))
        self.close_button.SetForegroundColour(wx.Colour(0, 0, 0))

    def OnIconicButtonEnter(self, event):
        self.Iconic_button.SetBackgroundColour(wx.Colour(226, 226, 226))

    def OnIconicButtonLeave(self, event):
        self.Iconic_button.SetBackgroundColour(wx.Colour(245, 245, 245))

    def start_socket_listener(self):
        # 开始监听事件
        self.socket_handler.openSocket(self.handle_message)

    def handle_message(self, data):
        # self.file_manager.update_login_list(data['data']['userid'], data['data'])
        self.file_manager.update_login_info(data['data'], self.config_data.app_info['data_dir'])
        self.file_manager.delete_files_with_name(f"{self.config_data.app_info['data_dir']}\\assets", "qrCode")
        # 在主线程中关闭当前窗口并打开FeiAssistPage
        wx.CallAfter(self.close_and_open_fei_assist_page)

    def close_and_open_fei_assist_page(self):
        self.socket_handler.disconnect()
        self.Destroy()  # 销毁当前窗口
        self.callback()
