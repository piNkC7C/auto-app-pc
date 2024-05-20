import time

import wx
from wx.adv import TaskBarIcon
import urllib.request
import io
import threading
import asyncio

from tools.tools import CustomButton, CustomSwitch, MyThread
from tools.fileOperate import File
from tools.messageQueue import MessageQueueManager
from tools.globalListener import GlobalListener, KeyListener
from gui import APP
from .online import TipPage
from log.log_record import debugLog
from api.qwcosplayApi import qwcosplay_clear_all_task, qwcosplay_change_host_status, qwcosplay_get_check_company_task, \
    qwcosplay_check_host_status, qwcosplay_quick_send_msg_task
from .components.message import MessageBox
from tests.taskList import TestTaskRunner
from config.config import Configs


class FeiAssistPage(wx.Frame):
    def __init__(self, callback, taskbar_icon):
        self.config_data = Configs()
        app_config = self.config_data.app_info
        app_name = app_config["app_name"]
        app_ico = app_config["app_ico"]
        super().__init__(None, title=app_name, size=(550, 470), style=wx.NO_BORDER)
        self.busy = wx.BusyInfo("加载中，请稍候...")
        self.callback = callback
        self.SetBackgroundColour(wx.Colour(245, 245, 245))  # 设置窗口背景颜色为白色
        self.font12 = wx.Font(wx.FontInfo(12).FaceName('Microsoft YaHei UI'))
        self.font16 = wx.Font(wx.FontInfo(16).FaceName('Microsoft YaHei UI'))
        self.file_manager = File()
        self.info = self.file_manager.get_login_info(self.config_data.app_info['data_dir'])
        self.app_instance = APP()
        self.online_page = TipPage("在线", 57, 117, 198, 228, 240, 255)
        self.onAI_page = TipPage("托管中", 7, 193, 96, 228, 255, 230)
        self.offAI_page = TipPage("托管中断", 57, 117, 198, 251, 115, 115)
        self.status_page_show('online')
        self.message_queue_manager = MessageQueueManager()

        # 居中窗口
        self.Center()

        # 创建自定义标题栏
        self.title_bar = wx.Panel(self, size=(550, 25))
        self.title_bar.SetBackgroundColour(wx.Colour(245, 245, 245))  # 设置标题栏背景颜色为rgb(245,245,245)
        self.title_bar.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)

        # 创建标题文本
        self.title_text = wx.StaticText(self.title_bar, label=app_name, pos=(10, 5))
        self.title_text.SetForegroundColour(wx.Colour(167, 166, 170))

        # 创建关闭按钮
        self.close_button = CustomButton(self.title_bar, label="×", pos=(515, 0), size=(35, 25), style=wx.NO_BORDER)
        font = wx.Font(wx.FontInfo(12).Bold())
        self.close_button.SetFont(font)
        self.close_button.SetForegroundColour(wx.Colour(0, 0, 0))
        self.close_button.SetBackgroundColour(wx.Colour(245, 245, 245))
        self.close_button.Bind(wx.EVT_BUTTON, self.OnCloseButtonClick)
        self.close_button.Bind(wx.EVT_ENTER_WINDOW, self.OnButtonEnter)
        self.close_button.Bind(wx.EVT_LEAVE_WINDOW, self.OnButtonLeave)

        # 最小化到托盘
        self.fei_status = False
        self.taskbar_show = False
        self.taskbar_icon = taskbar_icon

        # 创建垂直tab
        self.vertical_tab = wx.Panel(self, size=(95, 470), pos=(0, 75))
        self.vertical_tab.SetBackgroundColour(wx.Colour(245, 245, 245))  # 设置垂直tab背景颜色为rgb(245,245,245)

        # 绘制右边框
        self.vertical_tab.Bind(wx.EVT_PAINT, self.OnPaint)

        # 添加tab页
        self.tab_pages = {
            "小飞托管": wx.Panel(self, size=(455, 470), pos=(95, 75)),
            "账号设置": wx.Panel(self, size=(455, 470), pos=(95, 75))
        }

        # 账号设置页
        self.rect_panel = wx.Panel(self.tab_pages["账号设置"], size=(350, 140), pos=(50, 10))
        self.rect_panel.SetBackgroundColour(wx.Colour(255, 255, 255))  # 设置矩形背景颜色为白色
        self.rect_panel.SetForegroundColour(wx.Colour(0, 0, 0))  # 设置矩形前景颜色为黑色
        self.rect_panel_avatar = wx.Panel(self.tab_pages["账号设置"], size=(50, 50), pos=(75, 55))
        login_info = self.file_manager.get_login_info(self.config_data.app_info['data_dir'])
        self.load_image_from_url(login_info['avatar'], self.rect_panel_avatar)
        self.rect_panel_name = wx.StaticText(self.tab_pages["账号设置"], label=login_info['name'], pos=(145, 62))
        # default_font = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        # debugLog("Default font face name:", default_font.GetFaceName())
        # debugLog("Default font size:", default_font.GetPointSize())
        self.rect_panel_name.SetFont(self.font16)
        self.rect_panel_name.SetBackgroundColour(wx.Colour(255, 255, 255))
        # 创建切换账号按钮
        self.switch_account_button = wx.Button(self.tab_pages["账号设置"], label="切换账号", size=(90, 32),
                                               pos=(180, 180))
        self.switch_account_button.SetBackgroundColour(wx.Colour(233, 233, 233))  # 设置背景色为rgb(233, 233, 233)
        self.switch_account_button.Bind(wx.EVT_BUTTON, self.OnSwitchAccountButtonClick)

        # 小飞托管
        self.fei_state_text = wx.StaticText(self.tab_pages["小飞托管"], label="托管状态", pos=(50, 0))
        self.fei_state_text.SetFont(self.font12)
        # 添加自定义开关组件
        # self.switch_panel = wx.Panel(self.tab_pages["小飞托管"], size=(50, 26), pos=(310, 0))
        # self.switch = CustomSwitch(self.switch_panel)
        # 添加自定义开关组件
        self.switch_panel = wx.Panel(self.tab_pages["小飞托管"], size=(25, 25), pos=(150, 0))
        self.switch = CustomSwitch(self.switch_panel, size=(25, 25), on_color=(7, 193, 96), off_color=(229, 229, 229),
                                   callback=self.get_fei_switch_state)

        # 创建tab按钮
        self.tab_buttons = {}
        for i, (tab_name, tab_page) in enumerate(self.tab_pages.items()):
            button = CustomButton(self.vertical_tab, label=tab_name, pos=(0, i * 32), size=(90, 32), style=wx.NO_BORDER)
            self.tab_buttons[tab_name] = button
            button.SetBackgroundColour(wx.Colour(245, 245, 245))  # 清除按钮背景色
            button.SetForegroundColour(wx.Colour(0, 0, 0))  # 设置按钮文字颜色为黑色
            button.Bind(wx.EVT_BUTTON, lambda event, page=tab_page: self.OnTabButtonClick(event, page))

        # 默认激活第一个tab
        self.ActivateTab("小飞托管", True)

        # 绑定拖动窗口事件
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)
        # self.OnCloseButtonClick("")
        del self.busy

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
        self.taskbar_show = False
        self.Show(False)
        # test_task_run = TestTaskRunner()
        # self.app_instance.deal_task_list(test_task_run.test_task
        #                                  , "1111111", 1)
        # self.message_queue_manager.insert_message_task({
        #     "UserId": self.info["userid"],
        #     "Status": time.time(),
        #     "taskList":test_task_run.test_task
        # }, f"Fei_{self.info['userid']}", self.deal_queue_error, "")

    def OnButtonEnter(self, event):
        self.close_button.SetBackgroundColour(wx.Colour(251, 115, 115))
        self.close_button.SetForegroundColour(wx.Colour(245, 245, 245))
        cursor = wx.Cursor(wx.CURSOR_HAND)
        self.close_button.SetCursor(cursor)

    def OnButtonLeave(self, event):
        self.close_button.SetBackgroundColour(wx.Colour(245, 245, 245))
        self.close_button.SetForegroundColour(wx.Colour(0, 0, 0))

    def OnTabButtonClick(self, event, page):
        self.ActivateTab(page.GetParent().FindWindow(event.GetId()).GetLabel(), True)
        # 显示新激活的内容页
        page.Show()
        # 刷新布局
        self.Layout()

    def ActivateTab(self, tab_name, hide_others):
        if hide_others:
            for name, tab_page in self.tab_pages.items():
                if name != tab_name:
                    tab_page.Hide()
        for name, button in self.tab_buttons.items():
            button.SetForegroundColour(wx.Colour(0, 0, 0))  # 设置未激活tab的字体颜色为黑色
            button.SetBackgroundColour(wx.Colour(245, 245, 245))  # 清除按钮背景色
        active_button = self.tab_buttons[tab_name]
        active_button.SetForegroundColour(wx.Colour(219, 41, 75))  # 设置激活tab的字体颜色为rgb(219, 41, 75)
        active_button.SetBackgroundColour(wx.Colour(245, 245, 245))  # 设置按钮背景色
        self.move_tab_indicator(active_button)

    def move_tab_indicator(self, active_button):
        # 获取按钮位置和尺寸
        x, y = active_button.GetPosition()

        # 设置指示条位置和尺寸
        if hasattr(self, 'tab_indicator'):
            self.tab_indicator.SetPosition((93, y))
            self.tab_indicator.SetSize((3, 32))
        else:
            # 创建指示条
            self.tab_indicator = wx.Panel(self.vertical_tab, size=(3, 32),
                                          pos=(93, y))
            self.tab_indicator.SetBackgroundColour(wx.Colour(219, 41, 75))

    def OnPaint(self, event):
        dc = wx.PaintDC(self.vertical_tab)
        dc.SetPen(wx.Pen(wx.Colour(227, 227, 227), width=5))
        width, height = self.vertical_tab.GetSize()
        dc.DrawLine(width, 0, width, height)

    def load_image_from_url(self, url, panel):
        # 从URL加载图像并显示在指定的面板上
        image_data = self.download_image(url)
        if image_data:
            try:
                stream = io.BytesIO(image_data)
                image = wx.Image(stream, wx.BITMAP_TYPE_ANY)
                image.Rescale(50, 50)  # 调整图像大小
                bitmap = wx.Bitmap(image)
                wx.StaticBitmap(panel, -1, bitmap, (0, 0))
            except Exception as e:
                debugLog(f"Error creating image from data:{e}")

    def download_image(self, url):
        # 下载图像数据
        try:
            with urllib.request.urlopen(url) as response:
                data = response.read()
                return data
        except Exception as e:
            debugLog(f"Error downloading image:{e}")
            return None

    def OnSwitchAccountButtonClick(self, event):
        wx.CallAfter(self.close_and_open_login_page)
        # debugLog("Switch Account Button Clicked!")

    def close_and_open_login_page(self):
        clear_res = asyncio.run(qwcosplay_clear_all_task(self.info['userid']))
        if clear_res['code'] == 200:
            self.callback()

    def status_page_show(self, page):
        if page == 'online':
            self.online_page.Show()
            self.onAI_page.Show(False)
            self.offAI_page.Show(False)
        elif page == 'onAI':
            self.online_page.Show(False)
            self.onAI_page.Show()
            self.offAI_page.Show(False)
        elif page == 'offAI':
            self.online_page.Show(False)
            self.onAI_page.Show(False)
            self.offAI_page.Show()
        else:
            pass

    def deal_queue_error(self):
        self.status_page_show('offAI')

    def deal_queue_no_error(self):
        self.status_page_show('onAI')

    def start_threading(self, queue, status):
        if status:
            global_listener = GlobalListener(self.get_fei_switch_state, (False,), self.app_instance)
            listener_thread = threading.Thread(target=global_listener.start_listening)
            listener_thread.start()
            consume_thread = threading.Thread(target=self.message_queue_manager.consume_message_task,
                                              args=(queue, self.app_instance.deal_task_json, True,
                                                    self.deal_queue_error, self.deal_queue_no_error,
                                                    self.info['userid'], self.app_instance.fei_num,))
            consume_thread.start()
            self.OnCloseButtonClick("")
        else:
            self.message_queue_manager.stop_consume_message_task(f"Fei_{self.info['userid']}")

    def get_fei_switch_state(self, switch):
        self.fei_status = switch
        if switch:
            debugLog("验证托管状态")
            status_check = asyncio.run(qwcosplay_check_host_status(self.info["userid"]))
            if status_check['code'] == 200 and status_check['data'] == 0:
                debugLog(status_check)
                debugLog("获取验证企业任务")
                company_check = asyncio.run(qwcosplay_get_check_company_task())
                if company_check['code'] == 200:
                    debugLog(company_check)
                    open_res = self.app_instance.deal_task_list(company_check['data'], 1, 1)
                    if open_res:
                        change_res = asyncio.run(qwcosplay_change_host_status(self.info["userid"], 1))
                        if change_res['code'] == 200:
                            debugLog("准备打开托管")
                            self.app_instance.fei_status = switch
                            self.app_instance.fei_num += 1
                            self.switch.refresh_switch(switch)
                            self.status_page_show('onAI')
                            self.taskbar_icon.OnCheck(self.taskbar_icon.open_item, self.taskbar_icon.close_item)
                            self.start_threading(f"Fei_{self.info['userid']}", switch)
                            # self.message_queue_manager.insert_message_task({
                            #     "UserId": self.info["userid"],
                            #     "Status": 1
                            # }, "feiAssistStatus", self.deal_queue_error)
            #             else:
            #                 wx.MessageBox(f"托管开启失败：{change_res}", "提示", wx.OK | wx.ICON_INFORMATION)
            #         else:
            #             wx.MessageBox(f"验证当前登录企业失败", "提示", wx.OK | wx.ICON_INFORMATION)
            # else:
            #     wx.MessageBox(f"托管开启失败：请检查是否已在其他地方打开托管", "提示", wx.OK | wx.ICON_INFORMATION)
        else:
            change_res = asyncio.run(qwcosplay_change_host_status(self.info["userid"], 0))
            if change_res['code'] == 200:
                self.app_instance.fei_status = switch
                self.switch.refresh_switch(switch)
                self.status_page_show('online')
                self.taskbar_icon.OnCheck(self.taskbar_icon.close_item, self.taskbar_icon.open_item)
                self.start_threading(f"Fei_{self.info['userid']}", switch)
                # self.message_queue_manager.insert_message_task({
                #     "UserId": self.info["userid"],
                #     "Status": 0
                # }, "feiAssistStatus", self.deal_queue_error)
                # self.message_queue_manager.stop_consume_message_task(self.info["userid"])
            # else:
            #     wx.MessageBox(f"托管关闭失败：{change_res}", "提示", wx.OK | wx.ICON_INFORMATION)

    def all_close(self):
        self.app_instance.Destroy()
        self.online_page.Destroy()
        self.onAI_page.Destroy()
        self.offAI_page.Destroy()
