import PyInstaller.__main__

opts = [
    'app.py',  # 设置要打包的脚本文件
    '--onefile',  # 设置为单个文件模式
    '--windowed',  # 设置为无控制台窗口模式
    '--name=朱会潇·销售助理',  # 设置自定义的应用名称
    '--icon=zhuhuixiao.ico',
]

# 调用PyInstaller打包
PyInstaller.__main__.run(opts)
