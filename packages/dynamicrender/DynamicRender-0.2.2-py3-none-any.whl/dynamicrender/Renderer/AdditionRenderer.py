import asyncio
import configparser
import os
import traceback
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

import emoji
import httpx
from PIL import ImageFont, Image, ImageDraw, ImageFile
from fontTools.ttLib import TTFont

from dynamicrender.Logger import logger
from ..DynamicChecker.ModulesChecker import ModuleDynamic

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None


class AdditionRender:
    def __init__(self, dynamic: ModuleDynamic, forward=False):
        self.client = None
        self.container = None
        self.current_path = os.getcwd()
        self.content = None
        self.draw = None
        self.standby_font = None
        self.main_font = None
        self.config = None
        self.repost_color = None
        self.main_color = None
        self.emoji_font = None
        self.dynamic = dynamic
        self.forward = forward
        self.addition_type = {"ADDITIONAL_TYPE_RESERVE": self.additional_reserve,
                              "ADDITIONAL_TYPE_GOODS": self.additional_goods,
                              "ADDITIONAL_TYPE_COMMON": self.additional_common,
                              "ADDITIONAL_TYPE_UGC": self.additional_ugc,
                              "ADDITIONAL_TYPE_VOTE": self.additional_vote}

    async def addition_render(self):
        """
        渲染图片
        :return:
        """
        # 读取配置文件
        self.config = configparser.ConfigParser()
        self.config.read(os.path.join(self.current_path, "config.ini"))
        # 读取主背景颜色
        self.main_color = self.config.get("Color", "main_color")
        # 读取forward背景颜色
        self.repost_color = self.config.get("Color", "repost_color")
        # emoji字体名
        emoji_font_name = self.config.get("Font", "emoji_font")
        #  emoji字体尺寸
        emoji_font_size = self.config.getint("Size", "emoji_font_size")
        # emoji字体
        self.emoji_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", emoji_font_name),
                                             emoji_font_size)
        try:
            addition_img = await self.addition_type[self.dynamic.additional.type]()
            return addition_img
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def additional_reserve(self):
        """预约类型ADDITIONAL"""

        title = self.dynamic.additional.reserve.title
        desc_first = self.dynamic.additional.reserve.desc1.text
        desc_second = self.dynamic.additional.reserve.desc2.text
        badge_text = self.dynamic.additional.reserve.button.check.text if self.dynamic.additional.reserve.button.status == 2 else self.dynamic.additional.reserve.button.uncheck.text
        # 读取字体配置
        # 主字体名
        main_font_name = self.config.get("Font", "main_font")
        # 备用字体名
        standby_font_name = self.config.get("Font", "standby_font")

        # 主字体颜色
        main_font_color = self.config.get("Color", "main_font_color")
        # 副标题字体颜色
        sub_font_color = self.config.get("Color", "sub_font_color")
        # 读取主字体尺寸
        main_font_size = self.config.getint("Size", "main_font_size")
        # 副标题字体尺寸
        sub_font_size = self.config.getint("Size", "sub_font_size")

        self.main_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                            main_font_size)
        self.standby_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", standby_font_name),
                                               main_font_size)

        if not self.forward:
            self.content = Image.new("RGBA", (1040, 116), self.repost_color)
        else:
            self.content = Image.new("RGBA", (1040, 116), self.main_color)
        self.draw = ImageDraw.Draw(self.content)
        title_emoji_info = emoji.emoji_lis(title)
        title_emoji_list = []
        if title_emoji_info:
            # 将所有emoji内容放进列表内
            for i in title_emoji_info:
                title_emoji_list.append(i["emoji"])
            temp = []
            for i in title_emoji_list:
                if len(i) != 1:
                    emoji_first = i[0]
                    title = title.replace(i, emoji_first)
                    temp.append(emoji_first)
                    continue
                else:
                    temp.append(i)
                    continue
            title_emoji_list = temp

        position_info = await self.calculate_position(start_x=24, start_y=20, x_constraint=850, y_constraint=50,
                                                      text_size=main_font_size, text=title,
                                                      main_font_name=main_font_name,
                                                      standby_font_name=standby_font_name,
                                                      font_color=main_font_color,
                                                      emoji_list=title_emoji_list)
        task_list = []
        for i in position_info:
            task_list.append(self.draw_pic(i))
        await asyncio.gather(*task_list)
        button = Image.new("RGBA", (128, 56), "#00a0d8")
        draw = ImageDraw.Draw(button)
        size = self.main_font.getsize(badge_text)
        draw.text((int((button.size[0] - size[0]) / 2), int((button.size[1] - size[1]) / 2)), text=badge_text,
                  size=main_font_size, fill=(255, 255, 255, 255), font=self.main_font)
        sub_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name), sub_font_size)
        self.draw.text((24, 72), desc_first + "   " + desc_second, fill=sub_font_color, font=sub_font)
        self.content.paste(button, (888, int((self.content.size[1] - 56) / 2)), button)
        return self.content

    async def additional_goods(self):
        """GOODS类型ADDITIONAL"""
        # 读取配置
        main_font_color = self.config.get("Color", "main_font_color")
        extra_color = self.config.get("Color", "extra_color")
        main_font_name = self.config.get("Font", "main_font")
        standby_font_name = self.config.get("Font", "standby_font")
        main_font_size = self.config.getint("Size", "main_font_size")
        sub_font_size = self.config.getint("Size", "sub_font_size")
        items = self.dynamic.additional.goods.items
        head_text = self.dynamic.additional.goods.head_text
        if self.forward:
            self.content = Image.new("RGBA", (1040, 160), self.main_color)
            self.container = Image.new("RGBA", (1040, 196), self.repost_color)
        else:
            self.content = Image.new("RGBA", (1040, 160), self.repost_color)
            self.container = Image.new("RGBA", (1040, 196), self.main_color)
        container_draw = ImageDraw.Draw(self.container)
        container_draw.text(xy=(5, 5), text=head_text, fill=extra_color,
                            font=ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                                    size=int(sub_font_size * 0.8)))
        tasks = []
        self.client = httpx.Client()
        for item in items:
            tasks.append(item.cover + "@128w_128h_1c.webp")
        with ThreadPoolExecutor(max_workers=5) as pool:
            result = pool.map(self.get_img, tasks)
        result = list(result)
        self.client.close()
        if len(result) > 1:
            for index in range(len(result)):
                self.content.paste(result[index].resize((128, 128), Image.ANTIALIAS), ((index * 138) + 24, 16))
            self.container.paste(self.content, (0, 36))
        else:
            self.content.paste(result[0], (24, 16))
            title_position = await self.calculate_position(start_x=176, start_y=22, x_constraint=864, y_constraint=26,
                                                           text_size=main_font_size, text=items[0].name, emoji_list=[],
                                                           main_font_name=main_font_name,
                                                           standby_font_name=standby_font_name,
                                                           font_color=main_font_color)

            self.draw = ImageDraw.Draw(self.content)
            self.main_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                                main_font_size)
            self.standby_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", standby_font_name),
                                                   main_font_size)
            sub_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                          sub_font_size)
            tasks = []
            for i in title_position:
                tasks.append(self.draw_pic(i))
            await asyncio.gather(*tasks)
            price = items[0].price + "起"
            self.draw.text((176, 100), text=price, fill=extra_color, font=sub_font)
            button = Image.new("RGBA", (128, 56), "#00a0d8")
            draw = ImageDraw.Draw(button)
            desc = self.dynamic.additional.goods.items[0].jump_desc
            size = self.main_font.getsize(desc)
            draw.text((int((button.size[0] - size[0]) / 2), int((button.size[1] - size[1]) / 2)), text=desc,
                      size=main_font_size, fill=(255, 255, 255, 0), font=self.main_font)
            self.content.paste(button, (888, int((self.content.size[1] - 64) / 2)), button)
            self.container.paste(self.content, (0, 36))
        return self.container

    async def additional_common(self):
        """COMMON类型ADDITIONAL"""
        # 读取配置
        main_font_color = self.config.get("Color", "main_font_color")
        extra_color = self.config.get("Color", "extra_color")
        main_font_name = self.config.get("Font", "main_font")
        main_font_size = self.config.getint("Size", "main_font_size")
        sub_font_size = self.config.getint("Size", "sub_font_size")
        sub_font_color = self.config.get("Color", "sub_font_color")

        head_text = self.dynamic.additional.common.head_text
        title = self.dynamic.additional.common.title
        desc_first = self.dynamic.additional.common.desc1
        desc_second = self.dynamic.additional.common.desc2

        self.client = httpx.Client()
        if self.dynamic.additional.common.sub_type in ["pugv", "manga", "ogv"]:
            cover = self.dynamic.additional.common.cover + "@96w_128h_1c.webp"
            cover_image = self.get_img(cover).resize((96, 128)).convert("RGBA")
        else:
            cover = self.dynamic.additional.common.cover + "@128w_128h_1c.webp"
            cover_image = self.get_img(cover).resize((128, 128)).convert("RGBA")
        btn = self.dynamic.additional.common.button
        button_text = btn.jump_style.text if btn.type == 1 else btn.check.text

        if self.forward:
            self.content = Image.new("RGBA", (1040, 160), self.main_color)
            self.container = Image.new("RGBA", (1040, 196), self.repost_color)
        else:
            self.content = Image.new("RGBA", (1040, 160), self.repost_color)
            self.container = Image.new("RGBA", (1040, 196), self.main_color)

        self.content.paste(cover_image, (24, 16), cover_image)
        # 写入标题
        main_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                       main_font_size)
        content_draw = ImageDraw.Draw(self.content)
        content_draw.text(xy=(176, 16), text=title, fill=main_font_color, font=main_font)
        # 写入副标题
        sub_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                      sub_font_size)
        content_draw.text((176, 66), text=desc_first, fill=sub_font_color, font=sub_font)
        content_draw.text((176, 106), text=desc_second, fill=sub_font_color, font=sub_font)
        # 制作button
        button = Image.new("RGBA", (128, 56), "#00a0d8")
        draw = ImageDraw.Draw(button)
        size = sub_font.getsize(button_text)
        draw.text((int((128 - size[0]) / 2), int((56 - size[1]) / 2) - 5), text=button_text,
                  size=sub_font_size, fill=(255, 255, 255, 255), font=sub_font)
        self.content.paste(button, (888, int((self.content.size[1] - 64) / 2)))
        # 写入head_text
        container_draw = ImageDraw.Draw(self.container)
        container_draw.text(xy=(5, 5), text=head_text, fill=extra_color, font=sub_font)
        self.container.paste(self.content, (0, 36))

        return self.container

    async def additional_ugc(self):
        """UGC类型ADDITIONAL"""
        # 读取配置
        main_font_color = self.config.get("Color", "main_font_color")
        main_font_name = self.config.get("Font", "main_font")
        main_font_size = self.config.getint("Size", "main_font_size")
        sub_font_size = self.config.getint("Size", "sub_font_size")
        sub_font_color = self.config.get("Color", "sub_font_color")
        # 获取ugc信息
        cover = self.dynamic.additional.ugc.cover + "@228w_128h_1c.webp"
        title = self.dynamic.additional.ugc.title
        duration = self.dynamic.additional.ugc.duration
        desc_second = self.dynamic.additional.ugc.desc_second
        # 制作addition载体
        if self.forward:
            self.content = Image.new("RGBA", (1040, 160), self.main_color)
        else:
            self.content = Image.new("RGBA", (1040, 160), self.repost_color)
        # 制作时长载体
        duration_container = Image.new("RGBA", (68, 32), (0, 0, 0, 180))
        draw = ImageDraw.Draw(duration_container)
        # 制作字体
        sub_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name), sub_font_size)
        size = sub_font.getsize(duration)
        self.client = httpx.Client()
        draw.text(xy=(int((68 - size[0]) / 2), int((32 - size[1]) / 2) - 5), text=duration, fill="#ffffff",
                  font=sub_font)
        cover_img = self.get_img(cover)
        tasks = [self.calculate_position(start_x=276, start_y=16, x_constraint=1020,
                                         y_constraint=16 + 1.5 * main_font_size,
                                         text_size=main_font_size, text=title, emoji_list=[],
                                         main_font_name=main_font_name,
                                         standby_font_name=main_font_name,
                                         font_color=main_font_color)]
        result = await asyncio.gather(*tasks)
        self.draw = ImageDraw.Draw(self.content)
        self.content.paste(cover_img, (24, 16))
        self.content.paste(duration_container, (174, 102), duration_container)
        self.main_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                            size=main_font_size)
        self.standby_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                               size=main_font_size)
        self.draw.text(xy=(276, 106), text=desc_second, fill=sub_font_color, font=sub_font)
        task_list = []
        for i in result[0]:
            task_list.append(self.draw_pic(i))
        await asyncio.gather(*task_list)
        return self.content

    async def additional_vote(self):
        """VOTE类型ADDITIONAL"""
        # 读取配置
        main_font_color = self.config.get("Color", "main_font_color")
        main_font_name = self.config.get("Font", "main_font")
        main_font_size = self.config.getint("Size", "main_font_size")
        sub_font_size = self.config.getint("Size", "sub_font_size")
        sub_font_color = self.config.get("Color", "sub_font_color")
        # 获取投票信息
        desc = self.dynamic.additional.vote.desc
        join_num = str(self.dynamic.additional.vote.join_num) + "人参与"
        # 载体
        if self.forward:
            self.content = Image.new("RGBA", (1036, 156), self.main_color)
        else:
            self.content = Image.new("RGBA", (1036, 156), self.repost_color)
        vot_cover = Image.open(os.path.join(self.current_path, "Static", "Picture", "vote_icon.png")).resize(
            (156, 156)).convert("RGBA")
        main_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                       main_font_size)
        sub_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                      sub_font_size)
        draw = ImageDraw.Draw(self.content)
        draw.text(xy=(186, 30), text=desc, font=main_font, fill=main_font_color)
        draw.text(xy=(186, 80), text=join_num, font=sub_font, fill=sub_font_color)

        button = Image.new("RGBA", (128, 56), "#00a0d8")
        draw = ImageDraw.Draw(button)
        size = sub_font.getsize("投票")
        draw.text((int((128 - size[0]) / 2), int((56 - size[1]) / 2) - 5), text="投票",
                  size=sub_font_size, fill=(255, 255, 255, 0), font=sub_font)
        self.content.paste(button, (888, int((self.content.size[1] - 64) / 2)))
        self.content.paste(vot_cover, (0, 0))
        return self.content

    async def calculate_position(self, start_x, start_y, x_constraint, y_constraint, text_size, text,
                                 emoji_list=None, main_font_name=None, standby_font_name=None, font_color=None) -> list:
        """
        计算字的位置
        :param font_color: 字体颜色
        :param start_x: 文字x方向起始位置
        :param start_y: 文字y方向起始位置
        :param x_constraint: x方向约束
        :param y_constraint: y方向约束
        :param text: 文字主体
        :param text_size:文字尺寸
        :param emoji_list: emoji列表
        :param main_font_name: 主字体名称
        :param standby_font_name: 副字体名称
        :return:
        """
        x, y = start_x, start_y
        y_interval = int(1.5 * text_size)
        position_info = []
        main_font_path = os.path.join(os.getcwd(), "Static", "Font", main_font_name)
        standby_font_path = os.path.join(os.getcwd(), "Static", "Font", standby_font_name)
        main_font = ImageFont.truetype(main_font_path, size=text_size)
        standby_font = ImageFont.truetype(standby_font_path, size=text_size)
        font_key = TTFont(main_font_path, fontNumber=0)['cmap'].tables[0].ttFont.getBestCmap().keys()
        for i in text:
            if i in emoji_list:
                size = self.emoji_font.getsize(i)
                img = Image.new("RGBA", size)
                draw = ImageDraw.Draw(img)
                draw.text(xy=(0, 0), text=i, font=self.emoji_font, embedded_color=True)
                # 把emoji图片缩放到文字字体的大小
                img = img.resize((text_size, text_size), Image.ANTIALIAS)
                position_info.append({"info_type": "img", "content": img, "position": (x, y + 5)})
                x += text_size
                if x > x_constraint:
                    x = start_x
                    y += y_interval
                    if y > y_constraint:
                        position_info[-1]["info_type"] = "text"
                        position_info[-1]["content"] = ""
                        position_info[-2]["info_type"] = "text"
                        position_info[-2]["content"] = "..."
                        break
                continue
            if i == "\n":
                x = start_x
                y += y_interval
                if y > y_constraint:
                    position_info[-1]["info_type"] = "text"
                    position_info[-1]["content"] = ""
                    position_info[-2]["info_type"] = "text"
                    position_info[-2]["content"] = "..."
                    break
                continue
            if ord(i) in font_key:

                position_info.append(
                    {"info_type": "text", "content": i, "font": "main", "position": (x, y), "color": font_color})
                x_interval = main_font.getsize(i)[0]
                x += x_interval
                if x > x_constraint:
                    x = start_x
                    y += y_interval
                    if y > y_constraint:
                        position_info[-1]["info_type"] = "text"
                        position_info[-1]["content"] = ""
                        position_info[-2]["info_type"] = "text"
                        position_info[-2]["content"] = "..."
                        break
                continue
            else:
                position_info.append(
                    {"info_type": "text", "content": i, "font": "standby", "position": (x, y), "color": font_color})
                x_interval = standby_font.getsize(i)[0]
                x += x_interval
                if x > x_constraint:
                    x = start_x
                    y += y_interval
                if y > y_constraint:
                    position_info[-1]["info_type"] = "text"
                    position_info[-1]["content"] = ""
                    position_info[-2]["info_type"] = "text"
                    position_info[-2]["content"] = "..."
                    break
                continue
        return position_info

    async def draw_pic(self, word_info):
        font = {"standby": self.standby_font, "main": self.main_font}
        if word_info["info_type"] == "text":
            self.draw.text(xy=word_info["position"], text=word_info["content"], fill=word_info["color"],
                           font=font[word_info["font"]])
        else:
            self.content.paste(word_info["content"], word_info["position"], word_info["content"])

    def get_img(self, url):
        response = self.client.get(url)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        return img
