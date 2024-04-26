import wx
from wx.adv import TaskBarIcon
import asyncio

from log.log_record import debugLog
from api.qwcosplayApi import qwcosplay_clear_all_task
from config.config import Configs
from tools.startup import check_to_startup, add_to_startup, remove_from_startup


class MyTaskBarIcon(TaskBarIcon):
    def __init__(self, frame, login_status, quik_task, key_listening):
        self.config_data = Configs()
        app_config = self.config_data.app_info
        app_name = app_config["app_name"]
        app_ico = app_config["app_ico"]
        TaskBarIcon.__init__(self)
        self.frame = frame
        self.login_status = login_status
        self.quik_task = quik_task
        self.key_listening = key_listening

        self.icon = wx.Icon(app_ico, wx.BITMAP_TYPE_ICO)
        self.SetIcon(self.icon, f"{app_name}")
        # 创建一个菜单
        self.menu = wx.Menu()

        # 添加菜单项
        self.open_item = self.menu.Append(wx.ID_ANY, "打开托管", kind=wx.ITEM_CHECK)
        self.close_item = self.menu.Append(wx.ID_ANY, "关闭托管", kind=wx.ITEM_CHECK)
        self.auto_open_item = self.menu.Append(wx.ID_ANY, "开机自启", kind=wx.ITEM_CHECK)
        self.destroy_item = self.menu.Append(wx.ID_ANY, "退出应用")

        # 绑定菜单项的事件处理函数
        self.Bind(wx.EVT_MENU, self.OnOpenFei, self.open_item)
        self.Bind(wx.EVT_MENU, self.OnCloseFei, self.close_item)
        self.Bind(wx.EVT_MENU, self.OnAutoOpen, self.auto_open_item)
        self.Bind(wx.EVT_MENU, self.OnDestroyFei, self.destroy_item)

        # 创建一个菜单
        self.no_login_menu = wx.Menu()

        # 添加菜单项
        self.no_login_auto_open_item = self.no_login_menu.Append(wx.ID_ANY, "开机自启", kind=wx.ITEM_CHECK)
        self.no_login_destroy_item = self.no_login_menu.Append(wx.ID_ANY, "退出应用")

        # 绑定菜单项的事件处理函数
        self.Bind(wx.EVT_MENU, self.OnAutoOpen, self.no_login_auto_open_item)
        self.Bind(wx.EVT_MENU, self.OnDestroyLogin, self.no_login_destroy_item)

        self.is_startup = check_to_startup(self.config_data.app_name)
        debugLog(f"开机启动状态：{self.is_startup}")
        if self.is_startup:
            self.auto_open_item.Check()
            self.no_login_auto_open_item.Check()
        else:
            self.auto_open_item.Check(False)
            self.no_login_auto_open_item.Check(False)

        # 检查当前的托管状态，并设置菜单项的勾选状态
        if self.login_status and self.frame.fei_status:
            self.open_item.Check()
        else:
            self.close_item.Check()

        self.Bind(wx.adv.EVT_TASKBAR_LEFT_DCLICK, self.OnTaskBarLeftDClick)
        self.Bind(wx.adv.EVT_TASKBAR_RIGHT_UP, self.OnTaskBarRightUp)

    def OnTaskBarLeftDClick(self, event):
        # debugLog(self.frame.taskbar_show)
        if not self.frame.taskbar_show:
            self.frame.Show(True)
        else:
            pass

    def OnTaskBarRightUp(self, event):
        if self.login_status:
            # 显示菜单
            self.PopupMenu(self.menu)
        else:
            self.PopupMenu(self.no_login_menu)

    def OnAutoOpen(self, event):
        if self.is_startup:
            remove_res = remove_from_startup(self.config_data.app_name)
            if remove_res:
                self.auto_open_item.Check(False)
                self.no_login_auto_open_item.Check(False)
                self.is_startup = False
            else:
                wx.MessageBox(f"关闭自启失败", "提示", wx.OK | wx.ICON_INFORMATION)
        else:
            add_res = add_to_startup(self.config_data.app_name)
            if add_res:
                self.auto_open_item.Check()
                self.no_login_auto_open_item.Check()
                self.is_startup = True
            else:
                wx.MessageBox(f"打开自启失败", "提示", wx.OK | wx.ICON_INFORMATION)

    def OnOpenFei(self, event):
        self.OnCheck(self.close_item, self.open_item)
        self.frame.get_fei_switch_state(True)

    def OnCloseFei(self, event):
        self.OnCheck(self.open_item, self.close_item)
        self.frame.get_fei_switch_state(False)

    def OnCheck(self, check, uncheck):
        check.Check()
        uncheck.Check(False)

    def stop_key_listening(self):
        if self.quik_task['code'] == 200:
            self.key_listening.stop_listening()

    def OnDestroyFei(self, event):
        clear_res = asyncio.run(qwcosplay_clear_all_task(self.frame.info['userid']))
        debugLog(clear_res)
        if clear_res['code'] == 200:
            self.frame.get_fei_switch_state(False)
            self.frame.all_close()
            self.frame.Destroy()
            self.stop_key_listening()
            self.Destroy()
            # 结束应用程序的主事件循环
            wx.App.Get().ExitMainLoop()
        # pass

    def OnDestroyLogin(self, event):
        self.frame.all_close()
        self.frame.Destroy()
        self.stop_key_listening()
        self.Destroy()
        # 结束应用程序的主事件循环
        wx.App.Get().ExitMainLoop()

    def OnChangeFei(self, event, page_name, frame):
        if page_name == 'login':
            if self.frame is not None:
                self.open_item.Check(False)
                self.close_item.Check()
                self.frame.get_fei_switch_state(False)
                self.frame.all_close()
                self.frame.Destroy()
            self.login_status = False
            self.frame = frame
        else:
            # 检查当前的托管状态，并设置菜单项的勾选状态
            if frame.fei_status:
                self.open_item.Check()
            else:
                self.close_item.Check()
            self.login_status = True
            self.frame = frame
