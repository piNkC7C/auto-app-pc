import wx
from tools.fileOperate import File


class LoadingCom(wx.Frame):
    def __init__(self, app_name, fontcolor1, fontcolor2, fontcolor3, bgcolor1, bgcolor2, bgcolor3):
        super().__init__(None, title="", style=wx.BORDER_NONE | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        # 创建上中下三个静态文本
        self.upper_text = wx.StaticText(self, label=f"{app_name}",
                                        style=wx.ALIGN_CENTER_HORIZONTAL)
        # self.middle_text = wx.StaticText(self, label="", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.lower_text = wx.StaticText(self, label=f"加载中...", style=wx.ALIGN_CENTER_HORIZONTAL)

        # 设置字体和颜色
        font_bold = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                            faceName='Microsoft YaHei UI')
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                       faceName='Microsoft YaHei UI')
        self.upper_text.SetFont(font_bold)
        self.upper_text.SetForegroundColour(wx.Colour(51, 51, 51))  # #333

        # self.middle_text.SetFont(font)
        # self.middle_text.SetForegroundColour(wx.Colour(51, 51, 51))  # #333

        self.lower_text.SetFont(font)
        self.lower_text.SetForegroundColour(wx.Colour(fontcolor1, fontcolor2, fontcolor3))  # #333

        # 创建一个sizer来管理布局
        sizer = wx.BoxSizer(wx.VERTICAL)

        # 将 StaticBoxSizer 添加到主 sizer 中
        sizer.Add(self.upper_text, 0, wx.EXPAND | wx.ALL, 10)
        # sizer.Add(self.middle_text, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.lower_text, 0, wx.EXPAND | wx.ALL, 10)

        self.SetSizer(sizer)  # 设置窗口的sizer

        self.Layout()

        self.SetBackgroundColour(wx.Colour(bgcolor1, bgcolor2, bgcolor3))  # 设置背景色

        # 将窗口放置在屏幕右上角
        self.Fit()  # 自适应标签的大小
        self.SetSize(self.GetSize())  # 设置窗口大小与标签大小匹配
        self.Center()
