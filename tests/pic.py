import win32con
import win32gui
import pyautogui



program_name = 'WXWork.exe'  # 替换为你要判断的程序名称

hwnd = win32gui.FindWindow(None, "企业微信")
win32gui.SetForegroundWindow(hwnd)
win32gui.SetWindowPos(hwnd, win32con.HWND_NOTOPMOST, 0, 0, 800, 600, win32con.SWP_SHOWWINDOW)
im=pyautogui.screenshot()#截取整个屏幕
om=im.crop((1061,305,1090,320))#根据截取的屏幕仅截取“带赞的手势图片”，可以用pyautogui.mouseInfo()获取图片的位置(284,416,302,438)
om.save("dianzan.png")#将图片保存供pyautogui.locateOnScreen（）使用
