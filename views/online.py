import wx
from tools.fileOperate import File
from config.config import Configs


class TipPage(wx.Frame):
    def __init__(self, status, fontcolor1, fontcolor2, fontcolor3, bgcolor1, bgcolor2, bgcolor3):
        super().__init__(None, title="", style=wx.BORDER_NONE | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        self.file_manager = File()
        self.config_data = Configs()
        app_config = self.config_data.app_info
        app_name = app_config["app_name"]
        app_ico = app_config["app_ico"]
        self.login_info = self.file_manager.get_login_info()

        # 创建上中下三个静态文本
        self.upper_text = wx.StaticText(self, label=f"{app_name}",
                                        style=wx.ALIGN_CENTER_HORIZONTAL)
        self.middle_text = wx.StaticText(self, label="", style=wx.ALIGN_CENTER_HORIZONTAL)
        # 控制中间文本的宽度
        self.middle_text.SetLabel(self._truncate_text(f"{self.login_info['name']}", 12))
        self.lower_text = wx.StaticText(self, label=f"{status}", style=wx.ALIGN_CENTER_HORIZONTAL)

        # 创建图标
        # icon = wx.Bitmap(app_png, wx.BITMAP_TYPE_PNG)
        # 创建图标盒子
        # box = wx.StaticBox(self, label="", size=(14, 14))
        # bitmap = wx.StaticBitmap(box, bitmap=icon)

        # 设置字体和颜色
        font_bold = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                            faceName='Microsoft YaHei UI')
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                       faceName='Microsoft YaHei UI')
        self.upper_text.SetFont(font_bold)
        self.upper_text.SetForegroundColour(wx.Colour(51, 51, 51))  # #333

        self.middle_text.SetFont(font)
        self.middle_text.SetForegroundColour(wx.Colour(51, 51, 51))  # #333

        self.lower_text.SetFont(font)
        self.lower_text.SetForegroundColour(wx.Colour(fontcolor1, fontcolor2, fontcolor3))  # #333

        # 创建一个sizer来管理布局
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 添加图标盒子到主 sizer 中
        # sizer.Add(box, 0, wx.EXPAND | wx.ALL, 0)

        # 将 StaticBoxSizer 添加到主 sizer 中
        sizer.Add(self.upper_text, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.middle_text, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.lower_text, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(sizer)  # 设置窗口的sizer

        self.Layout()

        # self.SetTransparent(150)  # 设置窗口透明度为150（0-255）

        self.SetBackgroundColour(wx.Colour(bgcolor1, bgcolor2, bgcolor3))  # 设置背景色

        # 将窗口放置在屏幕右上角
        rect = wx.Display(0).GetClientArea()  # 主屏幕
        taskbar_height = wx.GetDisplaySize()[1] - rect[3]  # 整个屏幕高度减去工作区域高度，即为任务栏的高度
        screen_width, screen_height = wx.GetDisplaySize()
        text_width, text_height = self.upper_text.GetSize()
        self.Fit()  # 自适应标签的大小
        self.SetSize(self.GetSize())  # 设置窗口大小与标签大小匹配
        self.SetPosition((screen_width - self.GetSize()[0], screen_height - text_height * 3 - taskbar_height - 60))
        # 绑定拖动窗口事件
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)

    def _truncate_text(self, text, max_length):
        if len(text) > max_length:
            return text[:max_length] + "..."
        return text

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
