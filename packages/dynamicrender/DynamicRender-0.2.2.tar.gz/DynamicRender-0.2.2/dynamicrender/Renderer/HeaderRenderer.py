import asyncio
import configparser
import os
import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

import httpx
from PIL import Image, ImageDraw, ImageFont, ImageFile

from dynamicrender.DynamicChecker.ModulesChecker import ModuleAuthor
from dynamicrender.Logger import logger

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None


class HeaderRender:
    def __init__(self, author: ModuleAuthor, forward=False):
        self.__container = None
        self.__draw = None
        self.__forward = forward
        self.__author = author
        self.__current_path = os.getcwd()
        self.__font_path = os.path.join(self.__current_path, "Static", "Font")
        self.__session = None

    async def main_header_render(self):
        """
        渲染主动态的头
        :return:
        """
        try:
            # 获取程序当前运行路径
            config = configparser.ConfigParser()
            # 读取配置文件
            config.read(os.path.join(self.__current_path, "config.ini"))
            # 读取主背景颜色
            main_color = config.get("Color", "main_color")
            # 读取主字体
            main_font_name = config.get("Font", "main_font")
            # 读取昵称的字号
            uname_size = config.getint("Size", "uname_font_size")
            # 读取昵称颜色
            uname_color = config.get("Color", "main_font_color")
            # 读取时间的字号
            time_size = config.getint("Size", "sub_font_size")
            # 读取时间的颜色
            time_color = config.get("Color", "sub_font_color")
            # 格式化时间戳
            time_formate = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(self.__author.pub_ts))

            try:
                name_color = uname_color if not self.__author.vip.nickname_color else self.__author.vip.nickname_color
            except:
                name_color = uname_color

            # 将昵称和时间信息加入渲染信息列表
            render_info_list = [{"type": "text",
                                 "font_color": name_color,
                                 "font_size": uname_size,
                                 "content": self.__author.name,
                                 "font": main_font_name,
                                 "position": (164, 180)}, {"type": "text", "font_color": time_color,
                                                           "font": main_font_name,
                                                           "font_size": time_size,
                                                           "content": time_formate, "position": (164, 240)}]
            # 将头像链接放入链接列表内
            url_list = [{"type": "face", "url": self.__author.face + "@240w_240h_1c_1s.webp",
                         "path": os.path.join(self.__current_path, "Cache", "Face", str(self.__author.mid) + ".webp")}]
            # 将挂件信息放入请求列表中
            if self.__author.pendant and self.__author.pendant.image:
                url_list.append({"type": "pendant", "url": self.__author.pendant.image,
                                 "path": os.path.join(self.__current_path, "Cache", "Pendant",
                                                      self.__author.pendant.name + ".png")})
            # 将bili图标添加到渲染信息列表内
            bili_pic = Image.open(os.path.join(self.__current_path, "Static", "Picture", "bilibili.png")).convert(
                "RGBA").resize((154, 70))
            render_info_list.append({"type": "img", "content": bili_pic, "position": (477, 50)})
            # 获取头像和pendant
            self.__session = httpx.Client()
            with ThreadPoolExecutor(max_workers=2) as pool:
                results = pool.map(self.__get_images, url_list)
            for result in results:
                render_info_list.append(result)
            self.__session.close()
            # 如果有官方认证的话
            if self.__author.official_verify and self.__author.official_verify.type != -1:
                official_verify_path = [os.path.join(self.__current_path, "Static", "Picture", "official_yellow.png"),
                                        os.path.join(self.__current_path, "Static", "Picture", "official_blue.png")]
                img = Image.open(official_verify_path[self.__author.official_verify.type]).resize((32, 32))
                render_info_list.append({"type": "img", "content": img, "position": (100, 240)})
            # 没有官方认证则查看是否有大会员
            else:
                if self.__author.vip:
                    avatar_subscript = self.__author.vip.avatar_subscript
                    if avatar_subscript and avatar_subscript != 0:
                        avatar_path = {"2": os.path.join(self.__current_path, "Static", "Picture", "small_vip.png"),
                                       "1": os.path.join(self.__current_path, "Static", "Picture", "big_vip.png")}[
                            str(avatar_subscript)]
                        avatar_img = Image.open(avatar_path).resize((32, 32)).convert("RGBA")
                        render_info_list.append({"type": "img", "content": avatar_img, "position": (100, 240)})
            # 组装动态头
            self.__container = Image.new("RGBA", (1108, 330), main_color)
            self.__draw = ImageDraw.Draw(self.__container)
            tasks = []
            for i in render_info_list:
                tasks.append(self.__assembly_header(i))
            await asyncio.gather(*tasks)
            return self.__container

        except:
            logger.error("\n" + traceback.format_exc())

    async def origin_header_render(self):
        try:
            # 获取程序当前运行路径
            config = configparser.ConfigParser()
            # 读取配置文件
            config.read(os.path.join(self.__current_path, "config.ini"))
            # 读取背景颜色
            repost_color = config.get("Color", "repost_color")
            # 读取字体
            main_font_name = config.get("Font", "main_font")
            # 读取昵称的字号
            uname_size = config.getint("Size", "main_font_size")
            # 读取昵称颜色
            uname_color = config.get("Color", "extra_color")

            # 获取昵称及头像
            render_info_list = [{"type": "text",
                                 "font_color": uname_color,
                                 "font_size": uname_size,
                                 "content": self.__author.name,
                                 "font": main_font_name,
                                 "position": (80, 15)}]
            url_list = [{"type": "face", "url": self.__author.face + "@240w_240h_1c_1s.webp",
                         "path": os.path.join(self.__current_path, "Cache", "Face", str(self.__author.mid) + ".webp")}]
            # 获取头像和pendant
            self.__session = httpx.Client()
            with ThreadPoolExecutor(max_workers=2) as pool:
                results = pool.map(self.__get_images, url_list)
            for result in results:
                render_info_list.append(result)
            self.__session.close()
            self.__container = Image.new("RGBA", (1088, 70), repost_color)
            self.__draw = ImageDraw.Draw(self.__container)
            tasks = []
            for i in render_info_list:
                tasks.append(self.__assembly_header(i))
            await asyncio.gather(*tasks)
            return self.__container
        except:
            logger.error("\n" + traceback.format_exc())

    def __get_images(self, img_info):
        if img_info["type"] == "face":
            face_path = img_info["path"]
            # 查看是否有缓存
            if os.path.exists(face_path):
                # 查看修改时间是否大于24小时
                if time.time() - int(os.path.getmtime(face_path)) > 86400:
                    # 重新请求图片
                    response = self.__session.get(img_info["url"])
                    img_content = response.content
                    with open(face_path, "wb") as f:
                        f.write(img_content)
                    img = Image.open(BytesIO(img_content)).convert("RGBA")
                # 如果修改时间和现在相差小于24小时直接读取
                else:
                    img = Image.open(face_path)
            # 没有缓存过头像则直接请求
            else:
                response = self.__session.get(img_info["url"])
                img_content = response.content
                with open(face_path, "wb") as f:
                    f.write(img_content)
                img = Image.open(BytesIO(img_content)).convert("RGBA")
            img = self.__make_face_circle(img)
            if not self.__forward:
                info = {"type": "img", "content": img, "position": (32, 172)}
            else:
                info = {"type": "img", "content": img.resize((48, 48), Image.ANTIALIAS), "position": (15, 10)}
        else:
            pendant_path = img_info["path"]
            if os.path.exists(pendant_path):
                img = Image.open(pendant_path).convert("RGBA").resize((164, 164))
            else:
                response = self.__session.get(img_info["url"])
                with open(pendant_path, "wb") as f:
                    f.write(response.content)
                img = Image.open(BytesIO(response.content)).convert("RGBA").resize((164, 164))
            info = {"type": "img", "content": img, "position": (0, 140)}
        return info

    def __make_face_circle(self, avatar):
        """
        将头像裁剪成圆形
        :param avatar: 头像
        :return:处理好的头像
        """
        # 背景尺寸
        if avatar.size != (240, 240):
            avatar = avatar.resize((240, 240))
        bg_size = (240, 240)
        bg = Image.new('RGBA', bg_size, color=(255, 255, 255, 0))
        # 头像尺寸
        avatar_size = avatar.size
        avatar_draw = ImageDraw.Draw(avatar)
        avatar_draw.ellipse(((0, 0), (240, 240)), fill=None, outline=(251, 114, 153), width=5)
        # 头像路径
        # 新建一个蒙板图
        mask = Image.new('RGBA', avatar_size, color=(0, 0, 0, 0))
        # 画一个圆
        mask_draw = ImageDraw.Draw(mask)

        mask_draw.ellipse((0, 0, avatar_size[0], avatar_size[1]), fill=(0, 0, 0, 255))
        box = (0, 0, 240, 240)
        # 以下使用到paste(img, box=None, mask=None)方法
        #   img 为要粘贴的图片对你
        #   box 为图片 头像在 bg 中的位置
        #   mask 为蒙板，原理同 ps， 只显示 mask 中 Alpha 通道值大于等于1的部分
        bg.paste(avatar, box, mask)
        bg = bg.resize((96, 96), Image.ANTIALIAS)
        # bg_draw = ImageDraw.Draw(bg)
        return bg

    async def __assembly_header(self, document_info: dict) -> None:
        if document_info["type"] == "text":
            font = ImageFont.truetype(os.path.join(self.__font_path, document_info["font"]), document_info["font_size"],
                                      encoding='utf-8')
            self.__draw.text(xy=document_info["position"], text=document_info["content"], font=font,
                             fill=document_info["font_color"])
        else:
            img = document_info["content"]
            self.__container.paste(img, document_info["position"], img)
