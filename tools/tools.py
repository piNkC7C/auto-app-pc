import wx
import threading


class CustomButton(wx.Button):
    def __init__(self, parent, label, pos=wx.DefaultPosition, size=wx.DefaultSize, style=0):
        super().__init__(parent, label=label, pos=pos, size=size, style=style)
        self.SetCursor(wx.Cursor(wx.CURSOR_HAND))  # 设置按钮的鼠标悬停样式为手型


class CustomSwitch(wx.Panel):
    def __init__(self, parent, size=(25, 25), on_color=(7, 193, 96), off_color=(229, 229, 229), callback=None):
        super().__init__(parent, size=size)
        self.on_color = on_color
        self.off_color = off_color
        self.active = False
        self.callback = callback  # 添加回调函数
        self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnMouseEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnMouseLeave)

    def HitTest(self, pt):
        """
        Check if the given point is within the button area.
        """
        rect = self.GetClientRect()
        return rect.Contains(pt)

    def toggle(self, event):
        if self.callback:
            self.callback(not self.active)

    def refresh_switch(self, status):
        self.active = status
        self.Refresh()

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        dc.Clear()
        size = self.GetSize()
        width, height = size.GetWidth(), size.GetHeight()
        if self.active:
            dc.SetBrush(wx.Brush(wx.Colour(self.on_color)))
            label = "ON"
        else:
            dc.SetBrush(wx.Brush(wx.Colour(self.off_color)))
            label = "OFF"
        dc.DrawRectangle(0, 0, width, height)
        dc.SetTextForeground(wx.BLACK)
        dc.SetFont(wx.Font(wx.FontInfo(10)))
        text_width, text_height = dc.GetTextExtent(label)
        dc.DrawText(label, (width - text_width) // 2, (height - text_height) // 2)

    def OnMouseEnter(self, event):
        cursor = wx.Cursor(wx.CURSOR_HAND)
        self.SetCursor(cursor)

    def OnMouseLeave(self, event):
        self.SetCursor(wx.NullCursor)

    def OnLeftDown(self, event):
        pt = event.GetPosition()
        if self.HitTest(pt):
            self.toggle(event)
        else:
            event.Skip()  # 如果不在按钮区域内，则继续处理该事件


class MyThread(threading.Thread):
    def __init__(self, target_function, args=()):
        super().__init__()
        self.target_function = target_function
        self.args = args
        self.running = threading.Event()

    def run(self):
        self.running.set()
        try:
            while self.running.is_set():
                self.target_function(*self.args)
        except Exception as e:
            print(f"Error occurred in thread: {e}")  # 可以根据需要扩展错误处理逻辑
        finally:
            self.running.clear()

    def stop(self):
        self.running.clear()
        self.stop()

# class MyThread(threading.Thread):
#     def __init__(self, target_function, args):
#         super().__init__()
#         self.target_function = target_function
#         self.args = args  # 将args作为元组存储
#         self.running = True  # 使用标志控制线程是否运行
#
#     def run(self):
#         while self.running:
#             self.target_function(*self.args)  # 解包args传递给target_function
#
#     def stop(self):
#         self.running = False  # 设置标志为False，通知线程退出
