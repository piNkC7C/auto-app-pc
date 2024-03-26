import wx
import threading
import asyncio

from .login import LoginPage
from .feiassist import FeiAssistPage
from tools.fileOperate import File
from tools.socketHandle import socketHandle
from log.log_record import debugLog
from api.miniwechatApi import miniwechat_get_feiassistpic, miniwechat_check_login_status


class IndexPage(wx.Frame):
    def __init__(self):
        super().__init__(None, title="", style=wx.NO_BORDER)
        self.socket = None
        self.file_manager = File()
        oldPicList = self.file_manager.get_json_info_by_folder(['assets', 'images.json'])
        picList = asyncio.run(miniwechat_get_feiassistpic(oldPicList))
        if picList['code'] == 0:
            if picList['data'].__len__() > 0:
                # debugLog(picList['data'])
                newPicList = self.file_manager.write_json_info_by_folder(['assets', 'images.json'], picList['data'])
                for pic in newPicList:
                    self.file_manager.download_image(pic['PicUrl'], pic['PicName'], ['res', pic['PicName']])
        self.info = self.file_manager.get_login_info()
        check_res = asyncio.run(miniwechat_check_login_status(self.info))
        debugLog("登陆验证结果")
        debugLog(check_res)
        if check_res['code'] == 0:
            if check_res['data'] == '验证成功':
                self.show_fei_assist_page()
            else:
                self.show_login_page()

    def show_fei_assist_page(self):
        self.Show(False)  # 隐藏主页窗口
        fei_assist_callback = lambda: self.show_login_page()
        frame = FeiAssistPage(callback=fei_assist_callback)
        frame.Show()
        info = self.file_manager.get_login_info()
        # 实例化SocketHandler类
        self.socket = socketHandle(f"{info['feiassistid']}", frame.get_fei_switch_state)

    def show_login_page(self):
        self.stop_socket_listener()
        self.Show(False)  # 隐藏主页窗口
        login_callback = lambda: self.show_fei_assist_page()
        frame = LoginPage(callback=login_callback)
        frame.Show()

    def stop_socket_listener(self):
        if self.socket:
            self.socket.disconnect()
