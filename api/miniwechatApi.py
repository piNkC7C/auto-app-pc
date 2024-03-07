from request.miniwechatRequest import MiniWechatRequest

# 创建MiniWechatRequest实例
miniwechat_request = MiniWechatRequest()

async def miniwechat_get_feiassistid():
    try:
        # 发送POST请求
        response = miniwechat_request.get("/getFeiAssisId")
        return response
    except Exception as e:
        print("An error occurred during request:", e)
        return None