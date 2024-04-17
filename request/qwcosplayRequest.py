import requests
import wx
from requests.auth import HTTPBasicAuth

from log.log_record import debugLog

from tools.fileOperate import File


class QWCosplayRequest:
    def __init__(self):
        # self.base_url = "http://qwcosplay.iflying.com/api"
        self.base_url = "http://172.16.61.31:7094"
        self.timeout = 120
        self.file_manager = File()

    def request(self, method, url, **kwargs):
        full_url = self.base_url + url
        try:
            debugLog(f"{full_url}请求参数：")
            debugLog(f"{kwargs}")
            info = self.file_manager.get_login_info()
            # debugLog(info)
            response = requests.request(method, full_url, timeout=self.timeout,
                                        auth=HTTPBasicAuth(f"{info['feiassistid']}", info['feiassistauth']),
                                        **kwargs)
            response.raise_for_status()  # 检查请求是否成功
            return response.json()
        except requests.exceptions.RequestException as e:
            print(e)
            debugLog("An error occurred during request:")
            debugLog(str(e))
            wx.MessageBox("qwcosplay.iflying.com接口报错，请联系管理员！", "提示", wx.OK | wx.ICON_INFORMATION)
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
