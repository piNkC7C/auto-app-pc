import wx

from .login import LoginPage
from .feiassist import FeiAssistPage
from tools.fileOperate import File


class IndexPage(wx.Frame):
    def __init__(self):
        super().__init__(None, title="", style=wx.NO_BORDER)
        file_manager = File()
        logged_in = file_manager.check_login_info()
        if logged_in:
            self.show_fei_assist_page()
        else:
            self.show_login_page()

    def show_fei_assist_page(self):
        self.Show(False)  # 隐藏主页窗口
        fei_assist_callback = lambda: self.show_login_page()
        frame = FeiAssistPage(callback=fei_assist_callback)
        frame.Show()

    def show_login_page(self):
        self.Show(False)  # 隐藏主页窗口
        login_callback = lambda: self.show_fei_assist_page()
        frame = LoginPage(callback=login_callback)
        frame.Show()
