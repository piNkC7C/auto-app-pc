import os


class Configs:
    def __init__(self):
        self.win_username = os.environ['USERNAME']
        self.app_version = 'v0.0.3'
        self.app_name = '朱会潇·销售助理'
        self.update_name = 'update'
        roaming_dir = os.path.join(os.getenv('APPDATA'), 'zhuhuixiao')
        if not os.path.exists(roaming_dir):
            os.makedirs(roaming_dir)
        self.app_info = {
            "app_name": f"{self.app_name}{self.app_version}",
            "app_ico": f"{roaming_dir}\\res\\0\\zhuhuixiao.ico",
            "data_dir": roaming_dir,
        }
        self.queue_info = {
            "hostname": "124.71.164.184",
            "port": 5672,
            "username": "iflying",
            "password": "mq_iflying_2019"
        }
        self.has_start_use_path = [roaming_dir, 'assets', 'has_start_use.json']
