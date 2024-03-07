import sys
from cx_Freeze import setup, Executable

base = "Win32GUI" if sys.platform == "win32" else None

exe = Executable(
    script="app.py",
    base=base,
    icon="iflying.ico",  # 指定图标文件
    target_name="小飞助理.exe"
)

build_exe_options = {
    "include_files": ["iflying.ico", "res/", "assets/", "FeiAssistData/"],  # 包含其他文件
    # "includes": ["your_package_name"]  # 包含其他软件包
}

msi_options = {
    "icon": "iflying.ico"  # 指定图标文件
}

setup(
    name="小飞助理",
    version="1.0",
    description="My GUI application!",
    options={
        "build_exe": build_exe_options,
        "bdist_msi": msi_options
    },
    executables=[exe]
)
