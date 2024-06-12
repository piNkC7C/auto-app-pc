# import wx
#
# from tools.tools import CustomButton
#
#
# class FeiAssistPage(wx.Frame):
#     def __init__(self):
#         super().__init__(None, title="小飞助理", size=(550, 470), style=wx.NO_BORDER)
#         self.SetBackgroundColour(wx.Colour(245, 245, 245))  # 设置窗口背景颜色为白色
#
#         # 居中窗口
#         self.Center()
#
#         # 创建自定义标题栏
#         self.title_bar = wx.Panel(self, size=(550, 25))
#         self.title_bar.SetBackgroundColour(wx.Colour(245, 245, 245))  # 设置标题栏背景颜色为rgb(245,245,245)
#         self.title_bar.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
#
#         # 创建标题文本
#         self.title_text = wx.StaticText(self.title_bar, label="小飞助理", pos=(10, 5))
#         self.title_text.SetForegroundColour(wx.Colour(167, 166, 170))
#
#         # 创建关闭按钮
#         self.close_button = CustomButton(self.title_bar, label="×", pos=(515, 0), size=(35, 25), style=wx.NO_BORDER)
#         font = wx.Font(wx.FontInfo(12).Bold())
#         self.close_button.SetFont(font)
#         self.close_button.SetForegroundColour(wx.Colour(0, 0, 0))
#         self.close_button.SetBackgroundColour(wx.Colour(245, 245, 245))
#         self.close_button.Bind(wx.EVT_BUTTON, self.OnCloseButtonClick)
#         self.close_button.Bind(wx.EVT_ENTER_WINDOW, self.OnButtonEnter)
#         self.close_button.Bind(wx.EVT_LEAVE_WINDOW, self.OnButtonLeave)
#
#         # 创建左侧垂直 tab
#         self.vertical_tab = wx.Panel(self, size=(95, 470), pos=(0, 75))
#         self.vertical_tab.SetBackgroundColour(wx.Colour(245, 245, 245))  # 设置垂直 tab 背景颜色为 rgb(245,245,245)
#
#         # 绘制右边框
#         self.vertical_tab.Bind(wx.EVT_PAINT, self.OnPaint)
#
#         # 添加左侧 tab 页
#         self.tab_buttons = {}
#         for i, tab_name in enumerate(["小飞托管", "账号设置"]):
#             button = CustomButton(self.vertical_tab, label=tab_name, pos=(0, i * 32), size=(90, 32), style=wx.NO_BORDER)
#             self.tab_buttons[tab_name] = button
#             button.SetBackgroundColour(wx.Colour(245, 245, 245))  # 清除按钮背景色
#             button.SetForegroundColour(wx.Colour(0, 0, 0))  # 设置按钮文字颜色为黑色
#             button.Bind(wx.EVT_BUTTON, lambda event, name=tab_name: self.OnTabButtonClick(event, name))
#
#         # 创建右侧选项卡页
#         self.notebook = wx.Notebook(self, size=(455, 470), pos=(95, 75))
#         self.notebook.SetBackgroundColour(wx.Colour(245, 245, 245))  # 设置选项卡页背景颜色为 rgb(245,245,245)
#
#         # 添加右侧选项卡页
#         self.tab_pages = {
#             "小飞托管": wx.Panel(self.notebook),
#             "账号设置": wx.Panel(self.notebook)
#         }
#
#         for tab_name, tab_page in self.tab_pages.items():
#             self.notebook.AddPage(tab_page, tab_name)
#
#         # 默认激活第一个左侧 tab
#         self.ActivateTab("小飞托管")
#
#         # 绑定拖动窗口事件
#         self.Bind(wx.EVT_LEFT_DOWN, self.OnLeftDown)
#         self.Bind(wx.EVT_LEFT_UP, self.OnMouseUp)
#         self.Bind(wx.EVT_MOTION, self.OnMouseMove)
#
#     def OnLeftDown(self, event):
#         self.CaptureMouse()
#         self.delta = event.GetPosition()
#
#     def OnMouseMove(self, event):
#         if event.Dragging() and event.LeftIsDown():
#             pos = event.GetPosition()
#             self.SetPosition(self.GetPosition() + (pos - self.delta))
#
#     def OnMouseUp(self, event):
#         if self.HasCapture():
#             self.ReleaseMouse()
#
#     def OnCloseButtonClick(self, event):
#         self.Close()
#
#     def OnButtonEnter(self, event):
#         self.close_button.SetBackgroundColour(wx.Colour(251, 115, 115))
#         self.close_button.SetForegroundColour(wx.Colour(245, 245, 245))
#         # cursor = wx.Cursor(wx.CURSOR_HAND)
#         # self.close_button.SetCursor(cursor)
#
#     def OnButtonLeave(self, event):
#         self.close_button.SetBackgroundColour(wx.Colour(245, 245, 245))
#         self.close_button.SetForegroundColour(wx.Colour(0, 0, 0))
#
#     def OnTabButtonClick(self, event, tab_name):
#         self.ActivateTab(tab_name)
#
#     def ActivateTab(self, tab_name):
#         for name, button in self.tab_buttons.items():
#             button.SetForegroundColour(wx.Colour(0, 0, 0))  # 设置未激活 tab 的字体颜色为黑色
#             button.SetBackgroundColour(wx.Colour(245, 245, 245))  # 清除按钮背景色
#         active_button = self.tab_buttons[tab_name]
#         active_button.SetForegroundColour(wx.Colour(219, 41, 75))  # 设置激活 tab 的字体颜色为 rgb(219, 41, 75)
#         active_button.SetBackgroundColour(wx.Colour(245, 245, 245))  # 设置按钮背景色
#         self.notebook.SetSelection(list(self.tab_pages.keys()).index(tab_name))
#
#     def move_tab_indicator(self, active_button):
#         # 获取按钮位置和尺寸
#         x, y = active_button.GetPosition()
#
#         # 设置指示条位置和尺寸
#         if hasattr(self, 'tab_indicator'):
#             self.tab_indicator.SetPosition((93, y))
#             self.tab_indicator.SetSize((3, 32))
#         else:
#             # 创建指示条
#             self.tab_indicator = wx.Panel(self.vertical_tab, size=(3, 32),
#                                           pos=(93, y))
#             self.tab_indicator.SetBackgroundColour(wx.Colour(219, 41, 75))
#
#     def OnPaint(self, event):
#         dc = wx.PaintDC(self.vertical_tab)
#         dc.SetPen(wx.Pen(wx.Colour(227, 227, 227), width=5))
#         width, height = self.vertical_tab.GetSize()
#         dc.DrawLine(width, 0, width, height)
