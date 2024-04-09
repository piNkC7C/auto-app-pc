import wx


class LoadingCom(wx.Frame):
    def __init__(self, parent, app_name, fontcolor1, fontcolor2, fontcolor3, bgcolor1, bgcolor2, bgcolor3):
        super().__init__(parent, title="", style=wx.BORDER_NONE | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)

        self.upper_text = wx.StaticText(self, label=f"{app_name}", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.lower_text = wx.StaticText(self, label=f"加载中...", style=wx.ALIGN_CENTER_HORIZONTAL)

        font_bold = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                            faceName='Microsoft YaHei UI')
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                       faceName='Microsoft YaHei UI')

        self.upper_text.SetFont(font_bold)
        self.upper_text.SetForegroundColour(wx.Colour(fontcolor1, fontcolor2, fontcolor3))

        self.lower_text.SetFont(font)
        self.lower_text.SetForegroundColour(wx.Colour(fontcolor1, fontcolor2, fontcolor3))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.upper_text, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.lower_text, 0, wx.EXPAND | wx.ALL, 10)
        self.SetSizer(sizer)
        self.Layout()
        self.SetBackgroundColour(wx.Colour(bgcolor1, bgcolor2, bgcolor3))
        self.Fit()
        self.SetSize(self.GetSize())
        self.Center()

    def close(self):
        self.Destroy()

    @staticmethod
    def show(parent, app_name, fontcolor1, fontcolor2, fontcolor3, bgcolor1, bgcolor2, bgcolor3):
        app = wx.App()
        busy_info = LoadingCom(parent, app_name, fontcolor1, fontcolor2, fontcolor3, bgcolor1, bgcolor2, bgcolor3)
        busy_info.Show()
        app.MainLoop()
        return busy_info
