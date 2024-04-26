import os
import json
import urllib.parse
import sys
import requests

from log.log_record import debugLog


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
            debugLog("Login Info:")
            debugLog(login_info)

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

    def get_file_data_rb(self, path):
        if os.path.exists(path):
            with open(path, 'rb') as f:
                file_data = json.loads(f.read().decode('utf-8'))
                return file_data
        return None

    def get_current_directory(self):
        # 获取当前可执行文件所在目录
        exe_file = sys.argv[0]
        exe_dir = os.path.dirname(exe_file)
        return exe_dir

    def delete_file(self, path_list):
        # 构建文件路径
        file_path = os.path.join(*path_list)
        # 如果文件路径存在，则删除
        if os.path.exists(file_path):
            os.remove(file_path)
            debugLog(f"{file_path}已成功移除")

    def delete_files_with_name(self, directory, name):
        # 遍历目录中的文件
        for filename in os.listdir(directory):
            # 判断文件名是否包含 'qrCode'
            if name in filename:
                # 构建文件的绝对路径
                filepath = os.path.join(directory, filename)
                # 删除文件
                os.remove(filepath)
                debugLog(f"已删除文件: {filepath}")

    def get_json_info_by_folder(self, path_list):
        # 构建文件夹路径
        folder_path = os.path.join(*path_list[:-1])
        # 如果文件夹路径不存在，则创建它
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # 获取 JSON 文件路径
        json_file_path = os.path.join(folder_path, path_list[-1])
        # 如果 JSON 文件不存在，则创建一个空的 JSON 文件
        if not os.path.exists(json_file_path):
            with open(json_file_path, "w") as f:
                json.dump([], f)  # 写入一个空数组到文件中
                return []  # 返回一个空数组作为初始数据
        else:
            with open(json_file_path, "r") as f:
                json_info = json.load(f)
                return json_info

    def check_json_by_folder(self, path_list):
        # 构建文件夹路径
        folder_path = os.path.join(*path_list)
        # 如果文件夹路径不存在
        if not os.path.exists(folder_path):
            return False
        return True

    def write_json_info_by_folder(self, path_list, data_to_write):
        # 构建文件夹路径
        folder_path = os.path.join(*path_list[:-1])
        # 如果文件夹路径不存在，则创建它
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # 获取 JSON 文件路径
        json_file_path = os.path.join(folder_path, path_list[-1])
        with open(json_file_path, "w", encoding="utf-8") as f:  # 设置编码为utf-8
            json.dump(data_to_write, f, ensure_ascii=False)  # 写入数据到文件中，ensure_ascii设置为False
            return data_to_write

    def download_image(self, url, name, path_list):
        # 构建文件夹路径
        folder_path = os.path.join(*path_list[:-1])
        # 如果文件夹路径不存在，则创建它
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        # 构建文件夹路径
        save_path = os.path.join(*path_list)
        try:
            response = requests.get(url)
            if os.path.exists(save_path):
                os.remove(save_path)  # 如果文件已经存在，删除文件
            with open(save_path, 'wb') as f:
                f.write(response.content)
            debugLog(f"{name}已保存到：{save_path}")
        except Exception as e:
            debugLog(f"保存图片时出错：{str(e)}")
