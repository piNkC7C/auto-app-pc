import wx
import threading
import asyncio
import os
import sys
import subprocess

from .login import LoginPage
from .feiassist import FeiAssistPage
from tools.fileOperate import File
from tools.socketHandle import socketHandle
from log.log_record import debugLog
from api.miniwechatApi import miniwechat_get_feiassistpic, miniwechat_check_login_status
from .components.loading import LoadingCom, CustomBusyDialog
from tools.updateApp import check_for_updates, download_update


class IndexPage(wx.Frame):
    def __init__(self):
        super().__init__(None, title="", style=wx.BORDER_NONE | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        self.busy = wx.BusyInfo("检查下载更新...")
        self.update_wait = None
        self.app_version = 'v1.1'
        debugLog(f"版本号：{self.app_version}")
        self.app_name = '朱会潇·销售助理'
        self.app_info = {
            "app_name": f"{self.app_name}{self.app_version}",
            "app_ico": "res/0/zhuhuixiao.ico",
        }
        self.file_manager = File()
        # 初始化app配置
        self.file_manager.write_json_info_by_folder(['assets', 'app.json'], self.app_info)
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
        # 检查更新
        check_res = self.check_update()
        if check_res == 0:
            del self.update_wait
            debugLog("启动更新脚本")
            # 启动新的独立进程
            subprocess.Popen(["update.exe"])
        elif check_res == 1:
            del self.update_wait
            dlg_result = wx.MessageBox("安装包下载失败", "提示", wx.OK | wx.ICON_INFORMATION)
            # 检查用户的响应
            if dlg_result == wx.OK:
                # 用户点击了确定按钮
                sys.exit()
        else:
            del self.busy
            self.download_wait = wx.BusyInfo("下载资源...")
            self.init_data()

        # self.busy = LoadingCom(self.app_info['app_name'], 57, 117, 198, 228, 240, 255)
        # self.busy = CustomBusyDialog(self)
        # self.busy.Show()

    def check_update(self):
        update_res = check_for_updates(self.app_version)
        debugLog(update_res)
        debugLog(f"{self.app_name}{self.app_version}")
        if update_res:
            del self.busy
            self.update_wait = wx.BusyInfo("下载安装包...")
            # 备用目录
            download_res = download_update(self.app_name)
            if download_res:
                debugLog(f"{self.app_name}{update_res['message']}下载完成")
                return 0
            return 1
        else:
            return 2

    def init_data(self):
        # 队列配置
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
                del self.download_wait
                # self.busy.on_close()
                # busy.on_close()
                self.show_fei_assist_page()
            else:
                del self.download_wait
                # self.busy.on_close()
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
