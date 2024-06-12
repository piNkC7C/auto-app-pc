import requests
import wx
import asyncio
from requests.auth import HTTPBasicAuth

from log.log_record import debugLog

from tools.fileOperate import File
from config.config import Configs
from api.miniwechatApi import miniwechat_get_feiassistauth


class QWCosplayRequest:
    def __init__(self):
        self.base_url = "http://qwcosplay.iflying.com/api"
        # self.base_url = "http://172.16.61.31:7094"
        self.timeout = 120
        self.file_manager = File()
        self.config_data = Configs()

    def request(self, method, url, **kwargs):
        full_url = self.base_url + url
        try:
            debugLog(f"{full_url}请求参数：")
            debugLog(f"{kwargs}")
            info = self.file_manager.get_login_info(self.config_data.app_info['data_dir'])
            # if info:
            # debugLog(info)
            check_res = miniwechat_get_feiassistauth(f"{info['feiassistid']}", info['feiassistauth'])
            # debugLog(check_res)
            # debugLog("111111111")
            response = requests.request(method, full_url, timeout=self.timeout,
                                        auth=HTTPBasicAuth(f"{info['feiassistid']}", info['feiassistauth']),
                                        **kwargs)
            # else:
            # debugLog(info)
            # response = requests.request(method, full_url, timeout=self.timeout, **kwargs)
            response.raise_for_status()  # 检查请求是否成功
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            debugLog("A qwcosplay.iflying.com HTTPError occurred：")
            debugLog(str(http_err))
            if http_err.response.status_code == 401:
                debugLog("鉴权失败")
            return {
                "code": http_err.response.status_code,
                "message": str(http_err)
            }
        except requests.exceptions.RequestException as e:
            debugLog("Another qwcosplay.iflying.com error occurred：")
            debugLog(str(e))
            # wx.MessageBox("qwcosplay.iflying.com接口报错，请联系管理员！", "提示", wx.OK | wx.ICON_INFORMATION)
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


class QWCosplayRequestNoAuth:
    def __init__(self):
        self.base_url = "http://qwcosplay.iflying.com/api"
        # self.base_url = "http://172.16.61.31:7094"
        self.timeout = 120
        self.file_manager = File()
        self.config_data = Configs()

    def request(self, method, url, **kwargs):
        full_url = self.base_url + url
        try:
            debugLog(f"{full_url}请求参数：")
            debugLog(f"{kwargs}")
            # info = self.file_manager.get_login_info(self.config_data.app_info['data_dir'])
            # if info:
            #     # debugLog(info)
            #     check_res = miniwechat_get_feiassistauth(f"{info['feiassistid']}", info['feiassistauth'])
            #     # debugLog(check_res)
            #     # debugLog("111111111")
            #     response = requests.request(method, full_url, timeout=self.timeout,
            #                                 auth=HTTPBasicAuth(f"{info['feiassistid']}", info['feiassistauth']),
            #                                 **kwargs)
            # else:
            # debugLog(info)
            response = requests.request(method, full_url, timeout=self.timeout, **kwargs)
            response.raise_for_status()  # 检查请求是否成功
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            debugLog("A qwcosplay.iflying.com HTTPError occurred：")
            debugLog(str(http_err))
            if http_err.response.status_code == 401:
                debugLog("鉴权失败")
            return {
                "code": http_err.response.status_code,
                "message": str(http_err)
            }
        except requests.exceptions.RequestException as e:
            debugLog("Another qwcosplay.iflying.com error occurred：")
            debugLog(str(e))
            # wx.MessageBox("qwcosplay.iflying.com接口报错，请联系管理员！", "提示", wx.OK | wx.ICON_INFORMATION)
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
