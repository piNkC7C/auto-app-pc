import os
import json
import urllib.parse
import sys


def custom_open(file_path, mode='r'):
    return open(file_path, mode, encoding='utf-8')

class File(object):
    def __init__(self):
        pass

    def get_fei_assist_id(self):
        folder_name = os.path.join("FeiAssistData", "LoginList")
        if os.path.exists(folder_name) and os.path.isdir(folder_name):
            # 文件夹已存在，计算子文件个数
            files = [f for f in os.listdir(folder_name) if os.path.isfile(os.path.join(folder_name, f))]
            return f"fei_assist{len(files)}"
        else:
            # 文件夹不存在，创建文件夹并返回 100000000000
            os.makedirs(folder_name)
            return "fei_assist0"

    def check_qr_code_existence(self, fei_id):
        qr_code_path = os.path.join("assets", f"qrCode{fei_id}.png")
        return os.path.exists(qr_code_path)

    def check_login_info(self, ):
        login_info_path = os.path.join("FeiAssistData", "LoginInfo")
        if os.path.exists(login_info_path):
            with custom_open(login_info_path, "r") as f:
                login_info_data = json.load(f)
                userid = login_info_data.get("userid")
                if userid:
                    return True
                return False
        return False

    def update_login_info(self, login_info):
        login_info_path = os.path.join("FeiAssistData", "LoginInfo")
        if os.path.exists(login_info_path):
            with custom_open(login_info_path, "r") as f:
                data = json.load(f)
                data.update(login_info)
            with custom_open(login_info_path, "w") as f:
                json.dump(data, f, ensure_ascii=False)
        else:
            os.makedirs("FeiAssistData", exist_ok=True)
            with custom_open(login_info_path, "w") as f:
                json.dump(login_info, f, ensure_ascii=False)

        # 取出并打印 loginInfo
        with custom_open(login_info_path, "r") as f:
            login_info = json.load(f)
            print("Login Info:", login_info)

    def update_login_list(self, userid, login_info):
        login_list_path = os.path.join("FeiAssistData", "LoginList")
        if not os.path.exists(login_list_path):
            os.makedirs(login_list_path)

        files = os.listdir(login_list_path)
        if len(files) == 0:
            file_path = os.path.join(login_list_path, f"{userid}.json")
            with custom_open(file_path, "w") as f:
                json.dump(login_info, f)
        else:
            if f"{userid}.json" in files:
                return  # 如果文件已存在则退出函数
            else:
                file_path = os.path.join(login_list_path, f"{userid}.json")
                with custom_open(file_path, "w") as f:
                    json.dump(login_info, f)

    def get_login_info(self):
        login_info_path = os.path.join("FeiAssistData", "LoginInfo")
        if os.path.exists(login_info_path):
            with custom_open(login_info_path, "r") as f:
                login_info = json.load(f)
                return login_info
        return None

    def get_file_data(self, path):
        if os.path.exists(path):
            with open(path, "r") as f:
                file_data = json.load(f)
                return file_data
        return None

    def get_current_directory(self):
        # 获取当前可执行文件所在目录
        exe_file = sys.argv[0]
        exe_dir = os.path.dirname(exe_file)
        return exe_dir
