import ctypes
from log.log_record import debugLog


def screen_scale_rate():
    try:
        screen_scale_rate = ctypes.windll.shcore.GetScaleFactorForDevice(0)
    except Exception as e:
        debugLog(f"获取缩放比例报错:{str(e)}")
        screen_scale_rate = 100
    debugLog(f"缩放比例：{screen_scale_rate}")
    return screen_scale_rate
