import json
import wx

from request.qwcosplayRequest import QWCosplayRequest

from log.log_record import debugLog

# 创建QWCosplayRequest实例
qwcosplay_request = QWCosplayRequest()


# 任务开始
async def qwcosplay_task_start(taskId, startTime):
    try:
        debugLog("任务开始时间")
        debugLog(startTime)
        # 发送POST请求
        response = qwcosplay_request.post("/publicTask/task/start", json={
            'taskId': taskId,
            'startTime': startTime
        })
        return response
    except Exception as e:
        debugLog("An error occurred during request:")
        debugLog(str(e))
        wx.MessageBox(f"/publicTask/task/start：{str(e)}", "提示", wx.OK | wx.ICON_INFORMATION)
        return {
            "code": 999,
            "message": str(e)
        }


# 任务开始
async def qwcosplay_task_finish(taskId, finishTime):
    try:
        # 发送POST请求
        response = qwcosplay_request.post("/publicTask/task/finish", json={
            'taskId': taskId,
            'finishTime': finishTime
        })
        return response
    except Exception as e:
        debugLog("An error occurred during request:")
        debugLog(str(e))
        wx.MessageBox(f"/publicTask/task/finish：{str(e)}", "提示", wx.OK | wx.ICON_INFORMATION)
        return {
            "code": 999,
            "message": str(e)
        }


# 任务开始
async def qwcosplay_task_interrupt(taskId, interruptTime, interruptReason):
    try:
        # 发送POST请求
        response = qwcosplay_request.post("/publicTask/task/interrupt", json={
            'taskId': taskId,
            'interruptTime': interruptTime,
            'interruptReason': interruptReason
        })
        return response
    except Exception as e:
        debugLog("An error occurred during request:")
        debugLog(str(e))
        wx.MessageBox(f"/publicTask/task/interrupt：{str(e)}", "提示", wx.OK | wx.ICON_INFORMATION)
        return {
            "code": 999,
            "message": str(e)
        }


async def qwcosplay_clear_all_task(fyQyUserId):
    try:
        # 发送POST请求
        response = qwcosplay_request.post("/publicTask/task/clearAllTask", json={
            "fyQyUserId": fyQyUserId
        })
        return response
    except Exception as e:
        debugLog("An error occurred during request:")
        debugLog(str(e))
        wx.MessageBox(f"/publicTask/task/clearAllTask：{str(e)}", "提示", wx.OK | wx.ICON_INFORMATION)
        return {
            "code": 999,
            "message": str(e)
        }


async def qwcosplay_change_host_status(UserId, Status):
    try:
        # 发送POST请求
        response = qwcosplay_request.post("/reply/saleManage/changeHostingStatus", json={
            "userId": UserId,
            "status": Status
        })
        return response
    except Exception as e:
        debugLog("An error occurred during request:")
        debugLog(str(e))
        # wx.MessageBox(f"/reply/saleManage/changeHostingStatus：{str(e)}", "提示", wx.OK | wx.ICON_INFORMATION)
        return {
            "code": 999,
            "message": str(e)
        }


async def qwcosplay_user_watch_status(userId, saleId):
    try:
        # 发送POST请求
        response = qwcosplay_request.get("/reply/saleManage/getUserWatchStatus", params={
            "userId": userId,
            "saleId": saleId,
        })
        return response
    except Exception as e:
        debugLog("An error occurred during request:")
        debugLog(str(e))
        wx.MessageBox(f"/reply/saleManage/getUserWatchStatus：{str(e)}", "提示", wx.OK | wx.ICON_INFORMATION)
        return {
            "code": 999,
            "message": str(e)
        }


async def qwcosplay_get_check_company_task():
    try:
        # 发送POST请求
        response = qwcosplay_request.get("/reply/saleManage/getCheckCompanyTask")
        return response
    except Exception as e:
        debugLog("An error occurred during request:")
        debugLog(str(e))
        wx.MessageBox(f"/reply/saleManage/getCheckCompanyTask：{str(e)}", "提示", wx.OK | wx.ICON_INFORMATION)
        return {
            "code": 999,
            "message": str(e)
        }

async def qwcosplay_check_host_status(UserId):
    # 返回值0通过，1不通过
    try:
        # 发送POST请求
        response = qwcosplay_request.get("/reply/saleManage/checkHostingStatus", params={
            "userId": UserId,
        })
        return response
    except Exception as e:
        debugLog("An error occurred during request:")
        debugLog(str(e))
        # wx.MessageBox(f"/reply/saleManage/changeHostingStatus：{str(e)}", "提示", wx.OK | wx.ICON_INFORMATION)
        return {
            "code": 999,
            "message": str(e)
        }
