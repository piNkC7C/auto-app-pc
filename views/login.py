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


class LoginPage(wx.Frame):
    def __init__(self, callback):
        super().__init__(None, title="小飞助理", size=(280, 380), style=wx.NO_BORDER)
        self.callback = callback
        self.SetBackgroundColour(wx.Colour(245, 245, 245))  # 设置窗口背景颜色为白色

        # 居中窗口
        self.Center()

        # 创建自定义标题栏
        self.title_bar = wx.Panel(self, size=(280, 25))
        self.title_bar.SetBackgroundColour(wx.Colour(245, 245, 245))  # 设置标题栏背景颜色为rgb(245,245,245)
        self.title_bar.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

        # 创建标题文本
        self.title_text = wx.StaticText(self.title_bar, label="小飞助理", pos=(10, 5))
        self.title_text.SetForegroundColour(wx.Colour(167, 166, 170))

        # 创建关闭按钮
        self.close_button = CustomButton(self.title_bar, label="×", pos=(250, 0), size=(35, 25), style=wx.NO_BORDER)
        font = wx.Font(wx.FontInfo(12).Bold())
        self.close_button.SetFont(font)
        self.close_button.SetForegroundColour(wx.Colour(0, 0, 0))
        self.close_button.SetBackgroundColour(wx.Colour(245, 245, 245))
        self.close_button.Bind(wx.EVT_BUTTON, self.OnCloseButtonClick)
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
        # print(get_fetassistid_api_res)
        self.feiassistid = generate_object_id()
        print(self.feiassistid)
        self.local_ip = get_local_ip()

        qr_exists = self.file_manager.check_qr_code_existence(self.feiassistid)
        if qr_exists:
            pass
        else:
            # 生成登录二维码
            state = json.dumps({
                "id": self.feiassistid,
                "ip": self.local_ip
            })
            link = f"http://miniwechat.iflying.com/api/externalAppHome?state={state}"
            print(link)
            # 创建 QRCodeGenerator 实例
            generator = QRCodeGenerator(link=link, fei_id=self.feiassistid)
            # 调用 generate_qr_code 方法生成二维码
            generator.generate_qr_code()

        # 创建并启动新线程以监听事件
        self.thread = threading.Thread(target=self.start_socket_listener, args=(f"{self.feiassistid}{self.local_ip}",))
        self.thread.start()

        # 在窗口中央放置二维码
        qr_path = f"assets/qrCode{self.feiassistid}.png"
        qr_image = wx.Image(qr_path, wx.BITMAP_TYPE_PNG)
        qr_image = qr_image.Scale(200, 200)  # 缩放二维码图像大小为150x150
        qr_bitmap = wx.StaticBitmap(self, -1, wx.Bitmap(qr_image))
        qr_bitmap.SetPosition((40, 110))

        # 绑定拖动窗口事件
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)

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
        self.file_manager.delete_files_with_name("assets", "qrCode")
        self.Destroy()

    def OnButtonEnter(self, event):
        self.close_button.SetBackgroundColour(wx.Colour(251, 115, 115))
        self.close_button.SetForegroundColour(wx.Colour(245, 245, 245))
        # cursor = wx.Cursor(wx.CURSOR_HAND)
        # self.close_button.SetCursor(cursor)

    def OnButtonLeave(self, event):
        self.close_button.SetBackgroundColour(wx.Colour(245, 245, 245))
        self.close_button.SetForegroundColour(wx.Colour(0, 0, 0))

    def start_socket_listener(self, feiassistid):
        print(feiassistid)
        # 实例化SocketHandler类
        socket_handler = socketHandle()
        # 开始监听事件
        socket_handler.openSocket(self.handle_message, feiassistid)

    def handle_message(self, data):
        self.file_manager.update_login_list(data['data']['userid'], data['data'])
        self.file_manager.update_login_info(data['data'])
        self.file_manager.delete_files_with_name("assets", "qrCode")
        # self.file_manager.delete_file(f"assets/qrCode{self.feiassistid}.png")
        # 在主线程中关闭当前窗口并打开FeiAssistPage
        wx.CallAfter(self.close_and_open_fei_assist_page)

    def close_and_open_fei_assist_page(self):
        self.Destroy()  # 销毁当前窗口
        self.callback()
