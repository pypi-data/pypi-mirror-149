import configparser
import os
import re
import traceback
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

import emoji
import httpx
from PIL import ImageFont, Image, ImageDraw, ImageFile
from fontTools.ttLib.ttFont import TTFont

from dynamicrender.Logger import logger
from ..DynamicChecker.ModulesChecker import ModuleDynamic

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None


class TextRender:
    def __init__(self, dynamic: ModuleDynamic, forward=False):
        self.forward = forward
        self.container = None
        self.draw = None
        self.client = None
        self.emoji_list = []
        self.font_key = None
        self.dynamic = dynamic
        self.emoji_font = None
        self.standby_font = None
        self.text_font = None
        self.__base_path = os.getcwd()

        # 0 Bv转视频 1 网页链接 2 抽奖 3 恰饭 4 new_topic 5 投票 6 恰饭2.0
        self.rich_text_Instead = ["㉠", "㉡", "㉣", "㉢", "㉤", "㉥", "㉦"]
        self.emoji_pic_tag_instead = ["㉧", "㉨", "㉩", "㉪", "㉫", "㉬", "㉭", "㉮", "㉯", '㉰', "㉱", "㉲", "㉳", "㉴", "㉵", "㉶",
                                      "㉷", "㉸", "㉹", "㉺", "㉻", "㉿", "㋐", "㋑", "㋒", "㋓", "㋔", "㋕", "㋖", "㋗", "㋘", "㋙",
                                      "㋚", "㋛", "㋜", "㋝", "㋞", "㋟", "㋠", "㋡", "㋢", "㋣", "㋤", "㋥", "㋦", "㋧", "㋨", "㋩"]

    async def main_text_render(self):
        """
        动态主体渲染函数
        :return:
        """
        # 读取配置文件
        config = configparser.ConfigParser()
        config.read(os.path.join(self.__base_path, "config.ini"))
        # 读取字体大小
        font_size = config.getint("Size", "main_font_size")
        # 读取字体颜色
        font_color = config.get("Color", "main_font_color")
        # 读取字体名
        font_name = config.get("Font", "main_font")
        # 读取背景色
        if not self.forward:
            text_container_color = config.get("Color", "main_color")
        else:
            text_container_color = config.get("Color", "repost_color")
        # 读取emoji字体大小
        emoji_font_size = config.getint("Size", "emoji_font_size")
        # 读取emoji字体名
        emoji_font_name = config.get("Font", "emoji_font")
        # 读取备用字体名
        standby_font_name = config.get("Font", "standby_font")
        self.text_font = ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", font_name), font_size)
        # 设置备用字体
        self.standby_font = ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", standby_font_name),
                                               font_size)
        # 设置emoji字体
        self.emoji_font = ImageFont.truetype(os.path.join(self.__base_path, "Static", "Font", emoji_font_name),
                                             emoji_font_size)
        self.font_key = \
            TTFont(os.path.join(self.__base_path, "Static", "Font", font_name), fontNumber=0)['cmap'].tables[
                0].ttFont.getBestCmap().keys()
        # 取出内容主题
        desc = self.dynamic.desc
        # 如果内容不为空
        if desc:
            all_emoji = emoji.emoji_lis(desc.text)
            # 如果emoji列表不为空
            if all_emoji:
                # 将所有emoji内容放进列表内
                for i in all_emoji:
                    self.emoji_list.append(i["emoji"])
            result = await self.get_all_rich_text(desc.text, desc.rich_text_nodes)
            description = result["content"]
            rich_text_content = result["rich_text_content"]
            emoji_pics = result["emoji_pics"]
            rich_text_index = await self.calculate_rich_index(description, rich_text_content)
            if not self.forward:
                word_position_list = await self.calculate_text_position(start_x=20, start_y=10, x_constraint=1068,
                                                                        text=description, text_color=font_color,
                                                                        text_size=font_size, img_list=emoji_pics,
                                                                        rich_index=rich_text_index)
            else:
                word_position_list = await self.calculate_text_position(start_x=10, start_y=10, x_constraint=1044,
                                                                        text=description, text_color=font_color,
                                                                        text_size=font_size, img_list=emoji_pics,
                                                                        rich_index=rich_text_index)

            content_y = word_position_list[-1]["position"][1] + 50
            # 创建承载文本主体的图片
            if not self.forward:
                self.container = Image.new("RGBA", (1108, content_y), color=text_container_color)
            else:
                self.container = Image.new("RGBA", (1068, content_y), color=text_container_color)
            self.draw = ImageDraw.Draw(self.container)
            with ThreadPoolExecutor(5) as pool:
                pool.map(self.draw_pic, word_position_list)
            return self.container
        else:
            if self.dynamic.topic:
                result = await self.get_all_rich_text(text="", rich_text_nodes=[])
                description = result["content"]
                rich_text_content = result["rich_text_content"]
                emoji_pics = result["emoji_pics"]
                rich_text_index = await self.calculate_rich_index(description, rich_text_content)
                if not self.forward:
                    word_position_list = await self.calculate_text_position(start_x=20, start_y=10, x_constraint=1068,
                                                                            text=description, text_color=font_color,
                                                                            text_size=font_size, img_list=emoji_pics,
                                                                            rich_index=rich_text_index)
                else:
                    word_position_list = await self.calculate_text_position(start_x=10, start_y=10, x_constraint=1044,
                                                                            text=description, text_color=font_color,
                                                                            text_size=font_size, img_list=emoji_pics,
                                                                            rich_index=rich_text_index)

                content_y = word_position_list[-1]["position"][1] + 50
                # 创建承载文本主体的图片
                if not self.forward:
                    self.container = Image.new("RGBA", (1108, content_y), color=text_container_color)
                else:
                    self.container = Image.new("RGBA", (1068, content_y), color=text_container_color)
                self.draw = ImageDraw.Draw(self.container)
                with ThreadPoolExecutor(5) as pool:
                    pool.map(self.draw_pic, word_position_list)
                return self.container

    async def get_all_rich_text(self, text, rich_text_nodes) -> dict:
        """
        获取所有富文本
        :param text:
        :param rich_text_nodes:
        :return:
        """
        info_list = []
        emoji_list = []
        emoji_info_list = []
        emoji_info = []
        if rich_text_nodes:
            for rich_text in rich_text_nodes:
                if rich_text.type in ["RICH_TEXT_NODE_TYPE_TOPIC", "RICH_TEXT_NODE_TYPE_AT"]:
                    info_list.append(rich_text.text)
                    continue
                if rich_text.type == "RICH_TEXT_NODE_TYPE_BV":
                    new_text = self.rich_text_Instead[0] + rich_text.text
                    text = text.replace("https://b23.tv/" + rich_text.orig_text, new_text)
                    text = text.replace(rich_text.orig_text, new_text)
                    info_list.append(new_text)
                    continue
                if rich_text.type == "RICH_TEXT_NODE_TYPE_WEB":
                    new_text = self.rich_text_Instead[1] + rich_text.text
                    text = text.replace(rich_text.orig_text, new_text)
                    info_list.append(new_text)
                    continue
                if rich_text.type == "RICH_TEXT_NODE_TYPE_LOTTERY":
                    new_text = self.rich_text_Instead[2] + rich_text.text
                    text = text.replace(rich_text.orig_text, new_text)
                    info_list.append(new_text)
                    continue
                if rich_text.type == "RICH_TEXT_NODE_TYPE_GOODS":
                    if rich_text.goods.type == 1:
                        new_text = self.rich_text_Instead[3] + rich_text.text
                    else:
                        new_text = self.rich_text_Instead[1] + rich_text.text
                    text = text.replace(rich_text.orig_text, new_text)
                    info_list.append(new_text)
                    continue
                if rich_text.type == "RICH_TEXT_NODE_TYPE_VOTE":
                    new_text = self.rich_text_Instead[5] + rich_text.text
                    text = text.replace(rich_text.orig_text, new_text)
                    info_list.append(new_text)
                    continue
                if rich_text.type == "RICH_TEXT_NODE_TYPE_EMOJI":
                    emoji_info.append({"name": rich_text.emoji.text, "url": str(rich_text.emoji.icon_url)})
                    continue
        if self.dynamic.topic:
            new_text = self.rich_text_Instead[4] + self.dynamic.topic.name + "\n"
            text = new_text + text
            info_list.append(new_text)
        # 如果有bili_emoji,对其去重并下载
        if emoji_info:
            for i in emoji_info:
                if i not in emoji_info_list:
                    emoji_info_list.append(i)
            for i in range(len(emoji_info_list)):
                text = text.replace(emoji_info_list[i]["name"], self.emoji_pic_tag_instead[i])
            self.client = httpx.Client()
            with ThreadPoolExecutor(max_workers=5) as pool:
                emoji_result = pool.map(self.get_emoji, emoji_info_list)
            for i in emoji_result:
                emoji_list.append(i)
            self.client.close()
        # 去除特殊符号
        text = text.translate(str.maketrans({'\r': '', chr(65039): '', chr(65038): '', chr(8205): ''}))
        # text = text.replace({})   ("\r", "").replace(chr(65039), "").replace(chr(65038), "")
        # 将组合emoji替换成emoji的第一个
        if self.emoji_list:
            temp = []
            for i in self.emoji_list:
                if len(i) != 1:
                    emoji_first = i[0]
                    text = text.replace(i, emoji_first)
                    temp.append(emoji_first)
                    continue
                else:
                    temp.append(i)
                    continue
            self.emoji_list = temp

        return {"content": text, "rich_text_content": info_list, "emoji_pics": emoji_list}

    async def calculate_rich_index(self, text, rich_text_info):
        """
        获取副文本所有文字的索引
        :param text: 源文本
        :param rich_text_info: 副文本列表
        :return:
        """
        particular_text_index_set = ()
        for rich_text_detail in rich_text_info:
            # 加号和括号会影响正则，所以转义掉
            rich_text_detail = rich_text_detail.replace("+", "\+").replace("(", "\(")
            for t in re.finditer(rich_text_detail, text):
                particular_text_index_set = particular_text_index_set + tuple(x for x in range(t.start(), t.end()))
        return set(particular_text_index_set)

    async def calculate_text_position(self, start_x: int, start_y: int, x_constraint: int, text: str,
                                      text_color: str, text_size: int,
                                      img_list: list, rich_index: set) -> list:
        """
        计算文字的位置
        :param start_x: 文字在x方向的起点x坐标
        :param start_y: 文字在y方向的起点y坐标
        :param x_constraint: x方向的约束坐标
        :param text: 文本本体
        :param text_color: 文字颜色
        :param text_size: 文字尺寸
        :param img_list: bili_emoji图片列表
        :param rich_index: 富文本文字的索引
        :return:
        """
        tag_pic_list = {"0": "play.png", "1": "link.png", "2": "lottery.png", "3": "taobao.png", "4": "new_topic.png",
                        "5": "icon_vote.png"}
        y_interval = int(1.5 * text_size)
        position_list = []
        x, y = start_x, start_y
        for i in range(len(text)):
            # 如果是图标
            if text[i] in self.rich_text_Instead:
                # 打开图标图片
                t_content = Image.open(os.path.join(self.__base_path, "Static", "Picture",
                                                    tag_pic_list[str(self.rich_text_Instead.index(text[i]))])).convert(
                    "RGBA").resize((text_size, text_size), Image.ANTIALIAS)
                position_list.append({"info_type": "img", "content": t_content, "position": (x, y + 3)})
                x += text_size + 2
                if x > x_constraint:
                    x = start_x
                    y += y_interval
                continue
            # 如果是bili_emoji
            if text[i] in self.emoji_pic_tag_instead:
                # 如果按照索引取不到图片就把content[i]当作字符
                try:
                    t_content = img_list[self.emoji_pic_tag_instead.index(text[i])].resize(
                        (int(text_size * 1.5), int(text_size * 1.5)),
                        Image.ANTIALIAS)
                    position_list.append({"info_type": "img", "content": t_content, "position": (x, y)})
                    x += t_content.size[0]
                    if x > x_constraint:
                        x = start_x
                        y += y_interval
                    continue
                except:
                    size = self.text_font.getsize(text[i])
                    # 如果是蓝色字体
                    if i in rich_index:
                        position_list.append(
                            {"info_type": "text", "content": text[i], "position": (x, y),
                             "font_color": "#00A0D8",
                             "font_size": text_size})
                    else:
                        position_list.append(
                            {"info_type": "text", "content": text[i], "position": (x, y),
                             "font_color": text_color,
                             "font_size": text_size})
                    if ord(text[i]) not in self.font_key:
                        x += self.standby_font.getsize(text[i])[0]
                    else:
                        x += size[0]
                    if x > x_constraint:
                        x = start_x
                        y += y_interval
                    continue
            # 如果是emoji
            if text[i] in self.emoji_list:
                size = self.emoji_font.getsize(text[i])
                # 新建一个图片来承载emoji
                img = Image.new("RGBA", size)
                draw = ImageDraw.Draw(img)
                # 写入emoji
                draw.text(xy=(0, 0), text=text[i], font=self.emoji_font, embedded_color=True)
                # 把emoji图片缩放到文字字体的大小
                img = img.resize((text_size, text_size), Image.ANTIALIAS)
                # 将文字信息放入字典
                position_list.append({"info_type": "img", "content": img, "position": (x, y + 5)})
                x += text_size
                if x > x_constraint:
                    x = start_x
                    y += y_interval
                continue

            # 如果是换行
            if text[i] == "\n":
                x = start_x
                y += y_interval
                continue
            # 如果是文字
            size = self.text_font.getsize(text[i])
            # 如果是蓝色字体
            if i in rich_index:
                position_list.append(
                    {"info_type": "text", "content": text[i], "position": (x, y), "font_color": "#00A0D8",
                     "font_size": text_size})
            else:
                position_list.append(
                    {"info_type": "text", "content": text[i], "position": (x, y), "font_color": text_color,
                     "font_size": text_size})
            if ord(text[i]) not in self.font_key:
                x += self.standby_font.getsize(text[i])[0]
            else:
                x += size[0]
            if x > x_constraint:
                x = start_x
                y += y_interval
            continue
        return position_list

    def draw_pic(self, info):
        if info["info_type"] == "text":
            if ord(info["content"]) not in self.font_key:
                self.draw.text(info["position"], info["content"], fill=info["font_color"], font=self.standby_font)
            else:
                self.draw.text(info["position"], info["content"], fill=info["font_color"], font=self.text_font)
        elif info["info_type"] == "emoji":

            self.draw.text(xy=info["position"], text=info["content"], font=self.emoji_font, embedded_color=True)
        else:
            self.container.paste(info["content"], info["position"], info["content"])

    def get_emoji(self, emoji_info):
        emoji_name = emoji_info["name"]
        emoji_cache_path = os.path.join(self.__base_path, "Cache", "Emoji", emoji_name + ".png")
        if os.path.exists(emoji_cache_path):
            img = Image.open(emoji_cache_path).convert("RGBA")
        else:
            try:
                response = self.client.get(emoji_info["url"], timeout=800)
            except:
                logger.error(traceback.print_exc())
                response = httpx.get(emoji_info["url"], timeout=800)
            with open(emoji_cache_path, "wb") as f:
                f.write(response.content)
            img = Image.open(BytesIO(response.content)).convert("RGBA")
        return img
