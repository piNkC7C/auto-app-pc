import urllib
import urllib.request
import os
import sys
import shutil
from api.miniwechatApi import miniwechat_get_feiassistversion
import asyncio
from log.log_record import debugLog

# 更新服务器 URL
UPDATE_SERVER_URL = "https://shining-under-camera.obs.cn-east-3.myhuaweicloud.com/download/"


def check_for_updates(version):
    is_updating = asyncio.run(miniwechat_get_feiassistversion(version))
    debugLog(f"is_updating：{is_updating}")
    if is_updating['code'] == 0:
        return is_updating
    return False


def download_update(app_name, update_name):
    try:
        # # 创建备用目录
        # if not os.path.exists(temp_dir):
        #     os.makedirs(temp_dir)
        # 字符串转码
        encoded_app_name = urllib.parse.quote(app_name)
        # 下载最新版本
        with urllib.request.urlopen(UPDATE_SERVER_URL + f"{encoded_app_name}.exe") as newApp, open(
                f"{app_name}_new.exe",
                "wb") as out_file:
            newAppData = newApp.read()
            out_file.write(newAppData)
        return True
    except Exception as e:
        debugLog(f"Failed to download update:{str(e)}")
        return False
