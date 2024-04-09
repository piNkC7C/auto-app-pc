import wx
import threading
import asyncio

from .login import LoginPage
from .feiassist import FeiAssistPage
from tools.fileOperate import File
from tools.socketHandle import socketHandle
from log.log_record import debugLog
from api.miniwechatApi import miniwechat_get_feiassistpic, miniwechat_check_login_status
from .components.loading import LoadingCom


class IndexPage(wx.Frame):
    def __init__(self):
        super().__init__(None, title="", style=wx.BORDER_NONE | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        self.app_info = {
            "app_name": "朱会潇·销售助理",
            "app_ico": "res/0/zhuhuixiao.ico",
            # "app_png": "res/0/zhuhuixiao.png",
        }
        self.queue_info = {
            "hostname": "124.71.164.184",
            "port": 5672,
            "username": "iflying",
            "password": "mq_iflying_2019"
        }
        # loading页面
        # loading = LoadingCom(self.app_info['app_name'], 57, 117, 198, 228, 240, 255)
        # loading.Show()
        self.socket = None
        self.file_manager = File()
        self.init_data()

    def init_data(self):
        # 初始化app配置
        self.file_manager.write_json_info_by_folder(['assets', 'app.json'], self.app_info)
        self.file_manager.write_json_info_by_folder(['assets', 'queue.json'], self.queue_info)
        # 下载图片
        oldPicList = self.file_manager.get_json_info_by_folder(['assets', 'images.json'])
        picList = asyncio.run(miniwechat_get_feiassistpic(oldPicList))
        if picList['code'] == 0:
            self.file_manager.write_json_info_by_folder(['assets', 'images.json'],
                                                        picList['data']['pics'])
            if picList['data']['newPics'].__len__() > 0:
                for pic in picList['data']['newPics']:
                    self.file_manager.download_image(pic['PicUrl'], pic['PicName'],
                                                     ['res', pic['PicRate'], pic['PicName']])
        # 验证登录
        info = self.file_manager.get_login_info()
        check_res = asyncio.run(miniwechat_check_login_status(info))
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
        fei_frame = FeiAssistPage(callback=fei_assist_callback)
        fei_frame.Show()
        info = self.file_manager.get_login_info()
        # 实例化SocketHandler类
        self.socket = socketHandle(f"{info['feiassistid']}", fei_frame.get_fei_switch_state)

    def show_login_page(self):
        self.stop_socket_listener()
        self.Show(False)  # 隐藏主页窗口
        login_callback = lambda: self.show_fei_assist_page()
        frame = LoginPage(callback=login_callback)
        frame.Show()

    def stop_socket_listener(self):
        if self.socket:
            self.socket.disconnect()
