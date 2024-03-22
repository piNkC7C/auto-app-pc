import json

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
        return None


# 获取图片集
async def miniwechat_get_feiassistpic(oldPicList):
    try:
        response = miniwechat_request.post("/getFeiPics", json={'oldPicList': oldPicList})
        return response
    except Exception as e:
        debugLog("An error occurred during request:")
        debugLog(str(e))
        return None
