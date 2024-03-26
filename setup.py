import sys
from cx_Freeze import setup, Executable
from tools.fileOperate import File

file_manager = File()
app_config = file_manager.get_file_data_rb("assets/app.json")
app_name = app_config["app_name"]
app_ico = app_config["app_ico"]

base = "Win32GUI" if sys.platform == "win32" else None

exe = Executable(
    script="app.py",
    base=base,
    icon=app_ico,  # 指定图标文件
    target_name=f"{app_name}.exe"
)

build_exe_options = {
    "include_files": [app_ico, "res/", "assets/", "FeiAssistData/"],  # 包含其他文件
    # "includes": ["your_package_name"]  # 包含其他软件包
    "build_exe": f"build/{app_name}"
}

msi_options = {
    "icon": app_ico  # 指定图标文件
}

setup(
    name=app_name,
    version="1.0",
    description=app_name,
    options={
        "build_exe": build_exe_options,
        "bdist_msi": msi_options
    },
    executables=[exe]
)
