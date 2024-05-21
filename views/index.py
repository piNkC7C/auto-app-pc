import time

import wx
import threading
import asyncio
import os
import sys
import subprocess
import shutil
import ctypes

from .login import LoginPage
from .feiassist import FeiAssistPage
from tools.fileOperate import File
from tools.socketHandle import socketHandle
from log.log_record import debugLog
from api.miniwechatApi import miniwechat_get_feiassistpic, miniwechat_check_login_status
from api.qwcosplayApi import qwcosplay_quick_send_msg_task
from .components.loading import LoadingCom, CustomBusyDialog
from tools.updateApp import check_for_updates, download_update, download_update_exe
from config.config import Configs
from .components.taskBarIcon import MyTaskBarIcon
from tools.globalListener import GlobalListener, KeyListener
from tools.startup import add_to_startup, remove_from_startup


class IndexPage(wx.Frame):
    def __init__(self):
        super().__init__(None, title="", style=wx.BORDER_NONE | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        self.busy = wx.BusyInfo("检查下载更新...")
        self.update_wait = None
        self.config_data = Configs()
        self.app_version = self.config_data.app_version
        debugLog(f"版本号：{self.app_version}")
        self.app_name = self.config_data.app_name
        self.update_name = self.config_data.update_name
        self.taskbar_icon = None

        # self.app_info = self.config_data.app_info
        self.file_manager = File()
        # remove_from_startup(self.app_name)
        # 获取当前目录的绝对路径作为target_path
        # target_path = os.path.abspath(os.path.join(f"dist\\{self.app_name}.exe"))
        # startup_folder = f"C:\\Users\\{self.config_data.win_username}\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup"
        # shortcut_path = os.path.join(startup_folder, f"{self.app_name}.lnk")
        # if not os.path.exists(shortcut_path):
        #     os.symlink(target_path, shortcut_path)
        # 初始化app配置
        # self.file_manager.write_json_info_by_folder(['assets', 'app.json'], self.app_info)
        # self.queue_info = self.config_data.queue_info
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
        elif check_res == 2:
            self.download_wait = wx.BusyInfo("下载资源...")
            self.quick_task = asyncio.run(qwcosplay_quick_send_msg_task())
            self.key_listening = None
            if self.quick_task['code'] == 200:
                debugLog("打开快捷键监听")
                self.key_listening = KeyListener(self.quick_task['data']['keyList'],
                                                 self.quick_task['data']['instructionList'],
                                                 self.quick_task['data']['keyReleaseList'])
                self.key_listening_thread = threading.Thread(target=self.key_listening.start_listening)
                self.key_listening_thread.start()
            self.init_data()
        else:
            if check_res['code'] == 997:
                dlg_result = wx.MessageBox("请关闭代理，重新打开应用！", "提示", wx.OK | wx.ICON_INFORMATION)
                # 检查用户的响应
                if dlg_result == wx.OK:
                    # 用户点击了确定按钮
                    sys.exit()
            else:
                sys.exit()

        # self.busy = LoadingCom(self.app_info['app_name'], 57, 117, 198, 228, 240, 255)
        # self.busy = CustomBusyDialog(self)
        # self.busy.Show()

    def check_update(self):
        """

        :return: 0(更新且安装包下载成功)，1（更新但安装包下载失败），2（无需更新），返回获取版本号接口报错信息（获取版本号接口出问题）
        """
        update_res = check_for_updates(self.app_version)
        debugLog("检测更新结果")
        debugLog(update_res)
        debugLog(f"{self.app_name}{self.app_version}")
        del self.busy
        if update_res['code'] == 0:
            debugLog("管理员权限")
            debugLog(ctypes.windll.shell32.IsUserAnAdmin())
            user_admin = ctypes.windll.shell32.IsUserAnAdmin()
            if user_admin == 0:
                ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, sys.argv[0], None, 1)
                sys.exit()
            self.update_wait = wx.BusyInfo("下载安装包...")
            # 备用目录
            download_res = download_update(self.app_name)
            download_update_res = download_update_exe(self.update_name)
            time.sleep(0.5)
            if download_res and download_update_res:
                debugLog(f"{self.app_name}{update_res['message']}下载完成")
                return 0
            return 1
        elif update_res['code'] == 1:
            return 2
        else:
            return update_res

    def init_data(self):
        # 队列配置
        # self.file_manager.write_json_info_by_folder(['assets', 'queue.json'], self.queue_info)
        # 设置当前目录信息
        # self.file_manager.write_json_info_by_folder(['assets', 'app_info.json'], self.config_data.app_info)
        # 删除原配置文件
        self.file_manager.delete_file([self.config_data.app_info['data_dir'], 'assets', 'queue.json'])
        self.file_manager.delete_file([self.config_data.app_info['data_dir'], 'assets', 'app.json'])
        # 下载图片
        oldPicList = self.file_manager.get_json_info_by_folder(
            [self.config_data.app_info['data_dir'], 'assets', 'images.json'])
        picList = asyncio.run(miniwechat_get_feiassistpic(oldPicList))
        if picList['code'] == 0:
            self.file_manager.write_json_info_by_folder(
                [self.config_data.app_info['data_dir'], 'assets', 'images.json'],
                picList['data']['pics'])
            if picList['data']['newPics'].__len__() > 0:
                for pic in picList['data']['newPics']:
                    self.file_manager.download_image(pic['PicUrl'], pic['PicName'],
                                                     [self.config_data.app_info['data_dir'], 'res', pic['PicRate'],
                                                      pic['PicName']])
        # 设置开机自启动
        has_start_use = self.file_manager.check_json_by_folder(self.config_data.has_start_use_path)
        if not has_start_use:
            add_res = add_to_startup(self.config_data.app_name)
            debugLog(f"自动开启自启结果{add_res}")
            if add_res:
                self.file_manager.write_json_info_by_folder(self.config_data.has_start_use_path, {})
        self.taskbar_icon = MyTaskBarIcon(None, False, self.quick_task, self.key_listening)
        # 验证登录
        info = self.file_manager.get_login_info(self.config_data.app_info['data_dir'])
        check_res = asyncio.run(miniwechat_check_login_status(info))
        debugLog("登陆验证结果")
        debugLog(check_res)
        if check_res['code'] == 0:
            if check_res['data'] == '验证成功':
                del self.download_wait
                # self.busy.on_close()
                # busy.on_close()
                self.show_fei_assist_page(False)
            else:
                del self.download_wait
                # self.busy.on_close()
                self.show_login_page(False)

    def show_fei_assist_page(self, page_show):
        self.Show(False)  # 隐藏主页窗口
        fei_assist_callback = lambda: self.show_login_page(True)
        fei_frame = FeiAssistPage(callback=fei_assist_callback, taskbar_icon=self.taskbar_icon)
        self.taskbar_icon.OnChangeFei(self.taskbar_icon.destroy_item, 'feiassist', fei_frame)
        fei_frame.Show(page_show)
        info = self.file_manager.get_login_info(self.config_data.app_info['data_dir'])
        # 实例化SocketHandler类
        self.socket = socketHandle(f"{info['feiassistid']}", fei_frame.get_fei_switch_state)

    def show_login_page(self, page_show):
        self.stop_socket_listener()
        self.Show(False)  # 隐藏主页窗口
        login_callback = lambda: self.show_fei_assist_page(True)
        frame = LoginPage(callback=login_callback, taskbar_icon=self.taskbar_icon)
        self.taskbar_icon.OnChangeFei(self.taskbar_icon.destroy_item, 'login', frame)
        frame.Show(page_show)

    def stop_socket_listener(self):
        if self.socket:
            self.socket.disconnect()
