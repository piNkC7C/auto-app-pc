import qrcode
import os
import pathlib
import sys

from .fileOperate import File


class QRCodeGenerator:
    def __init__(self, link, fei_id):
        self.link = link
        self.fei_id = fei_id
        # self.file_manager = File()

    def generate_qr_code(self):
        # 获取当前执行文件的目录
        file_path = os.path.join("assets", f"qrCode{self.fei_id}.png")
        print(file_path)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.link)
        qr.make(fit=True)

        # 创建二维码图像
        qr_image = qr.make_image(fill_color="black", back_color="white")

        # 保存二维码图像
        qr_image.save(file_path)
