import wx


class LoadingCom(wx.Dialog):
    def __init__(self, app_name, fontcolor1, fontcolor2, fontcolor3, bgcolor1, bgcolor2, bgcolor3):
        super().__init__(None, title="", style=wx.BORDER_NONE | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        self.panel = wx.Panel(self)
        self.upper_text = wx.StaticText(self.panel, label=f"{app_name}", style=wx.ALIGN_CENTER_HORIZONTAL)
        self.lower_text = wx.StaticText(self.panel, label=f"加载中...", style=wx.ALIGN_CENTER_HORIZONTAL)

        font_bold = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD,
                            faceName='Microsoft YaHei UI')
        font = wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL,
                       faceName='Microsoft YaHei UI')

        self.upper_text.SetFont(font_bold)
        self.upper_text.SetForegroundColour(wx.Colour(51, 51, 51))

        self.lower_text.SetFont(font)
        self.lower_text.SetForegroundColour(wx.Colour(fontcolor1, fontcolor2, fontcolor3))

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.upper_text, 0, wx.EXPAND | wx.ALL, 10)
        sizer.Add(self.lower_text, 0, wx.EXPAND | wx.ALL, 10)
        self.panel.SetSizer(sizer)
        self.panel.SetBackgroundColour(wx.Colour(bgcolor1, bgcolor2, bgcolor3))
        sizer.Fit(self)
        # self.Layout()
        # self.Fit()
        # self.SetSize(self.GetSize())
        self.Center()
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self):
        # Prevent the dialog from being closed by pressing the close button
        self.Destroy()


class CustomBusyDialog(wx.Dialog):
    def __init__(self, parent, message="加载中..."):
        super().__init__(parent, title="", style=wx.BORDER_NONE | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        self.panel = wx.Panel(self)
        self.message = message

        # self.bitmap = wx.StaticBitmap(self.panel, bitmap=wx.Bitmap("busy_icon.png", wx.BITMAP_TYPE_PNG))
        self.text = wx.StaticText(self.panel, label=self.message)

        sizer = wx.BoxSizer(wx.VERTICAL)
        # sizer.Add(self.bitmap, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        sizer.Add(self.text, 0, wx.ALIGN_CENTER | wx.ALL, 10)
        self.panel.SetSizer(sizer)
        sizer.Fit(self)

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self):
        # Prevent the dialog from being closed by pressing the close button
        self.Destroy()
