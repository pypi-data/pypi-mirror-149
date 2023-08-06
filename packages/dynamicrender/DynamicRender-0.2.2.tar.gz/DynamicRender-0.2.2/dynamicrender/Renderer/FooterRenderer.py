import configparser
import os
import traceback

import qrcode
from PIL import Image, ImageDraw, ImageFont, ImageFile

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None
from ..Logger import logger


class FooterRender:
    def __init__(self, dynamic_id):
        self.__dynamic_id = dynamic_id
        self.__base_path = os.getcwd()

    async def foot_render(self):
        try:
            conf = configparser.ConfigParser()
            # 读取配置文件
            conf.read(os.path.join(self.__base_path, "config.ini"))
            # 读取主体背景色
            main_color = conf.get("Color", "main_color")
            # 读取主字体
            font_name = conf.get("Font", "main_font")

            container = Image.new("RGBA", (1108, 300), main_color)
            qr_code = await self.__make_qrcode()
            girl = Image.open(os.path.join(self.__base_path, "Static", "Picture", "yyj.png")).convert("RGBA").resize(
                (300, 300))
            bili_pic = Image.open(os.path.join(self.__base_path, "Static", "Picture", "bilibili.png")).convert("RGBA")
            bili_pic = bili_pic.resize((int(bili_pic.size[0] / 4), int(bili_pic.size[1] / 4)))
            # 贴上看板娘
            container.paste(girl, (825, -5), girl)
            # 贴上二维码
            container.paste(qr_code, (905, 160), qr_code)
            # 贴上bili图标
            container.paste(bili_pic, (50, 120), bili_pic)
            # 写入提示扫码语句
            draw = ImageDraw.Draw(container, "RGBA")
            font = ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", font_name), 20, encoding='utf-8')
            draw.text((50, 200), "扫描二维码查看动态", font=font, fill="#ff4e80")
            draw.text((50, 255), "DMC", font=font, fill="#99a2aa")

            return container
        except:
            logger.error("\n" + traceback.format_exc())

    async def __make_qrcode(self):
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_Q, box_size=3, border=1)
        qr.add_data("https://t.bilibili.com/" + str(self.__dynamic_id))
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="#ebceaf").convert("RGBA").rotate(-8, expand=True,
                                                                                             resample=Image.BICUBIC)
        img = img.resize((103, 103))
        return img
