import wx

class MessageBox(wx.Frame):
    def __init__(self, parent, message, title):
        super().__init__(parent, title=title)

        # 显示一个提示框
        wx.MessageBox(message, title)

