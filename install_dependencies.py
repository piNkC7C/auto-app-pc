import subprocess
from log.log_record import debugLog


def install_dependencies():
    required_libraries = ['pyautogui', 'esdk-obs-python', 'pymysql', 'colorama', 'pymongo', 'moment', 'opencv-python',
                          'cson', 'redis','']  # 将所需的依赖库列在这里

    for library in required_libraries:
        try:
            # 检查依赖库是否已安装
            subprocess.run(['pip', 'install', library], check=True)
        except subprocess.CalledProcessError:
            debugLog(f"Failed to install {library}. Please install it manually.")
