import wx
from tools.fileOperate import File


class OnLinePage(wx.Frame):
    def __init__(self):
        super().__init__(None, title="", style=wx.BORDER_NONE | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        self.file_manager = File()
        self.login_info = self.file_manager.get_login_info()
        # 根据width设置换行文本
        self.tip_text = wx.StaticText(self, label=f"小飞chat助理 （在线）\n{self.login_info['name']}")
        # 创建一个sizer来管理布局
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tip_text, 0, wx.EXPAND | wx.ALL, 10)  # 添加静态文本到sizer，并设置边距
        self.SetSizer(sizer)  # 设置窗口的sizer

        font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)  # 调整字体大小
        self.tip_text.SetFont(font)
        self.tip_text.Wrap(255)
        self.Layout()

        self.tip_text.SetForegroundColour(wx.Colour(255, 255, 255))
        self.SetBackgroundColour(wx.Colour(0, 0, 255))  # 设置背景为蓝色

        # 将窗口放置在屏幕右上角
        screen_width, screen_height = wx.GetDisplaySize()
        text_width, text_height = self.tip_text.GetSize()
        self.Fit()  # 自适应标签的大小
        self.SetSize(self.GetSize())  # 设置窗口大小与标签大小匹配
        self.SetPosition((screen_width - self.GetSize()[0], screen_height - text_height - 199))
        # 绑定拖动窗口事件
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)

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

class OnAIPage(wx.Frame):
    def __init__(self):
        super().__init__(None, title="", style=wx.BORDER_NONE | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        self.file_manager = File()
        self.login_info = self.file_manager.get_login_info()
        # 根据width设置换行文本
        self.tip_text = wx.StaticText(self, label=f"小飞chat助理 （托管中）\n{self.login_info['name']}")
        # 创建一个sizer来管理布局
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tip_text, 0, wx.EXPAND | wx.ALL, 10)  # 添加静态文本到sizer，并设置边距
        self.SetSizer(sizer)  # 设置窗口的sizer

        font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)  # 调整字体大小
        self.tip_text.SetFont(font)
        self.tip_text.Wrap(305)
        self.Layout()

        self.tip_text.SetForegroundColour(wx.Colour(255, 0, 48))
        self.SetBackgroundColour(wx.Colour(0, 255, 0))  # 设置背景为蓝色

        # 将窗口放置在屏幕右上角
        screen_width, screen_height = wx.GetDisplaySize()
        text_width, text_height = self.tip_text.GetSize()
        self.Fit()  # 自适应标签的大小
        self.SetSize(self.GetSize())  # 设置窗口大小与标签大小匹配
        self.SetPosition((screen_width - self.GetSize()[0], screen_height - text_height - 199))
        # 绑定拖动窗口事件
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)

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

class OffAIPage(wx.Frame):
    def __init__(self):
        super().__init__(None, title="", style=wx.BORDER_NONE | wx.STAY_ON_TOP | wx.FRAME_NO_TASKBAR)
        self.file_manager = File()
        self.login_info = self.file_manager.get_login_info()
        # 根据width设置换行文本
        self.tip_text = wx.StaticText(self, label=f"小飞chat助理 （托管中断）\n{self.login_info['name']}")
        # 创建一个sizer来管理布局
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tip_text, 0, wx.EXPAND | wx.ALL, 10)  # 添加静态文本到sizer，并设置边距
        self.SetSizer(sizer)  # 设置窗口的sizer

        font = wx.Font(18, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)  # 调整字体大小
        self.tip_text.SetFont(font)
        self.tip_text.Wrap(305)
        self.Layout()

        self.tip_text.SetForegroundColour(wx.Colour(255, 255, 255))
        self.SetBackgroundColour(wx.Colour(255, 0, 0))  # 设置背景为蓝色

        # 将窗口放置在屏幕右上角
        screen_width, screen_height = wx.GetDisplaySize()
        text_width, text_height = self.tip_text.GetSize()
        self.Fit()  # 自适应标签的大小
        self.SetSize(self.GetSize())  # 设置窗口大小与标签大小匹配
        self.SetPosition((screen_width - self.GetSize()[0], screen_height - text_height - 199))
        # 绑定拖动窗口事件
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
        self.Bind(wx.EVT_MOTION, self.OnMouseMove)

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