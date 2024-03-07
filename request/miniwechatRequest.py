import requests

class MiniWechatRequest:
    def __init__(self):
        self.base_url = "http://miniwechat.iflying.com/api"
        # self.base_url = "http://127.0.0.1:4745/api"
        self.timeout = 10

    def request(self, method, url, **kwargs):
        full_url = self.base_url + url
        try:
            response = requests.request(method, full_url, timeout=self.timeout, **kwargs)
            response.raise_for_status()  # 检查请求是否成功
            return response.json()
        except requests.exceptions.RequestException as e:
            print("An error occurred during request:", e)
            return None

    def get(self, url, **kwargs):
        return self.request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self.request('POST', url, **kwargs)

    def put(self, url, **kwargs):
        return self.request('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.request('DELETE', url, **kwargs)