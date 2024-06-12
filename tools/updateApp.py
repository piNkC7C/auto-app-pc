import urllib
import urllib.request
import os
import sys
import shutil
import time
from api.miniwechatApi import miniwechat_get_feiassistversion
import asyncio
import subprocess
from log.log_record import debugLog

# 更新服务器 URL
UPDATE_SERVER_URL = "https://shining-under-camera.obs.cn-east-3.myhuaweicloud.com/download/company/"


def check_for_updates(version):
    is_updating = asyncio.run(miniwechat_get_feiassistversion(version))
    # debugLog(f"is_updating：{is_updating}")
    return is_updating


def download_update(app_name):
    try:
        # # 创建备用目录
        # if not os.path.exists(temp_dir):
        #     os.makedirs(temp_dir)
        # 字符串转码
        encoded_app_name = urllib.parse.quote(app_name)
        url = UPDATE_SERVER_URL + f"{encoded_app_name}.exe"
        debugLog(url)
        # 下载最新版本
        with urllib.request.urlopen(url) as newApp, open(
                f"{app_name}_new.exe",
                "wb") as out_file:
            newAppData = newApp.read()
            out_file.write(newAppData)
        return True
    except Exception as e:
        debugLog(f"Failed to download update:{str(e)}")
        return False


def download_update_exe(update_name):
    try:
        # # 创建备用目录
        # if not os.path.exists(temp_dir):
        #     os.makedirs(temp_dir)
        # 字符串转码
        encoded_update_name = urllib.parse.quote(update_name)
        url = UPDATE_SERVER_URL + f"{encoded_update_name}.exe"
        debugLog(url)
        # 下载最新版本
        with urllib.request.urlopen(url) as newApp, open(
                f"{update_name}_new.exe",
                "wb") as out_file:
            newAppData = newApp.read()
            out_file.write(newAppData)

        time.sleep(0.5)

        result = subprocess.run(["taskkill", "/f", "/im", "{}.exe".format(update_name)], capture_output=True, text=True)
        debugLog("结束进程结果")
        debugLog(result)
        time.sleep(5)
        if result.returncode == 0 or result.returncode == 128:
            # 替换当前版本
            debugLog("替换更新程序")
            os.replace(f"{update_name}_new.exe", f"{update_name}.exe")
        time.sleep(0.5)
        return True
    except Exception as e:
        debugLog(f"Failed to download update:{str(e)}")
        return False
