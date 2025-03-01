from typing import List, Dict, Optional
from astrbot.api.event import filter
from astrbot.api.all import *
import os
from typing import (Dict, Any, Optional, AnyStr, Callable, Union, Awaitable,
                    Coroutine)

from data.plugins.astrbot_plugin_moreapi.api_collection import api,emoji,image,translate, text, search
from data.plugins.astrbot_plugin_moreapi.api_collection import video, music, guangyu, chess, blue_archive
@register("astrbot_plugin_moreapi", "达莉娅",
          "多功能调用插件，发【api】看菜单",
          "v1.7.0")
class MyPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.op = False
        self.flag2 = True
        self.flag = False
        self.song_name = None
        self.rooms = []
        self.config = config
        self.file_path = './data/plugins/astrbot_plugin_moreapi/data.jsonl'
        if not os.path.exists(self.file_path):
            self.save_game()
            print(f"文件 {self.file_path} 不存在，已创建并初始化。")
        else:
            print(f"文件 {self.file_path} 已存在，跳过创建。")
        self.load_game()
        #self.api_name = config.get('name', 'FunAudioLLM/CosyVoice2-0.5B')

    def load_game(self):
        dicts = []
        with open(self.file_path, 'r') as f:
            for line in f:
                dicts.append(json.loads(line.strip()))
        # 分配到各自的字典
        if not dicts:  # 如果 dicts 为空
            logger.warning("加载的数据为空")
            return
        else:
            self.rooms = dicts[0]
            return

    def save_game(self):
        with open(self.file_path, 'w') as f:
            f.write(json.dumps(self.rooms) + '\n')
    '''---------------------------------------------------'''
    @command("test")
    async def test(self, event: AstrMessageEvent):
        provider = self.context.get_using_provider()
        if provider:
            response = await provider.text_chat("你好", session_id=event.session_id)
            print(response.completion_text)  # LLM 返回的结果

    '''注册一个 LLM 函数工具function-calling 给了大语言模型调用外部工具的能力。
    注册一个 function-calling 函数工具。
    请务必按照以下格式编写一个工具（包括函数注释，AstrBot 会尝试解析该函数注释）'''
    '''---------------------------------------------------'''
    @filter.command("api")
    async def menu(self, event: AstrMessageEvent):
        img = "./data/plugins/astrbot_plugin_moreapi/menu_output.png"
        if not os.path.exists(img):
            result = api.get_menu()
        else:
            result = event.make_result()
            result.chain = [Plain(f"MOREAPI菜单：\n"), Image.fromFileSystem(img)]
        await event.send(result)
    @filter.command("光遇任务")
    async def trap0(self, event: AstrMessageEvent):
        result = guangyu.fetch_daily_tasks()
        await event.send(result)
    @filter.command("小姐姐视频")
    async def trap1(self, event: AstrMessageEvent):
        result = video.xjj()
        await event.send(result)
    @filter.command("电影票房")
    async def trap2(self, event: AstrMessageEvent):
        result = text.movie()
        await event.send(result)
    @filter.command("b站番剧")
    async def trap3(self, event: AstrMessageEvent,num:Optional[str] = '5'):
        result = search.get_update_days(num)
        await event.send(result)
    @filter.command("cosplay")
    async def trap4(self, event: AstrMessageEvent):
        dat = image.fetch_cosplay_data()
        result = MessageChain()
        result.chain = []
        for reg in dat:
            result.chain.append(reg)
            await event.send(result)
            result.chain = []
    @filter.command("翻译")
    async def trap5(self, event: AstrMessageEvent):
        msg = event.get_message_str()
        parts = msg.split(maxsplit = 1)
        result = translate.translate_text(parts[1])
        await event.send(result)
    @filter.command("每日段子")
    async def trap6(self, event: AstrMessageEvent):
        result = text.get_random_text()
        await event.send(result)
    @filter.command("毒鸡汤")
    async def trap9(self, event: AstrMessageEvent):
        result = text.get_dujitang()
        await event.send(result)
    @filter.command("搜狗搜图")
    async def trap7(self, event: AstrMessageEvent,a:str):
        result = search.fetch_image_url(a)
        await event.send(result)
    @filter.command("天气")
    async def trap8(self, event: AstrMessageEvent,a:str):
        result = search.get_weather(a)
        await event.send(result)
    @filter.command("头像框")
    async def trap10(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        result = emoji.get_qq_avatar(ids)
        await event.send(result)
    @filter.command("小人举牌")
    async def trap11(self, event: AstrMessageEvent,a:str):
        result = emoji.fetch_image_from_api(a)
        await event.send(result)
    @filter.command("音乐推荐")
    async def trap12(self, event: AstrMessageEvent):
        result = music.get_music()
        det = music.search_music3()
        voice = MessageChain()
        voice.chain.append(Record(file=det))
        await event.send(voice)
        await event.send(result)
    @filter.command("随机原神")
    async def trap13(self, event: AstrMessageEvent):
        result = image.call_api()
        await event.send(result)
    @filter.command("随机龙图")
    async def trap14(self, event: AstrMessageEvent):
        result = image.call_api2()
        await event.send(result)
    @filter.command("温柔语录")
    async def trap15(self, event: AstrMessageEvent):
        result = text.get_random_text2()
        await event.send(result)
    @filter.command("手写")
    async def trap16(self, event: AstrMessageEvent,a:str):
        result = emoji.generate_image12(a)
        await event.send(result)
    @filter.command("塔罗牌")
    async def trap17(self, event: AstrMessageEvent):
        result = image.get_tarot_reading()
        await event.send(result)
    @filter.command("随机生成超能力")
    async def trap18(self, event: AstrMessageEvent):
        result = image.get_random_superpower()
        await event.send(result)
    @filter.command("网页截图")
    async def trap19(self, event: AstrMessageEvent, url: str):
        result = image.get_webpage_screenshot(url)
        await event.send(result)
    @filter.command("emoji合成")
    async def trap20(self, event: AstrMessageEvent, emoji1: str, emoji2: str):
        result = emoji.mix_emojis(emoji1, emoji2)
        await event.send(result)
    @filter.command("ikun图片")
    async def trap21(self, event: AstrMessageEvent, lx: str = "bqb"):
        result = image.get_ikun_image(lx)
        await event.send(result)
    @filter.command("原神cosplay")
    async def trap22(self, event: AstrMessageEvent):
        result = image.get_random_genshin_cosplay()
        await event.send(result)
    @filter.command("搜索音乐")
    async def trap23(self, event: AstrMessageEvent, song_name: str, n: Optional[str] = None):
        self.song_name = song_name
        result = music.search_music(song_name, n)
        await event.send(result)
    @filter.command("音乐")
    async def trap24(self, event: AstrMessageEvent,n: int):
        result = music.search_music(self.song_name, n)
        det = music.search_music2()
        voice = MessageChain()
        voice.chain.append(Record(file=det))
        await event.send(voice)
        await event.send(result)
    @filter.command("五子棋")
    async def trap25(self, event: AstrMessageEvent, types:str = '0', x: Optional[str] = None,y: Optional[str] = None):
        qq = event.get_sender_id()
        group = event.get_group_id()
        result = chess.play_gobang(qq, group, types, x, y)
        await event.send(result)
    @filter.command("每日新闻")
    async def trap26(self, event: AstrMessageEvent):
        result = image.get_daily_60s_news()
        await event.send(result)
    @filter.command("搜索b站视频")
    async def trap27(self, event: AstrMessageEvent, msg: str, n:Optional[str]= "1"):
        result = video.search_bilibili_video(msg, n)
        det = video.movie1()
        voice = MessageChain()
        voice.chain.append(Video.fromURL(det))
        await event.send(voice)
        await event.send(result)
    @filter.command("百科查询")
    async def trap28(self, event: AstrMessageEvent, msg: str):
        result = search.get_baike_info(msg)
        await event.send(result)
    @filter.command("电视剧排行榜")
    async def trap29(self, event: AstrMessageEvent):
        result = text.get_tv_show_heat_ranking()
        await event.send(result)
    @filter.command("斗图")
    async def trap30(self, event: AstrMessageEvent, msg: str):
        result = image.get_doutu_images(msg)
        await event.send(result)
    @filter.command("百度题库")
    async def trap31(self, event: AstrMessageEvent, question: str):
        result = search.get_baidu_tiku_answer(question)
        await event.send(result)
    @filter.command("ba攻略")
    async def trap32(self, event: AstrMessageEvent,a: str):
        ba = blue_archive.Baarchive()
        result = ba.handle_blue_archive(a)
        await event.send(result)
    @filter.command("随机制作")
    async def emoji0(self, event: AstrMessageEvent,msg:Optional[str] = '',msg2:Optional[str] = ''):
        ids = emoji.parse_target(event)
        ids2 = emoji.parse_target2(event,ids)
        data = emoji.fetch_image2(ids,ids2,msg,msg2)
        await event.send(data)
    @filter.command("摸头")
    async def emoji1(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "摸头")
        await event.send(data)
    @filter.command("感动哭了")
    async def emoji2(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "感动哭了")
        await event.send(data)
    @filter.command("膜拜")
    async def emoji3(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "膜拜")
        await event.send(data)
    @filter.command("咬")
    async def emoji4(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "咬")
        await event.send(data)
    @filter.command("可莉吃")
    async def emoji5(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "可莉吃")
        await event.send(data)
    @filter.command("吃掉")
    async def emoji6(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "吃掉")
        await event.send(data)
    @filter.command("捣")
    async def emoji7(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "捣")
        await event.send(data)
    @filter.command("咸鱼")
    async def emoji8(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "咸鱼")
        await event.send(data)
    @filter.command("玩")
    async def emoji9(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "玩")
        await event.send(data)
    @filter.command("舔")
    async def emoji10(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "舔")
        await event.send(data)
    @filter.command("拍")
    async def emoji11(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "拍")
        await event.send(data)
    @filter.command("丢")
    async def emoji12(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "丢")
        await event.send(data)
    @filter.command("撕")
    async def emoji13(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "撕")
        await event.send(data)
    @filter.command("求婚")
    async def emoji14(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "求婚")
        await event.send(data)
    @filter.command("爬")
    async def emoji15(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "爬")
        await event.send(data)
    @filter.command("你可能需要他")
    async def emoji16(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "你可能需要他")
        await event.send(data)
    @filter.command("想看")
    async def emoji17(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "想看")
        await event.send(data)
    @filter.command("点赞")
    async def emoji18(self, event: AstrMessageEvent):
        ids = emoji.parse_target(event)
        data = emoji.fetch_image(ids, "点赞")
        await event.send(data)
    @filter.on_decorating_result(priority=100)
    async def voice(self, event: AstrMessageEvent):
        result = event.get_result()
        texts = result.get_plain_text()
        room = event.get_group_id()
        res = MessageChain()
        res.chain = result.chain
        adapter_name = event.get_platform_name()
        if  not self.op:
            return
        if adapter_name == "qq_official":
            logger.info("检测为官方机器人，自动忽略转语音请求")
            return
        if not result.chain:
            logger.info(f"返回消息为空,pass")
            return
        if not result.is_llm_result():
            logger.info(f"非LLM消息,pass")
            return
        if room in self.rooms :
            logger.info(f"本群插件已关闭")
            return
        if self.flag:
            await event.send(res)
        logger.info(f"LLM返回的文本是：{texts}")
        result.chain.remove(Plain(texts))
        if self.flag2:
            texts = text.remove_complex_emoticons(texts)
            logger.info(f"过滤颜表情后的文本是：{texts}")
        text_chunks = [texts[i:i + 200] for i in range(0, len(texts), 200)]
        for chunk in text_chunks:
            result = music.generate_voice(chunk,"梅琳娜")
            await event.send(result)

    @filter.command("vits")
    async def switch(self, event: AstrMessageEvent):
        room  = event.get_group_id()
        chain1 = [Plain(f"本群插件已经启动（仅本群）"),Face(id=337)]
        chain2 = [Plain(f"本群插件已经关闭（仅本群）"),Face(id=337)]
        if room in self.rooms:
            self.rooms.remove(room)
            self.save_game()
            yield event.chain_result(chain1)
        else:
            self.rooms.append(room)
            self.save_game()
            yield event.chain_result(chain2)

    @filter.command("filter")
    async def filter_switch(self, event: AstrMessageEvent):
        chain1 = [Plain(f"过滤已经启动"),Face(id=337)]
        chain2 = [Plain(f"过滤已经关闭"),Face(id=337)]
        self.flag2 = not self.flag2
        if self.flag2:
            yield event.chain_result(chain1)
        else:
            yield event.chain_result(chain2)

    @filter.command("text")
    async def text_switch(self, event: AstrMessageEvent):
        user_id = event.get_sender_id()
        chain1 = [Plain(f"文本已经启动"),Face(id=337)]
        chain2 = [Plain(f"文本已经关闭"),Face(id=337)]
        self.flag = not self.flag
        if self.flag:
            yield event.chain_result(chain1)
        else:
            yield event.chain_result(chain2)

    @filter.command("gg")
    async def switch2(self, event: AstrMessageEvent):
        self.op = True
        chain1 = [Plain(f"TTS启动"), Face(id=337)]
        yield event.chain_result(chain1)
'''
    @llm_tool("Image_Recognition")
    async def trap1566(self, event: AstrMessageEvent, image_url: str) -> MessageEventResult:
        ''''''根据用户提供的图片URL进行图片识别，返回动漫相关信息。用户需要图片识别，提到有关图片识别时调用此工具。
        Args:
            image_url (string): 用户提供的图片URL，可以模糊判断
        ''''''
        data = self.image_recognition(image_url)
        result = event.make_result()
        result.chain = []
        if data and data.get("code") == 200:
            result.chain.append(Plain(f"中文标题: {data['data'].get('chinesetitle', 'N/A')}\n"))
            result.chain.append(Plain(f"原生标题: {data['data'].get('nativetitle', 'N/A')}\n"))
            result.chain.append(Plain(f"罗马音标题: {data['data'].get('romajititle', 'N/A')}\n"))
            result.chain.append(Plain(f"相似度: {data['data'].get('similarity', 'N/A')}\n"))
            result.chain.append(Image.fromURL(data['data'].get('img', 'N/A')))
            result.chain.append(Plain(f"视频链接: {data['data'].get('video', 'N/A')}\n"))
        else:
            result.chain.append(Plain("图片识别失败，请检查图片URL或稍后再试。"))
        return event.set_result(result)

    def image_recognition(self, image_url):
        # API地址
        url = "https://api.52vmy.cn/api/img/fan"

        # 请求参数
        params = {
            "url": image_url
        }

        try:
            # 发送GET请求
            response = requests.get(url, params=params)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()  # 解析返回的JSON数据

            if data.get("code") == 200:
                return data
            else:
                print(f"图片识别失败: {data.get('msg', '未知错误')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            return None
'''