import os

from tools.startup import get_windows_username


class Configs:
    def __init__(self):
        self.win_username = get_windows_username()
        self.app_version = 'v0.1'
        self.app_name = '朱会潇·销售助理'
        self.app_info = {
            "app_name": f"{self.app_name}{self.app_version}",
            "app_ico": "res/0/zhuhuixiao.ico",
        }
        self.queue_info = {
            "hostname": "124.71.164.184",
            "port": 5672,
            "username": "iflying",
            "password": "mq_iflying_2019"
        }
        self.has_start_use_path = ['assets', 'has_start_use.json']
