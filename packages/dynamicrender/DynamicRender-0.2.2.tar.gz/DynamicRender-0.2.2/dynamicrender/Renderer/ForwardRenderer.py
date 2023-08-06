import asyncio
import configparser
import os
import traceback

from PIL import Image, ImageFile

from dynamicrender.DynamicChecker import Orig
from dynamicrender.Logger import logger
from dynamicrender.Renderer.AdditionRenderer import AdditionRender
from dynamicrender.Renderer.HeaderRenderer import HeaderRender
from dynamicrender.Renderer.MajorRenderer import MajorRender
from dynamicrender.Renderer.TextRenderer import TextRender
ImageFile.LOAD_TRUNCATED_IMAGES = True
Image.MAX_IMAGE_PIXELS = None

class ForwardRender:
    def __init__(self, dynamic: Orig):
        self.__dynamic = dynamic
        self.__main_color = None
        self.function_dic = {"DYNAMIC_TYPE_WORD": self.word_dynamic,
                             "DYNAMIC_TYPE_DRAW": self.draw_dynamic,
                             "DYNAMIC_TYPE_AV": self.av_dynamic,
                             "DYNAMIC_TYPE_LIVE_RCMD": self.live_rcmd_dynamic,
                             "DYNAMIC_TYPE_LIVE": self.live_dynamic,
                             "DYNAMIC_TYPE_ARTICLE": self.article_dynamic,
                             "DYNAMIC_TYPE_COMMON_VERTICAL": self.vertical_dynamic,
                             "DYNAMIC_TYPE_COURSES_SEASON": self.course_dynamic,
                             "DYNAMIC_TYPE_MEDIALIST": self.media_list_dynamic,
                             "DYNAMIC_TYPE_PGC": self.video_dynamic,
                             "DYNAMIC_TYPE_MUSIC": self.music_dynamic,
                             "DYNAMIC_TYPE_COMMON_SQUARE": self.square_dynamic,
                             "DYNAMIC_TYPE_NONE": self.none_dynamic
                             }

    async def render(self):
        current_path = os.getcwd()
        config = configparser.ConfigParser()
        config_path = os.path.join(current_path, "config.ini")
        config.read(config_path)
        try:
            self.__main_color = config.get("Color", "repost_color")
            img = await self.function_dic[self.__dynamic.type]()
            return img
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def word_dynamic(self):
        """
        文本型动态处理函数
        :return:
        """
        try:
            tasks = []
            tasks.append(HeaderRender(self.__dynamic.modules.module_author, forward=True).origin_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic, forward=True).main_text_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic, forward=True).addition_render())
            result = await asyncio.gather(*tasks)
            if result:
                img = await self.assemble_card(result)
                return img
            else:
                return
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def draw_dynamic(self):
        """
        图片带文本型动态处理函数
        :return:
        """
        try:
            tasks = []
            tasks.append(HeaderRender(self.__dynamic.modules.module_author, forward=True).origin_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic, forward=True).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major, forward=True).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic, forward=True).addition_render())
            result = await asyncio.gather(*tasks)
            if result:
                img = await self.assemble_card(result)
                return img
            else:
                return
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def media_list_dynamic(self):
        """
        收藏
        :return:
        """
        try:
            tasks = []
            tasks.append(HeaderRender(self.__dynamic.modules.module_author, forward=True).origin_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic, forward=True).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major, forward=True).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic, forward=True).addition_render())
            result = await asyncio.gather(*tasks)
            if result:
                img = await self.assemble_card(result)
                return img
            else:
                return
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def av_dynamic(self):
        """
        视频类型动态处理函数
        :return:
        """
        try:
            tasks = []
            tasks.append(HeaderRender(self.__dynamic.modules.module_author, forward=True).origin_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic, forward=True).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major, forward=True).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic, forward=True).addition_render())
            result = await asyncio.gather(*tasks)
            if result:
                img = await self.assemble_card(result)
                return img
            else:
                return
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def live_rcmd_dynamic(self):
        """
        直播类型动态处理函数
        :return:
        """
        try:
            tasks = []
            tasks.append(HeaderRender(self.__dynamic.modules.module_author, forward=True).origin_header_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major, forward=True).major_render())
            result = await asyncio.gather(*tasks)
            if result:
                img = await self.assemble_card(result)
                return img
            else:
                return
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def live_dynamic(self):
        """
       直播类型动态处理函数
       :return:
       """
        try:
            tasks = []
            tasks.append(HeaderRender(self.__dynamic.modules.module_author, forward=True).origin_header_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major, forward=True).major_render())
            result = await asyncio.gather(*tasks)
            if result:
                img = await self.assemble_card(result)
                return img
            else:
                return
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def article_dynamic(self):
        """
        专栏类型动态处理函数
        :return:
        """
        try:
            tasks = []
            tasks.append(HeaderRender(self.__dynamic.modules.module_author, forward=True).origin_header_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major, forward=True).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic, forward=True).addition_render())
            result = await asyncio.gather(*tasks)
            if result:
                img = await self.assemble_card(result)
                return img
            else:
                return
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def vertical_dynamic(self):
        """
        漫画类型的动态处理函数
        :return:
        """
        try:
            tasks = []
            tasks.append(HeaderRender(self.__dynamic.modules.module_author, forward=True).origin_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic, forward=True).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major, forward=True).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic).addition_render())
            result = await asyncio.gather(*tasks)
            if result:
                img = await self.assemble_card(result)
                return img
            else:
                return
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def course_dynamic(self):
        """
        付费课程类型的处理函数
        :return:
        """
        try:
            tasks = []
            tasks.append(HeaderRender(self.__dynamic.modules.module_author, forward=True).origin_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic, forward=True).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major, forward=True).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic, forward=True).addition_render())
            result = await asyncio.gather(*tasks)
            if result:
                img = await self.assemble_card(result)
                return img
            else:
                return
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def video_dynamic(self):
        """
        动漫、纪录片、电影、电视剧等类型的处理函数
        :return:
        """
        try:
            tasks = []
            tasks.append(HeaderRender(self.__dynamic.modules.module_author, forward=True).origin_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic, forward=True).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major, forward=True).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic, forward=True).addition_render())
            result = await asyncio.gather(*tasks)
            if result:
                img = await self.assemble_card(result)
                return img
            else:
                return
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def music_dynamic(self):
        """
        音乐类型动态的处理函数
        :return:
        """
        try:
            tasks = []
            tasks.append(HeaderRender(self.__dynamic.modules.module_author, forward=True).origin_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic, forward=True).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major, forward=True).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic, forward=True).addition_render())
            result = await asyncio.gather(*tasks)
            if result:
                img = await self.assemble_card(result)
                return img
            else:
                return
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def square_dynamic(self):
        """
        装扮、歌单、活动等的处理函数
        :return:
        """
        try:
            tasks = []
            tasks.append(HeaderRender(self.__dynamic.modules.module_author, forward=True).origin_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic, forward=True).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major, forward=True).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic, forward=True).addition_render())
            result = await asyncio.gather(*tasks)
            if result:
                img = await self.assemble_card(result)
                return img
            else:
                return
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def none_dynamic(self):
        try:
            tasks = [MajorRender(self.__dynamic.modules.module_dynamic.major, forward=True).major_render()]
            result = await asyncio.gather(*tasks)
            if result:
                img = await self.assemble_card(result)
                return img
            else:
                return
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def assemble_card(self, result):
        y = 0
        for i in result:
            if i:
                y += i.size[1]
        container = Image.new("RGBA", (1088, y + 20), self.__main_color)
        position_y = 0
        for z in range(len(result)):
            if z != 0:
                if result[z - 1]:
                    position_y += result[z - 1].size[1]
            if result[z]:
                container.paste(result[z], (int((container.size[0] - result[z].size[0]) / 2), position_y))
        return container

# if __name__ == '__main__':
#     print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
