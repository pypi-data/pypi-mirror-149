import asyncio
import configparser
import math
import os
import traceback
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO

import emoji
import httpx
from PIL import ImageFont, Image, ImageDraw, ImageFile
from fontTools.ttLib import TTFont

from dynamicrender.DynamicChecker.ModulesChecker import Major
from dynamicrender.Logger import logger

ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None


class MajorRender:
    def __init__(self, major: Major, forward=False):
        self.draw = None
        self.content = None
        self.main_font = None
        self.standby_font = None
        self.emoji_font = None
        self.repost_color = None
        self.main_color = None
        self.config = None
        self.major = major
        self.forward = forward
        self.current_path = os.getcwd()
        self.major_type = {"MAJOR_TYPE_LIVE": self.__major_type_live,
                           "MAJOR_TYPE_MEDIALIST": self.__major_type_medialist,
                           "MAJOR_TYPE_NONE": self.__major_type_none,
                           "MAJOR_TYPE_PGC": self.__major_type_pgc,
                           "MAJOR_TYPE_COMMON": self.__major_type_common,
                           "MAJOR_TYPE_MUSIC": self.__major_type_music,
                           "MAJOR_TYPE_ARTICLE": self.__major_type_article,
                           "MAJOR_TYPE_DRAW": self.__major_type_draw,
                           "MAJOR_TYPE_LIVE_RCMD": self.__major_type_live_rcmd,
                           "MAJOR_TYPE_ARCHIVE": self.__major_type_archive,
                           "MAJOR_TYPE_COURSES": self.__major_courses}

    async def major_render(self):
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
            img = await self.major_type[self.major.type]()
            return img
        except:
            logger.error("\n" + traceback.format_exc())

    async def __major_type_live(self):
        """直播类型"""
        """分享直播"""
        self.client = httpx.Client()
        # 读取配置
        main_font_color = self.config.get("Color", "main_font_color")
        main_font_name = self.config.get("Font", "main_font")
        main_font_size = self.config.getint("Size", "main_font_size")
        sub_font_size = self.config.getint("Size", "sub_font_size")
        sub_font_color = self.config.get("Color", "sub_font_color")
        # 读取major信息
        title = self.major.live.title
        desc_first = self.major.live.desc_first
        badge_text = self.major.live.badge.text
        cover = self.major.live.cover + "@406w_254h_1e_1c.webp"
        desc_second = self.major.live.desc_second
        sub_info = desc_first + " • " + desc_second

        cover_img = self.__get_pic({"url": cover})
        color = self.main_color if self.forward else self.repost_color
        main_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                       size=main_font_size)
        sub_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                      size=sub_font_size)
        content = Image.new("RGBA", (1036, 254), color)
        content.paste(cover_img, (0, 0))

        draw = ImageDraw.Draw(content)
        draw.text(xy=(438, 16), text=title, fill=main_font_color, font=main_font)
        draw.text(xy=(438, 200), text=sub_info, fill=sub_font_color, font=sub_font)
        badge = Image.new("RGBA", (130, 50), "#e56187")
        draw = ImageDraw.Draw(badge)
        badge_text_size = main_font.getsize(badge_text)
        draw.text(xy=(int((130 - badge_text_size[0]) / 2), int((50 - badge_text_size[1]) / 2 - 3)), text=badge_text,
                  fill="white", font=main_font)
        content.paste(badge, (260, 15))
        self.client.close()
        return content

    async def __major_type_medialist(self):
        """收藏夹"""
        self.client = httpx.Client()
        # 读取配置
        main_font_color = self.config.get("Color", "main_font_color")
        main_font_name = self.config.get("Font", "main_font")
        main_font_size = self.config.getint("Size", "uname_font_size")
        sub_font_size = self.config.getint("Size", "sub_font_size")
        sub_font_color = self.config.get("Color", "sub_font_color")
        # 读取信息
        title = self.major.medialist.title
        sub_info = self.major.medialist.sub_title
        cover = self.major.medialist.cover + "@406w_254h_1e_1c.webp"
        badge_text = self.major.medialist.badge.text

        cover_img = self.__get_pic({"url": cover})
        color = self.main_color if self.forward else self.repost_color
        main_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                       size=main_font_size)
        sub_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                      size=sub_font_size)
        content = Image.new("RGBA", (1036, 254), color)
        content.paste(cover_img, (0, 0))

        draw = ImageDraw.Draw(content)
        draw.text(xy=(438, 24), text=title, fill=main_font_color, font=main_font)
        draw.text(xy=(438, 200), text=sub_info, fill=sub_font_color, font=sub_font)
        badge = Image.new("RGBA", (130, 50), "#e56187")
        draw = ImageDraw.Draw(badge)
        badge_text_size = main_font.getsize(badge_text)
        draw.text(xy=(int((130 - badge_text_size[0]) / 2), int((50 - badge_text_size[1]) / 2 - 3)), text=badge_text,
                  fill="white", font=main_font)
        content.paste(badge, (870, 30))
        self.client.close()
        return content

    async def __major_type_none(self):
        """失效资源"""
        # 读取配置
        # main_font_color = self.config.get("Color", "main_font_color")
        main_font_name = self.config.get("Font", "main_font")
        # main_font_size = self.config.getint("Size", "uname_font_size")
        sub_font_size = self.config.getint("Size", "sub_font_size")
        sub_font_color = self.config.get("Color", "sub_font_color")
        # 读取major
        tips = self.major.none.tips
        color = self.repost_color if self.forward else self.main_color
        content = Image.new("RGBA", (1040, 40), color)
        sub_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name), sub_font_size)
        draw = ImageDraw.Draw(content)
        size = sub_font.getsize(tips)

        draw.text(xy=(10, int((40 - size[1]) / 2)), text=tips, fill=sub_font_color, font=sub_font)

        return content

    async def __major_courses(self):
        """付费课程"""
        self.client = httpx.Client()
        # 读取配置
        main_font_color = self.config.get("Color", "main_font_color")
        main_font_name = self.config.get("Font", "main_font")
        standby_font_name = self.config.get("Font", "standby_font")
        main_font_size = self.config.getint("Size", "main_font_size")
        sub_font_size = self.config.getint("Size", "sub_font_size")
        sub_font_color = self.config.get("Color", "sub_font_color")
        color = self.main_color if self.forward else self.repost_color
        # 获取major
        title = self.major.courses.title
        sub_title = self.major.courses.sub_title
        desc = self.major.courses.desc
        badge_text = self.major.courses.badge.text
        # 贴封面
        cover = self.major.courses.cover + "@406w_254h_1c.webp"
        cover_img = self.__get_pic({"url": cover})
        self.content = Image.new("RGBA", (1036, 254), color)
        self.content.paste(cover_img, (0, 0))
        # 写入主标题
        self.main_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                            size=main_font_size)
        self.standby_font = ImageFont.truetype(
            font=os.path.join(self.current_path, "Static", "Font", standby_font_name), size=main_font_size)
        self.draw = ImageDraw.Draw(self.content)
        self.draw.text(xy=(438, 18), text=title, fill=main_font_color, font=self.main_font)
        # 写入desc
        desc_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                       size=sub_font_size)
        self.draw.text(xy=(438, 180), text=desc, fill=main_font_color, font=desc_font)
        # 计算sub_title
        self.main_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                            size=sub_font_size)
        sub_title_position = await self.__calculate_position(start_x=438,
                                                             start_y=80,
                                                             x_constraint=996,
                                                             y_constraint=80 + sub_font_size * 2,
                                                             text=sub_title,
                                                             text_size=sub_font_size,
                                                             emoji_list=[],
                                                             main_font_name=main_font_name,
                                                             standby_font_name=standby_font_name,
                                                             font_color=sub_font_color)
        with ThreadPoolExecutor(max_workers=5) as pool:
            pool.map(self.draw_pic, sub_title_position)

        badge = Image.new("RGBA", (130, 50), "#e56187")
        draw = ImageDraw.Draw(badge)
        badge_text_size = self.main_font.getsize(badge_text)
        draw.text(xy=(int((130 - badge_text_size[0]) / 2), int((50 - badge_text_size[1]) / 2) - 5), text=badge_text,
                  fill="white", font=self.main_font)
        self.content.paste(badge, (260, 15))

        self.client.close()
        return self.content

    async def __major_type_pgc(self):
        """番剧、电影、纪录片、电视剧"""
        self.client = httpx.Client()
        # 读取配置
        main_font_color = self.config.get("Color", "main_font_color")
        main_font_name = self.config.get("Font", "main_font")
        main_font_size = self.config.getint("Size", "main_font_size")
        sub_font_size = self.config.getint("Size", "sub_font_size")
        sub_font_color = self.config.get("Color", "sub_font_color")
        color = self.main_color if self.forward else self.repost_color
        # 读取major信息
        cover = self.major.pgc.cover + "@406w_254h_1e_1c.webp"
        title = self.major.pgc.title
        badge_text = self.major.pgc.badge.text
        sub_text = "播放:" + self.major.pgc.stat.play + "     " + "弹幕:" + self.major.pgc.stat.danmaku

        cover_img = self.__get_pic({"url": cover})
        content = Image.new("RGBA", (1036, 254), color)
        content.paste(cover_img, (0, 0))

        main_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                       size=main_font_size)
        sub_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                      size=sub_font_size)

        draw = ImageDraw.Draw(content)
        draw.text(xy=(438, 16), text=title, fill=main_font_color, font=main_font)
        draw.text(xy=(438, 200), text=sub_text, fill=sub_font_color, font=sub_font)
        badge = Image.new("RGBA", (130, 50), "#e56187")
        draw = ImageDraw.Draw(badge)
        badge_text_size = main_font.getsize(badge_text)
        draw.text(xy=(int((130 - badge_text_size[0]) / 2), int((50 - badge_text_size[1]) / 2 - 3)), text=badge_text,
                  fill="white", font=main_font)
        content.paste(badge, (260, 15))
        self.client.close()
        return content

    async def __major_type_common(self):
        """常见的方形card"""
        self.client = httpx.Client()
        if self.major.common.biz_type in [201]:
            img = await self.__common_comic()
        else:
            img = await self.__common_other()
        return img

    async def __major_type_music(self):
        """音乐"""
        self.client = httpx.Client()
        # 读取配置
        main_font_color = self.config.get("Color", "main_font_color")
        main_font_name = self.config.get("Font", "main_font")
        main_font_size = self.config.getint("Size", "main_font_size")
        sub_font_size = self.config.getint("Size", "sub_font_size")
        sub_font_color = self.config.get("Color", "sub_font_color")
        standby_font_name = self.config.get("Font", "standby_font")
        color = self.main_color if self.forward else self.repost_color
        # 读取major
        cover = self.major.music.cover + '@160w_160h_1c.webp'
        label = self.major.music.label
        title = self.major.music.title
        # 处理
        cover_img = self.__get_pic({"url": cover})
        self.content = Image.new("RGBA", (1036, 160), color)
        self.content.paste(cover_img, (0, 0), cover_img)
        self.main_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                            size=main_font_size)
        self.standby_font = ImageFont.truetype(
            font=os.path.join(self.current_path, "Static", "Font", standby_font_name), size=main_font_size)
        self.draw = ImageDraw.Draw(self.content)
        title_position = await self.__calculate_position(start_x=190,
                                                         start_y=32,
                                                         x_constraint=996,
                                                         y_constraint=32,
                                                         text=title,
                                                         text_size=main_font_size,
                                                         main_font_name=main_font_name,
                                                         standby_font_name=standby_font_name,
                                                         font_color=main_font_color,
                                                         emoji_list=[])

        with ThreadPoolExecutor(max_workers=5) as pool:
            pool.map(self.draw_pic, title_position)
        sub_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                      size=sub_font_size)
        self.draw.text(xy=(190, 100), text=label, fill=sub_font_color, font=sub_font)
        self.client.close()
        return self.content

    async def __major_type_article(self):
        """专栏"""
        self.client = httpx.Client()
        # 读取配置
        main_font_color = self.config.get("Color", "main_font_color")
        main_font_name = self.config.get("Font", "main_font")
        standby_font_name = self.config.get("Font", "standby_font")
        main_font_size = self.config.getint("Size", "uname_font_size")
        sub_font_size = self.config.getint("Size", "sub_font_size")
        sub_font_color = self.config.get("Color", "sub_font_color")
        color = self.main_color if self.forward else self.repost_color
        # 读取major消息
        covers = self.major.article.covers
        desc = self.major.article.desc
        title = self.major.article.title
        # 容器
        self.content = Image.new("RGBA", (1036, 420), color)
        src_list = []
        if len(covers) == 1:
            src = covers[0]
            src_list.append({"url": src + "@1036w_240h_1c.webp", "size": (1036, 240)})
        else:
            for i in covers:
                src_list.append({"url": i + "@340w_240h_1c.webp"})
        with ThreadPoolExecutor(max_workers=3) as pool:
            result = pool.map(self.__get_pic, src_list)
            x, y = 0, 0
            for i in result:
                self.content.paste(i, (x, y))
                x += 350
        tasks = [self.__calculate_position(start_x=30, start_y=260, x_constraint=996,
                                           y_constraint=260,
                                           text_size=main_font_size,
                                           text=title,
                                           emoji_list=[],
                                           main_font_name=main_font_name,
                                           standby_font_name=standby_font_name,
                                           font_color=main_font_color),
                 self.__calculate_position(start_x=30, start_y=330, x_constraint=996,
                                           y_constraint=330 + sub_font_size * 2, text_size=sub_font_size,
                                           text=desc,
                                           emoji_list=[],
                                           main_font_name=main_font_name,
                                           standby_font_name=standby_font_name,
                                           font_color=sub_font_color)]
        position_info = await asyncio.gather(*tasks)
        self.main_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                            size=main_font_size)
        self.standby_font = ImageFont.truetype(
            font=os.path.join(self.current_path, "Static", "Font", standby_font_name), size=main_font_size)
        self.draw = ImageDraw.Draw(self.content)
        with ThreadPoolExecutor(max_workers=5) as pool:
            pool.map(self.draw_pic, position_info[0])

        self.main_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                            size=sub_font_size)
        self.standby_font = ImageFont.truetype(
            font=os.path.join(self.current_path, "Static", "Font", standby_font_name), size=sub_font_size)
        with ThreadPoolExecutor(max_workers=5) as pool:
            pool.map(self.draw_pic, position_info[1])

        self.client.close()
        return self.content

    async def __major_type_draw(self):
        """图片类型"""
        self.client = httpx.Client()
        items = self.major.draw.items
        color = self.repost_color if self.forward else self.main_color
        img_count = len(items)
        if img_count == 1:
            img_height = items[0].height
            img_width = items[0].width
            src = items[0].src
            if img_height / img_width > 3:
                img_url = src + f"@{img_width}w_{img_width}h_!header.webp"
            else:
                img_url = src
            img = self.__get_pic({"url": img_url})
            img = img.resize((1068, int(img.size[1] * 1068 / img.size[0])), Image.ANTIALIAS)
            content = Image.new("RGBA", (1068, img.size[1] + 20), color)
            content.paste(img, (0, 0))
        elif img_count in [2, 4]:
            pic_list = []
            for i in items:
                if i.height / i.width >= 3:
                    img_url = i.src + '@250w_250h_!header.webp'
                    pic_list.append({"url": img_url, "size": (504, 504)})
                    continue
                img_url = i.src + '@250w_250h_1e_1c.webp'
                pic_list.append({"url": img_url, "size": (504, 504)})
            with ThreadPoolExecutor(max_workers=4) as pool:
                results = pool.map(self.__get_pic, pic_list)
            num = int(img_count / 2)
            content = Image.new("RGBA", (1068, 504 * num + 40), color)
            x, y = 20, 10
            for i in results:
                content.paste(i, (x, y))
                x += 524
                if x > 1000:
                    x = 20
                    y += 524
        else:
            pic_list = []
            for i in items:
                if i.height / i.width >= 3:
                    img_url = i.src + '@250w_250h_!header.webp'
                    pic_list.append({"url": img_url, "size": (342, 342)})
                    continue
                img_url = i.src + '@250w_250h_1e_1c.webp'
                pic_list.append({"url": img_url, "size": (342, 342)})
            with ThreadPoolExecutor(max_workers=9) as pool:
                results = pool.map(self.__get_pic, pic_list)
            num = math.ceil(img_count / 3)
            content = Image.new("RGBA", (1068, 342 * num + 40), color)
            x, y = 10, 10
            for i in results:
                i = i.resize((342, 342), Image.ANTIALIAS)
                content.paste(i, (x, y))
                x += 352
                if x > 1000:
                    x = 10
                    y += 352
        self.client.close()
        return content

    async def __major_type_live_rcmd(self):
        """分享直播"""
        self.client = httpx.Client()
        # 读取配置
        main_font_color = self.config.get("Color", "main_font_color")
        main_font_name = self.config.get("Font", "main_font")
        main_font_size = self.config.getint("Size", "main_font_size")
        sub_font_size = self.config.getint("Size", "sub_font_size")
        sub_font_color = self.config.get("Color", "sub_font_color")
        # 读取major信息
        title = self.major.live_rcmd.content.live_play_info.title
        area_name = self.major.live_rcmd.content.live_play_info.area_name
        badge_text = "直播中"
        cover = self.major.live_rcmd.content.live_play_info.cover + "@406w_254h_1e_1c.webp"
        online = str(self.major.live_rcmd.content.live_play_info.online) + "人气"
        sub_info = area_name + " • " + online

        cover_img = self.__get_pic({"url": cover})
        color = self.main_color if self.forward else self.repost_color
        main_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                       size=main_font_size)
        sub_font = ImageFont.truetype(os.path.join(self.current_path, "Static", "Font", main_font_name),
                                      size=sub_font_size)
        content = Image.new("RGBA", (1036, 254), color)
        content.paste(cover_img, (0, 0))

        draw = ImageDraw.Draw(content)
        draw.text(xy=(438, 16), text=title, fill=main_font_color, font=main_font)
        draw.text(xy=(438, 200), text=sub_info, fill=sub_font_color, font=sub_font)
        badge = Image.new("RGBA", (130, 50), "#e56187")
        draw = ImageDraw.Draw(badge)
        badge_text_size = main_font.getsize(badge_text)
        draw.text(xy=(int((130 - badge_text_size[0]) / 2), int((50 - badge_text_size[1]) / 2 - 3)), text=badge_text,
                  fill="white", font=main_font)
        content.paste(badge, (260, 15))
        self.client.close()
        return content

    async def __major_type_archive(self):
        """视频"""
        self.client = httpx.Client()
        # 读取配置
        main_font_color = self.config.get("Color", "main_font_color")
        main_font_name = self.config.get("Font", "main_font")
        standby_font_name = self.config.get("Font", "standby_font")
        main_font_size = self.config.getint("Size", "main_font_size")
        sub_font_size = self.config.getint("Size", "sub_font_size")
        sub_font_color = self.config.get("Color", "sub_font_color")
        color = self.main_color if self.forward else self.repost_color
        # 获取视频信息
        title = self.major.archive.title
        desc = self.major.archive.desc
        cover = self.major.archive.cover + "@406w_254h_1e_1c.webp"
        badge_text = self.major.archive.badge.text
        cover_img = self.__get_pic({"url": cover})
        # 制作容器
        self.content = Image.new("RGBA", (1036, 254), color)
        self.content.paste(cover_img, (0, 0))
        # 获取title内的emoji
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
        # 获取desc内的emoji
        desc_emoji_info = emoji.emoji_lis(desc)
        desc_emoji_list = []
        if desc_emoji_info:
            # 将所有emoji内容放进列表内
            for i in desc_emoji_info:
                desc_emoji_list.append(i["emoji"])
            temp = []
            for i in desc_emoji_list:
                if len(i) != 1:
                    emoji_first = i[0]
                    title = title.replace(i, emoji_first)
                    temp.append(emoji_first)
                    continue
                else:
                    temp.append(i)
                    continue
            desc_emoji_list = temp

        self.main_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                            size=main_font_size)
        self.standby_font = ImageFont.truetype(
            font=os.path.join(self.current_path, "Static", "Font", standby_font_name), size=main_font_size)
        self.draw = ImageDraw.Draw(self.content)
        tasks = [self.__calculate_position(start_x=438, start_y=18, x_constraint=1000,
                                           y_constraint=18 + main_font_size * 2,
                                           text_size=main_font_size,
                                           text=title,
                                           emoji_list=title_emoji_list,
                                           main_font_name=main_font_name,
                                           standby_font_name=standby_font_name,
                                           font_color=main_font_color),
                 self.__calculate_position(start_x=438, start_y=120, x_constraint=1000,
                                           y_constraint=120 + sub_font_size * 2, text_size=sub_font_size,
                                           text=desc,
                                           emoji_list=desc_emoji_list,
                                           main_font_name=main_font_name,
                                           standby_font_name=standby_font_name,
                                           font_color=sub_font_color)]
        position_info = await asyncio.gather(*tasks)
        with ThreadPoolExecutor(max_workers=5) as pool:
            pool.map(self.draw_pic, position_info[0])

        self.main_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                            size=sub_font_size)
        self.standby_font = ImageFont.truetype(
            font=os.path.join(self.current_path, "Static", "Font", standby_font_name), size=sub_font_size)
        with ThreadPoolExecutor(max_workers=5) as pool:
            pool.map(self.draw_pic, position_info[1])
        badge = Image.new("RGBA", (130, 50), "#e56187")
        draw = ImageDraw.Draw(badge)
        badge_text_size = self.main_font.getsize(badge_text)
        draw.text(xy=(int((130 - badge_text_size[0]) / 2), int((50 - badge_text_size[1]) / 2) - 5), text=badge_text,
                  fill="white", font=self.main_font)
        self.content.paste(badge, (260, 15))
        self.client.close()
        return self.content

    async def __common_comic(self):
        # 读取配置
        main_font_color = self.config.get("Color", "main_font_color")
        main_font_name = self.config.get("Font", "main_font")
        main_font_size = self.config.getint("Size", "main_font_size")
        sub_font_size = self.config.getint("Size", "sub_font_size")
        sub_font_color = self.config.get("Color", "sub_font_color")
        color = self.main_color if self.forward else self.repost_color
        # 读取major信息
        cover = self.major.common.cover + "@240w_320h_1c.webp"
        title = self.major.common.title
        desc = self.major.common.desc
        label = self.major.common.label
        badge_text = self.major.common.badge.text
        content = Image.new("RGBA", (1040, 320), color)
        main_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                       size=main_font_size)
        sub_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                      size=sub_font_size)
        cover_img = self.__get_pic({"url": cover})
        draw = ImageDraw.Draw(content)
        draw.text(xy=(270, 30), text=title, fill=main_font_color, font=main_font)
        draw.text(xy=(270, 90), text=desc, fill=sub_font_color, font=sub_font)
        draw.text(xy=(270, 150), text=label, fill=sub_font_color, font=sub_font)
        badge = Image.new("RGBA", (74, 34), "#FB7299")
        draw = ImageDraw.Draw(badge)
        badge_text_size = sub_font.getsize(badge_text)
        badge_position = (int((74 - badge_text_size[0]) / 2), int((34 - badge_text_size[1]) / 2) - 3)
        draw.text(xy=badge_position, text=badge_text, font=sub_font, fill="#ffffff")
        content.paste(badge, (910, 35))
        content.paste(cover_img, (0, 0))
        self.client.close()
        return content

    async def __common_other(self):
        # 读取配置
        main_font_color = self.config.get("Color", "main_font_color")
        main_font_name = self.config.get("Font", "main_font")
        main_font_size = self.config.getint("Size", "main_font_size")
        sub_font_size = self.config.getint("Size", "sub_font_size")
        sub_font_color = self.config.get("Color", "sub_font_color")
        standby_font_name = self.config.get("Font", "standby_font")
        color = self.main_color if self.forward else self.repost_color
        # 读取major
        badge_text = self.major.common.badge.text
        cover = self.major.common.cover + "@160w_160h_1c.webp"
        title = self.major.common.title
        desc = self.major.common.desc
        cover_img = self.__get_pic({"url": cover})
        self.content = Image.new("RGBA", (1040, 160), color)
        self.content.paste(cover_img, (0, 0), cover_img)
        self.main_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                            size=main_font_size)
        self.standby_font = ImageFont.truetype(
            font=os.path.join(self.current_path, "Static", "Font", standby_font_name), size=main_font_size)
        self.draw = ImageDraw.Draw(self.content)
        tasks = []
        if desc:
            tasks.append(self.__calculate_position(
                start_x=190,
                start_y=30,
                x_constraint=996,
                y_constraint=30,
                text_size=main_font_size,
                text=title,
                emoji_list=[],
                main_font_name=main_font_name,
                standby_font_name=standby_font_name,
                font_color=main_font_color
            ))
            tasks.append(
                self.__calculate_position(
                    start_x=190,
                    start_y=80,
                    x_constraint=996,
                    y_constraint=80,
                    text_size=sub_font_size,
                    text=desc,
                    emoji_list=[],
                    main_font_name=main_font_name,
                    standby_font_name=standby_font_name,
                    font_color=sub_font_color
                )
            )
        else:
            tasks.append(self.__calculate_position(
                start_x=190,
                start_y=60,
                x_constraint=996,
                y_constraint=60,
                text_size=main_font_size,
                text=title,
                emoji_list=[],
                main_font_name=main_font_name,
                standby_font_name=standby_font_name,
                font_color=main_font_color
            ))

        position_info = await asyncio.gather(*tasks)
        if len(tasks) == 1:
            with ThreadPoolExecutor(max_workers=5) as pool:
                pool.map(self.draw_pic, position_info[0])
        else:
            with ThreadPoolExecutor(max_workers=5) as pool:
                pool.map(self.draw_pic, position_info[0])
            self.main_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                                size=sub_font_size)
            with ThreadPoolExecutor(max_workers=5) as pool:
                pool.map(self.draw_pic, position_info[1])
        self.client.close()

        if badge_text:
            sub_font = ImageFont.truetype(font=os.path.join(self.current_path, "Static", "Font", main_font_name),
                                          size=sub_font_size)
            badge = Image.new("RGBA", (72, 34), self.major.common.badge.bg_color)
            draw = ImageDraw.Draw(badge)
            badge_text_size = sub_font.getsize(badge_text)
            badge_position = (int((74 - badge_text_size[0]) / 2), int((34 - badge_text_size[1]) / 2) - 3)
            draw.text(xy=badge_position, text=badge_text, font=sub_font, fill="#ffffff")
            self.content.paste(badge, (920, 30))
        return self.content

    def __get_pic(self, img_info):
        try:
            response = self.client.get(img_info["url"], timeout=500)
            img = Image.open(BytesIO(response.content)).convert("RGBA")
            if "size" in img_info.keys():
                img = img.resize(img_info["size"], Image.ANTIALIAS)
            return img
        except:
            logger.error(traceback.print_exc())
            response = httpx.get(img_info["url"], timeout=500)
            img = Image.open(BytesIO(response.content)).convert("RGBA")
            if "size" in img_info.keys():
                img = img.resize(img_info["size"], Image.ANTIALIAS)
            return img

    async def __calculate_position(self, start_x, start_y, x_constraint, y_constraint, text_size, text,
                                   emoji_list=None, main_font_name=None, standby_font_name=None,
                                   font_color=None) -> list:
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
        # text = text.replace("\r", "").replace(chr(65039),'').replace(chr(65038),'')
        text = text.translate(str.maketrans({'\r': '', chr(65039): '', chr(65038): '', chr(8205): ''}))
        for i in range(len(text)):
            if text[i] in emoji_list:
                emoji_size = self.emoji_font.getsize(text[i])
                img = Image.new("RGBA", emoji_size)
                draw = ImageDraw.Draw(img)
                draw.text(xy=(0, 0), text=text[i], font=self.emoji_font, embedded_color=True)
                # 把emoji图片缩放到文字字体的大小
                position_info.append(
                    {"info_type": "img", "content": img.resize((text_size, text_size), Image.ANTIALIAS),
                     "position": (x, y + 5)})
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
            if text[i] == "\n":
                continue
            if ord(text[i]) in font_key:
                position_info.append(
                    {"info_type": "text", "content": text[i], "font": "main", "position": (x, y), "color": font_color})
                x_interval = main_font.getsize(text[i])[0]
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
                    {"info_type": "text", "content": text[i], "font": "standby", "position": (x, y),
                     "color": font_color})
                x_interval = standby_font.getsize(text[i])[0]
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

    def draw_pic(self, word_info):
        font = {"standby": self.standby_font, "main": self.main_font}
        if word_info["info_type"] == "text":
            self.draw.text(xy=word_info["position"], text=word_info["content"], fill=word_info["color"],
                           font=font[word_info["font"]])
        else:
            self.content.paste(word_info["content"], word_info["position"], word_info["content"])
