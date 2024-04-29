import os
import winreg
import os
from log.log_record import debugLog


def add_to_startup(app_name):
    is_add = False
    exe_path = os.path.abspath(os.path.join(f"{app_name}.exe"))
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    try:
        # 检查是否已存在相同的自启动项
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_READ) as reg_key:
            try:
                existing_value, _ = winreg.QueryValueEx(reg_key, app_name)
                if existing_value == exe_path:
                    debugLog("自启动项已存在，无需再次添加。")
                    is_add = True
                    return is_add
            except FileNotFoundError:
                pass  # 如果键值不存在，则继续执行添加操作
            except Exception as e:
                debugLog(f"检测是否存在自启动项时发生错误：{e}")
                is_add = False
                return is_add

        # 如果不存在相同的自启动项，则进行添加
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_ALL_ACCESS) as reg_key:
            winreg.SetValueEx(reg_key, app_name, 0, winreg.REG_SZ, exe_path)
        debugLog("自启动项添加成功。")
        is_add = True
    except Exception as e:
        debugLog(f"添加自启动项时发生错误：{e}")
        is_add = False
    return is_add


def remove_from_startup(app_name):
    is_deleted = False
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    try:
        with winreg.OpenKey(key, key_path, 0, winreg.KEY_ALL_ACCESS) as reg_key:
            winreg.DeleteValue(reg_key, app_name)
            debugLog("自启动项删除成功。")
            is_deleted = True
    except FileNotFoundError:
        debugLog("自启动项不存在，无需删除。")
        is_deleted = True
    except Exception as e:
        debugLog(f"删除自启动项时发生错误：{e}")
        is_deleted = False
    return is_deleted


def check_to_startup(app_name):
    exe_path = os.path.abspath(os.path.join(f"{app_name}.exe"))
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"

    # 检查是否已存在相同的自启动项
    with winreg.OpenKey(key, key_path, 0, winreg.KEY_READ) as reg_key:
        try:
            existing_value, _ = winreg.QueryValueEx(reg_key, app_name)
            if existing_value == exe_path:
                return True
        except FileNotFoundError:
            pass  # 如果键值不存在，则继续执行添加操作

    return False


def get_to_startup(app_name):
    key = winreg.HKEY_CURRENT_USER
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    # 检查是否已存在相同的自启动项
    with winreg.OpenKey(key, key_path, 0, winreg.KEY_READ) as reg_key:
        try:
            existing_value, _ = winreg.QueryValueEx(reg_key, app_name)
            return existing_value
        except FileNotFoundError:
            return False

