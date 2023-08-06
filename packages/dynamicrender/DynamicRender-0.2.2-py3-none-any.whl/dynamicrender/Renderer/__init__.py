import asyncio
import configparser
import os
import traceback

from PIL import Image

from dynamicrender.DynamicChecker import Item
from dynamicrender.Logger import logger
from dynamicrender.Renderer.FooterRenderer import FooterRender
from dynamicrender.Renderer.HeaderRenderer import HeaderRender
from dynamicrender.Renderer.TextRenderer import TextRender
from dynamicrender.Renderer.AdditionRenderer import AdditionRender
from dynamicrender.Renderer.MajorRenderer import MajorRender
from dynamicrender.Renderer.ForwardRenderer import ForwardRender
class BiliRender:
    def __init__(self, dynamic: Item):
        self.__dynamic = dynamic
        self.__main_color = None
        self.check_file()
        self.function_dic = {"DYNAMIC_TYPE_WORD": self.word_dynamic,
                             "DYNAMIC_TYPE_DRAW": self.draw_dynamic,
                             "DYNAMIC_TYPE_AV": self.av_dynamic,
                             "DYNAMIC_TYPE_LIVE_RCMD": self.live_rcmd_dynamic,
                             "DYNAMIC_TYPE_LIVE":self.live_dynamic,
                             "DYNAMIC_TYPE_ARTICLE": self.article_dynamic,
                             "DYNAMIC_TYPE_COMMON_VERTICAL": self.vertical_dynamic,
                             "DYNAMIC_TYPE_COURSES_SEASON": self.course_dynamic,
                             "DYNAMIC_TYPE_MEDIALIST":self.media_list_dynamic,
                             "DYNAMIC_TYPE_PGC": self.video_dynamic,
                             "DYNAMIC_TYPE_MUSIC": self.music_dynamic,
                             "DYNAMIC_TYPE_COMMON_SQUARE": self.square_dynamic,
                             "DYNAMIC_TYPE_FORWARD": self.forward_dynamic

                             }

    def check_file(self):
        """
        第一次运行查看是否缺少文件
        :return:
        """
        # 当前程序运行路径
        current_path = os.getcwd()
        # 字体和图片的存储路径
        static_path = os.path.join(current_path, "Static")
        # 头像缓存路径
        face_cache_path = os.path.join(current_path, "Cache", "Face")
        # 挂件缓存路径
        pendant_cache_path = os.path.join(current_path, "Cache", "Pendant")
        # emoji缓存路径
        emoji_cache_path = os.path.join(current_path, "Cache", "Emoji")
        # 配置文件路径
        config_path = os.path.join(current_path, "config.ini")
        # 当前文件绝对路径
        curren_abs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if not os.path.exists(static_path):
            try:
                logger.info("创建静态文件目录")
                os.makedirs(static_path)
                self.copy_dir(os.path.join(curren_abs_path, "Static"), static_path)
                logger.info("静态文件创建完毕")
            except:
                logger.error("\n" + traceback.format_exc())
        else:
            pic_file_size = len(os.listdir(os.path.join(os.path.join(static_path, "Picture"))))
            font_file_size = len(os.listdir(os.path.join(os.path.join(static_path, "Font"))))
            if pic_file_size == 0 or font_file_size == 0:
                logger.error("缺少静态文件，请于https://gitee.com/DMC_der/DynamicRender2.0/tree/feature/下载对应静态文件并放于static目录内")
        if not os.path.exists(face_cache_path):
            logger.info("创建头像缓存目录")
            os.makedirs(face_cache_path)
        if not os.path.exists(pendant_cache_path):
            logger.info("创建挂件缓存目录")
            os.makedirs(pendant_cache_path)
        if not os.path.exists(emoji_cache_path):
            logger.info("创建emoji缓存目录")
            os.makedirs(emoji_cache_path)
        if not os.path.exists(config_path):
            logger.info("创建配置文件目录")
            config = configparser.ConfigParser()
            config['Logger'] = {
                'file_level': 'ERROR',
                'log_level': 'INFO'}
            config["Color"] = {
                'main_color': '#dcdad7',
                'repost_color': '#d5d3cf',
                'main_font_color': 'black',
                'sub_font_color': '#99a2aa',
                'extra_color': '#00a1d6'
            }
            config["Size"] = {
                'uname_font_size': 32,
                'main_font_size': 28,
                'sub_font_size': 24,
                'emoji_font_size': 109
            }
            config["Font"] = {
                'main_font': 'HanaMinA.ttf',
                'emoji_font': 'nte.ttf',
                'standby_font': 'Unifont.ttf',
            }
            with open(config_path, 'w') as cfg:
                config.write(cfg)
            self.__main_color = "#ffffff"
        else:
            config = configparser.ConfigParser()
            config.read(config_path)
            self.__main_color = config.get("Color", "main_color")

    async def render(self):
        img = await self.function_dic[self.__dynamic.type]()
        return img

    async def word_dynamic(self):
        """
        文本型动态处理函数
        :return:
        """
        try:
            tasks = []
            tasks.append(HeaderRender(self.__dynamic.modules.module_author).main_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic).main_text_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic).addition_render())
            tasks.append(FooterRender(self.__dynamic.id_str).foot_render())
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
            tasks.append(HeaderRender(self.__dynamic.modules.module_author).main_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic).addition_render())
            tasks.append(FooterRender(self.__dynamic.id_str).foot_render())
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
            tasks.append(HeaderRender(self.__dynamic.modules.module_author).main_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic).addition_render())
            tasks.append(FooterRender(self.__dynamic.id_str).foot_render())
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
            tasks.append(HeaderRender(self.__dynamic.modules.module_author).main_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic).addition_render())
            tasks.append(FooterRender(self.__dynamic.id_str).foot_render())
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
            tasks.append(HeaderRender(self.__dynamic.modules.module_author).main_header_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major).major_render())
            tasks.append(FooterRender(self.__dynamic.id_str).foot_render())
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
            tasks.append(HeaderRender(self.__dynamic.modules.module_author).main_header_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major).major_render())
            tasks.append(FooterRender(self.__dynamic.id_str).foot_render())
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
            tasks.append(HeaderRender(self.__dynamic.modules.module_author).main_header_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic).addition_render())
            tasks.append(FooterRender(self.__dynamic.id_str).foot_render())
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
            tasks.append(HeaderRender(self.__dynamic.modules.module_author).main_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic).addition_render())
            tasks.append(FooterRender(self.__dynamic.id_str).foot_render())
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
            tasks.append(HeaderRender(self.__dynamic.modules.module_author).main_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic).addition_render())
            tasks.append(FooterRender(self.__dynamic.id_str).foot_render())
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
            tasks.append(HeaderRender(self.__dynamic.modules.module_author).main_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic).addition_render())
            tasks.append(FooterRender(self.__dynamic.id_str).foot_render())
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
            tasks.append(HeaderRender(self.__dynamic.modules.module_author).main_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic).addition_render())
            tasks.append(FooterRender(self.__dynamic.id_str).foot_render())
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
            tasks.append(HeaderRender(self.__dynamic.modules.module_author).main_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic).main_text_render())
            tasks.append(MajorRender(self.__dynamic.modules.module_dynamic.major).major_render())
            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic).addition_render())
            tasks.append(FooterRender(self.__dynamic.id_str).foot_render())
            result = await asyncio.gather(*tasks)
            if result:
                img = await self.assemble_card(result)
                return img
            else:
                return
        except:
            logger.error("\n" + traceback.format_exc())
            return

    async def forward_dynamic(self):
        """
        转发类型的动态的处理函数
        :return:
        """
        try:
            tasks = []
            tasks.append(HeaderRender(self.__dynamic.modules.module_author).main_header_render())
            tasks.append(TextRender(self.__dynamic.modules.module_dynamic).main_text_render())

            tasks.append(ForwardRender(self.__dynamic.orig).render())

            if self.__dynamic.modules.module_dynamic.additional:
                tasks.append(AdditionRender(self.__dynamic.modules.module_dynamic).addition_render())
            tasks.append(FooterRender(self.__dynamic.id_str).foot_render())
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
        container = Image.new("RGBA", (1108, y), self.__main_color)
        position_y = 0
        for z in range(len(result)):
            if z != 0:
                if result[z - 1]:
                    position_y += result[z - 1].size[1]
            if result[z]:
                container.paste(result[z], (int((container.size[0] - result[z].size[0]) / 2), position_y))
        return container

    def copy_dir(self, src_path, target_path):
        if os.path.isdir(src_path) and os.path.isdir(target_path):
            filelist_src = os.listdir(src_path)
            for file in filelist_src:
                path = os.path.join(os.path.abspath(src_path), file)
                if os.path.isdir(path):
                    path1 = os.path.join(os.path.abspath(target_path), file)
                    if not os.path.exists(path1):
                        os.mkdir(path1)
                    self.copy_dir(path, path1)
                else:
                    with open(path, 'rb') as read_stream:
                        contents = read_stream.read()
                        path1 = os.path.join(target_path, file)
                        with open(path1, 'wb') as write_stream:
                            write_stream.write(contents)
            return True

        else:
            return False



