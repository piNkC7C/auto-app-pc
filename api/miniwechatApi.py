import json
import wx

from request.miniwechatRequest import MiniWechatRequest

from log.log_record import debugLog

# 创建MiniWechatRequest实例
miniwechat_request = MiniWechatRequest()


# 获取小飞id
async def miniwechat_get_feiassistid():
    try:
        # 发送POST请求
        response = miniwechat_request.get("/getFeiAssistId")
        return response
    except Exception as e:
        debugLog("An error occurred during request:")
        debugLog(str(e))
        wx.MessageBox(f"mimniwechat/getFeiAssistId：{str(e)}", "提示", wx.OK | wx.ICON_INFORMATION)
        return {
            "code": 999,
            "message": str(e)
        }


# 获取图片集
async def miniwechat_get_feiassistpic(oldPicList):
    try:
        response = miniwechat_request.post("/getFeiPics", json={'oldPicList': oldPicList})
        return response
    except Exception as e:
        debugLog("An error occurred during request:")
        debugLog(str(e))
        wx.MessageBox(f"mimniwechat/getFeiPics：{str(e)}", "提示", wx.OK | wx.ICON_INFORMATION)
        return {
            "code": 999,
            "message": str(e)
        }


async def miniwechat_check_login_status(json):
    try:
        response = miniwechat_request.post("/checkLoginStatus", json=json)
        return response
    except Exception as e:
        debugLog("An error occurred during request:")
        debugLog(str(e))
        wx.MessageBox(f"mimniwechat/checkLoginStatus：{str(e)}", "提示", wx.OK | wx.ICON_INFORMATION)
        return {
            "code": 999,
            "message": str(e)
        }


async def miniwechat_get_feiassistversion(version):
    try:
        # 发送POST请求
        response = miniwechat_request.get("/getFeiAssistVersion", params={
            "version": version,
        })
        return response
    except Exception as e:
        debugLog("An error occurred during request:")
        debugLog(str(e))
        wx.MessageBox(f"mimniwechat/getFeiAssistVersion：{str(e)}", "提示", wx.OK | wx.ICON_INFORMATION)
        return {
            "code": 999,
            "message": str(e)
        }
