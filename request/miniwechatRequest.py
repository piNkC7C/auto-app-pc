import requests
import wx

from log.log_record import debugLog

class MiniWechatRequest:
    def __init__(self):
        self.base_url = "http://miniwechat.iflying.com/api"
        # self.base_url = "http://172.16.61.6:4745/api"
        self.timeout = 10

    def request(self, method, url, **kwargs):
        full_url = self.base_url + url
        try:
            response = requests.request(method, full_url, timeout=self.timeout, **kwargs)
            response.raise_for_status()  # 检查请求是否成功
            return response.json()
        except requests.exceptions.ProxyError as e:
            debugLog("A proxy error occurred:")
            debugLog(str(e))
            return {
                "code": 997,
                "message": str(e)
            }
        except requests.exceptions.ConnectionError as e:
            debugLog("A Connection error occurred:")
            debugLog(str(e))
            return {
                "code": 998,
                "message": str(e)
            }
        except requests.exceptions.RequestException as e:
            debugLog("Another error occurred:")
            debugLog(str(e))
            wx.MessageBox("miniwechat接口报错，请联系管理员！", "提示", wx.OK | wx.ICON_INFORMATION)
            return {
                "code": 999,
                "message": str(e)
            }

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        return self.request('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)