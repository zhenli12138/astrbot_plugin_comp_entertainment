from astrbot.api.event import filter
from astrbot.api.all import *
from typing import (Dict, Any, Optional, AnyStr, Callable, Union, Awaitable,Coroutine)
import os
import json
from astrbot.api.provider import ProviderRequest
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
from data.plugins.astrbot_plugin_comp_entertainment.api_collection import daliya, ddz, deer, ai_make
from data.plugins.astrbot_plugin_comp_entertainment.api_collection import pilcreate
from data.plugins.astrbot_plugin_comp_entertainment.api_collection import api,emoji,image,text, search
from data.plugins.astrbot_plugin_comp_entertainment.api_collection import video, music,chess, blue_archive
from pathlib import Path
from typing import Dict, List
from astrbot.api.all import *
MESSAGE_BUFFER: Dict[str, List[dict]] = {}  # {group_id: [{"user_id": str, "messages": list}, ...]}
BUFFER_LIMIT = 2  # 一问一答的对话对数量
MERGE_TIMEOUT = 60  # 同一用户消息合并时间窗口（秒）

@register("astrbot_plugin_comp_entertainment", "达莉娅",
          "达莉娅群娱插件，60+超多功能集成调用插件，持续更新中，发【菜单】看菜单",
          "v2.1.0")
class CompEntertainment(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.deerpipe = deer.Deer()
        self.song_name = None
        # 文件路径配置
        self.ALLOWED_GROUPS_FILE = Path("./data/plugins/allowed_groups.jsonl")
        self.menu_path = "./data/plugins/menu_output.png"
        self.hashfile = "./data/plugins/menu.json"
        self.file_path = './data/plugins/vitsrooms.jsonl'
        self.ddzpath = './data/plugins/data.jsonl'
        # 菜单配置
        self.version = '210'
        self.hashs = ''
        if not os.path.exists(self.hashfile):
            self.save()
            print(f"文件 {self.hashfile} 不存在，已创建并初始化。")
        else:
            print(f"文件 {self.hashfile} 已存在，跳过创建。")
        self.load()
        # ddz配置
        self.rooms = {}  # {room_id: game}
        self.player_rooms = {}  # {player_id: room_id}
        if not os.path.exists(self.ddzpath):
            self.save_game()
            print(f"文件 {self.ddzpath} 不存在，已创建并初始化。")
        else:
            print(f"文件 {self.ddzpath} 已存在，跳过创建。")
        self.load_game()
        # 人工智障配置
        self.vitsrooms = []
        self.allowed_groups = self._load_allowed_groups()
        self.last_message_time: Dict[str, Dict[str, float]] = {}
        if not os.path.exists(self.file_path):
            self.save_rooms()
            print(f"文件 {self.file_path} 不存在，已创建并初始化。")
        else:
            print(f"文件 {self.file_path} 已存在，跳过创建。")
        self.load_rooms()
    '''菜单功能部分'''

    @filter.command("菜单")
    async def menu(self, event: AstrMessageEvent):
        new_hashs = await api.get_hash()
        new_version = await api.get_version()
        if not new_version:
            new_version = self.version
        if not new_hashs:
            new_hashs = self.hashs
        if new_hashs != self.hashs:
            self.hashs = new_hashs
            self.save()
            result = await api.get_menu(self.menu_path)
        else:
            result = MessageChain()
            result.chain = []
            result.chain = [Image.fromFileSystem(self.menu_path)]
        if new_version != self.version:
            res = MessageChain()
            old_version = f"v{self.version[0]}.{self.version[1]}.{self.version[2]}"
            new_version = f"v{new_version[0]}.{new_version[1]}.{new_version[2]}"
            res.chain = [Plain(f"提示：达莉娅综合群娱插件当前版本为{old_version}，最新版本为{new_version},请及时更新\n")]
            await event.send(res)
        await event.send(result)

    '''API功能部分'''

    @filter.command("光遇任务")
    async def trap0(self, event: AstrMessageEvent):
        result = await search.fetch_daily_tasks()
        await event.send(result)
    @filter.command("小姐姐视频")
    async def trap1(self, event: AstrMessageEvent):
        result = await video.xjj()
        await event.send(result)
    @filter.command("电影票房")
    async def trap2(self, event: AstrMessageEvent):
        result = await text.movie()
        await event.send(result)
    @filter.command("b站番剧")
    async def trap3(self, event: AstrMessageEvent,num:Optional[str] = '5'):
        result = await search.get_update_days(num)
        await event.send(result)
    @filter.command("cosplay")
    async def trap4(self, event: AstrMessageEvent):
        dat = await image.fetch_cosplay_data()
        result = MessageChain()
        result.chain = []
        try:
            for reg in dat:
                result.chain.append(reg)
                await event.send(result)
                result.chain = []
        except:
            await event.send(dat)
    @filter.command("翻译")
    async def trap5(self, event: AstrMessageEvent):
        msg = event.get_message_str()
        parts = msg.split(maxsplit = 1)
        result = await text.translate_text(parts[1])
        await event.send(result)
    @filter.command("随机段子")
    async def trap6(self, event: AstrMessageEvent):
        result = await text.get_random_text()
        await event.send(result)
    @filter.command("毒鸡汤")
    async def trap9(self, event: AstrMessageEvent):
        result = await text.get_dujitang()
        await event.send(result)
    @filter.command("搜狗搜图")
    async def trap7(self, event: AstrMessageEvent,a:str):
        result = await search.fetch_image_url(a)
        await event.send(result)
    @filter.command("天气")
    async def trap8(self, event: AstrMessageEvent,a:str):
        result = await search.get_weather(a)
        await event.send(result)
    @filter.command("头像框")
    async def trap10(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        result = await emoji.get_qq_avatar(ids)
        await event.send(result)
    @filter.command("小人举牌")
    async def trap11(self, event: AstrMessageEvent,a:str):
        result = await emoji.fetch_image_from_api(a)
        await event.send(result)
    @filter.command("音乐推荐")
    async def trap12(self, event: AstrMessageEvent):
        result,det= await music.get_music()
        voice = MessageChain()
        voice.chain.append(Record.fromURL(det))
        await event.send(voice)
        await event.send(result)
    @filter.command("随机原神")
    async def trap13(self, event: AstrMessageEvent):
        result = await image.call_api()
        await event.send(result)
    @filter.command("随机龙图")
    async def trap14(self, event: AstrMessageEvent):
        result = await image.call_api2()
        await event.send(result)
    @filter.command("温柔语录")
    async def trap15(self, event: AstrMessageEvent):
        result = await text.get_random_text2()
        await event.send(result)
    @filter.command("手写")
    async def trap16(self, event: AstrMessageEvent,a:str):
        result = await emoji.generate_image12(a)
        await event.send(result)
    @filter.command("塔罗牌")
    async def trap17(self, event: AstrMessageEvent):
        result = await image.get_tarot_reading()
        await event.send(result)
    @filter.command("随机生成超能力")
    async def trap18(self, event: AstrMessageEvent):
        result = await image.get_random_superpower()
        await event.send(result)
    @filter.command("网页截图")
    async def trap19(self, event: AstrMessageEvent, url: str):
        result = await image.get_webpage_screenshot(url)
        await event.send(result)
    @filter.command("emoji合成")
    async def trap20(self, event: AstrMessageEvent, emoji1: str, emoji2: str):
        result = await emoji.mix_emojis(emoji1, emoji2)
        await event.send(result)
    @filter.command("ikun图片")
    async def trap21(self, event: AstrMessageEvent, lx: str = "bqb"):
        result = await image.get_ikun_image(lx)
        await event.send(result)
    @filter.command("原神cosplay")
    async def trap22(self, event: AstrMessageEvent):
        result = await image.get_random_genshin_cosplay()
        await event.send(result)
    @filter.command("搜索音乐")
    async def trap23(self, event: AstrMessageEvent):
        msg = event.get_message_str()
        parts = msg.split(maxsplit = 2)
        song_name = parts[1]
        self.song_name = song_name
        result = await music.search_music(song_name)
        await event.send(result)
    @filter.command("音乐")
    async def trap24(self, event: AstrMessageEvent,n: int):
        result,det = await music.search_music(self.song_name, n)
        voice = MessageChain()
        voice.chain.append(Record.fromURL(det))
        await event.send(voice)
        await event.send(result)
    @filter.command("五子棋")
    async def trap25(self, event: AstrMessageEvent, types:str = '0', x: Optional[str] = None,y: Optional[str] = None):
        qq = event.get_sender_id()
        group = event.get_group_id()
        result = await chess.play_gobang(qq, group, types, x, y)
        await event.send(result)
    @filter.command("每日新闻")
    async def trap26(self, event: AstrMessageEvent):
        result = await image.get_daily_60s_news()
        await event.send(result)
    @filter.command("搜索b站视频")
    async def trap27(self, event: AstrMessageEvent, msg: str, n:Optional[str]= "1"):
        result,det = await video.search_bilibili_video(msg, n)
        voice = MessageChain()
        voice.chain.append(Video.fromURL(det))
        await event.send(voice)
        await event.send(result)
    @filter.command("百科查询")
    async def trap28(self, event: AstrMessageEvent, msg: str):
        result = await search.get_baike_info(msg)
        await event.send(result)
    @filter.command("电视剧排行榜")
    async def trap29(self, event: AstrMessageEvent):
        result = await text.get_tv_show_heat_ranking()
        await event.send(result)
    @filter.command("斗图")
    async def trap30(self, event: AstrMessageEvent, msg: str):
        result = await image.get_doutu_images(msg)
        await event.send(result)
    @filter.command("百度题库")
    async def trap31(self, event: AstrMessageEvent, question: str):
        result = await search.get_baidu_tiku_answer(question)
        await event.send(result)
    @filter.command("ba攻略")
    async def trap32(self, event: AstrMessageEvent,a: str):
        ba = blue_archive.Baarchive()
        result = await ba.handle_blue_archive(a)
        await event.send(result)
    @filter.command("网易云音乐解析")
    async def trap33(self, event: AstrMessageEvent,urls: str):
        result,det= await music.wyy_music_info(urls)
        voice = MessageChain()
        voice.chain.append(Record.fromURL(det))
        await event.send(voice)
        await event.send(result)
    '''表情包制作功能部分'''

    @filter.command("随机制作")
    async def emoji0(self, event: AstrMessageEvent,msg:Optional[str] = '',msg2:Optional[str] = ''):
        ids = await emoji.parse_target(event)
        ids2 = await emoji.parse_target2(event,ids)
        data = await emoji.fetch_image2(ids,ids2,msg,msg2)
        await event.send(data)
    @filter.command("摸头")
    async def emoji1(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "摸头")
        await event.send(data)
    @filter.command("感动哭了")
    async def emoji2(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "感动哭了")
        await event.send(data)
    @filter.command("膜拜")
    async def emoji3(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "膜拜")
        await event.send(data)
    @filter.command("咬")
    async def emoji4(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "咬")
        await event.send(data)
    @filter.command("可莉吃")
    async def emoji5(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "可莉吃")
        await event.send(data)
    @filter.command("吃掉")
    async def emoji6(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "吃掉")
        await event.send(data)
    @filter.command("捣")
    async def emoji7(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "捣")
        await event.send(data)
    @filter.command("咸鱼")
    async def emoji8(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "咸鱼")
        await event.send(data)
    @filter.command("玩")
    async def emoji9(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "玩")
        await event.send(data)
    @filter.command("舔")
    async def emoji10(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "舔")
        await event.send(data)
    @filter.command("拍")
    async def emoji11(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "拍")
        await event.send(data)
    @filter.command("丢")
    async def emoji12(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "丢")
        await event.send(data)
    @filter.command("撕")
    async def emoji13(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "撕")
        await event.send(data)
    @filter.command("求婚")
    async def emoji14(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "求婚")
        await event.send(data)
    @filter.command("爬")
    async def emoji15(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "爬")
        await event.send(data)
    @filter.command("你可能需要他")
    async def emoji16(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "你可能需要他")
        await event.send(data)
    @filter.command("想看")
    async def emoji17(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "想看")
        await event.send(data)
    @filter.command("点赞")
    async def emoji18(self, event: AstrMessageEvent):
        ids = await emoji.parse_target(event)
        data = await emoji.fetch_image(ids, "点赞")
        await event.send(data)

    '''鹿管功能部分'''

    @filter.command("钱包")
    async def get_currency(self, event: AstrMessageEvent):
        user_id = event.get_sender_id()
        currency = await deer.Deer.get_currency(self.deerpipe,user_id)
        result = MessageChain()
        result.chain = [Plain(f"您的鹿币金额为：{currency}")]
        await event.send(result)
    @filter.command("购买")
    async def buy(self, event: AstrMessageEvent, item_name: str):
        await deer.Deer.buy_item(self.deerpipe,event,item_name)
    @filter.command("使用")
    async def use(self, event: AstrMessageEvent, item_name: str):
        await deer.Deer.use_item(self.deerpipe, event, item_name)
    @filter.command("鹿")
    async def deer_sign_in(self, event: AstrMessageEvent):
        await deer.Deer.deer_sign_in(self.deerpipe, event)
    @filter.command("帮鹿")
    async def help_sign_in(self, event: AstrMessageEvent):
        await deer.Deer.help_sign_in(self.deerpipe, event)
    @filter.command("戴锁")
    async def toggle_lock(self, event: AstrMessageEvent):
        await deer.Deer.toggle_lock(self.deerpipe, event)
    @filter.command("看鹿")
    async def view_calendar(self, event: AstrMessageEvent):
        await deer.Deer.view_calendar(self.deerpipe, event)
    @filter.command("鹿榜")
    async def leaderboard(self, event: AstrMessageEvent):
        await deer.Deer.leaderboard(self.deerpipe, event)
    @filter.command("补鹿")
    async def resign(self, event: AstrMessageEvent, day: int):
        await deer.Deer.resign(self.deerpipe,event, day)
    @filter.command("戒鹿")
    async def cancel_sign_in(self, event: AstrMessageEvent, day: Optional[int] = None):
        await deer.Deer.cancel_sign_in(self.deerpipe, event, day)

    '''斗地主功能部分'''

    @filter.command("斗地主")
    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def ddz_menu(self, event: AstrMessageEvent):
        img = await pilcreate.generate_menu()
        result = MessageChain()
        result.chain = [Image.fromFileSystem(img)]
        yield event.image_result(img)
    @filter.command("结束游戏")
    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def exit_game(self,event: AstrMessageEvent):
        self.rooms,self.player_rooms = await ddz.exit_game(event,self.rooms,self.player_rooms)
        self.save_game()
    @filter.command("退出房间")
    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def exit_room(self, event: AstrMessageEvent):
        self.rooms,self.player_rooms = await ddz.exit_room(event,self.rooms,self.player_rooms)
        self.save_game()
    @filter.command("创建房间")
    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def create_room_cmd(self,event: AstrMessageEvent):
        self.rooms, self.player_rooms = await ddz.create_room(event, self.rooms, self.player_rooms)
        self.save_game()
    @filter.command("加入房间")
    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def join_room_cmd(self,event: AstrMessageEvent):
        self.rooms, self.player_rooms = await ddz.join_room(event, self.rooms, self.player_rooms)
        self.save_game()
    @filter.command("开始游戏")
    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def start_game(self,event: AstrMessageEvent):
        self.rooms, self.player_rooms = await ddz.start_game(event, self.rooms, self.player_rooms)
        self.save_game()
    @filter.command('不抢')
    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def process_bid1(self, event: AstrMessageEvent):
        self.rooms, self.player_rooms = await ddz.process_bid1(event, self.rooms, self.player_rooms)
        self.save_game()
    @filter.command('抢地主')
    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def process_bid2(self, event: AstrMessageEvent):
        self.rooms, self.player_rooms = await ddz.process_bid2(event, self.rooms, self.player_rooms)
        self.save_game()
    @filter.command('出牌')
    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def handle_play(self,event: AstrMessageEvent,cards_str:str):
        self.rooms, self.player_rooms = await ddz.handle_play(event,cards_str,self.rooms, self.player_rooms)
        self.save_game()
    @filter.command('pass')
    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def handle_pass(self,event: AstrMessageEvent):
        self.rooms, self.player_rooms = await ddz.handle_pass(event,self.rooms, self.player_rooms)
        self.save_game()

    '''人工智障功能部分'''

    @filter.command("人工智障")
    async def switch(self, event: AstrMessageEvent):
        room = event.get_group_id()
        chain1 = [Plain(f"本群插件已经启动（仅本群）"), Face(id=337)]
        chain2 = [Plain(f"本群插件已经关闭（仅本群）"), Face(id=337)]
        if room in self.vitsrooms:
            self.vitsrooms.remove(room)
            self.save_rooms()
            yield event.chain_result(chain2)
        else:
            self.vitsrooms.append(room)
            self.save_rooms()
            yield event.chain_result(chain1)

    @filter.command("开启收集")
    async def enable_collection(self, event: AstrMessageEvent):
        """启用当前群聊的消息收集"""
        if not event.message_obj.group_id:
            logger.warning("请在群聊中使用此命令")
            return

        self._save_group(event.message_obj.group_id, True)
        logger.warning("已开启本群消息收集")

    @filter.command("关闭收集")
    async def disable_collection(self, event: AstrMessageEvent):
        """禁用当前群聊的消息收集"""
        if not event.message_obj.group_id:
            yield event.plain_result("请在群聊中使用此命令")
            return

        self._save_group(event.message_obj.group_id, False)
        yield event.plain_result("已关闭本群消息收集")

    @filter.on_decorating_result(priority=101)
    async def ai_make(self, event: AstrMessageEvent):
        result = event.get_result()
        room = event.get_group_id()
        if not result.chain:
            logger.info(f"返回消息为空,pass")
            return
        if not result.is_llm_result():
            logger.info(f"非LLM消息,pass")
            return
        if room in self.vitsrooms:
            message_chain = []
            for component in event.message_obj.message:
                if isinstance(component, Plain):
                    message_chain.append({"type": "text", "content": component.text.strip()})
                '''
                elif isinstance(component, Image):
                    img_url = component.url if component.url.startswith("http") else component.file
                    message_chain.append({"type": "image", "file": img_url})
                '''
            text_contents = [item["content"] for item in message_chain if item.get("type") == "text"]
            try:
                for texts in text_contents:
                    component_text = await ai_make.ask_question(event, texts)
                    result = event.make_result()
                    result.message(component_text)
                    event.set_result(result)
            except Exception as e:
                return

    @event_message_type(EventMessageType.GROUP_MESSAGE)
    async def on_group_message(self, event: AstrMessageEvent):
        """处理群聊消息"""
        group_id = event.message_obj.group_id
        if group_id not in self.allowed_groups or group_id == '945041621':
            return

        message_chain = []
        for component in event.message_obj.message:
            if isinstance(component, Plain):
                message_chain.append({"type": "text", "content": component.text.strip()})
            '''
            elif isinstance(component, Image):
                img_url = component.url if component.url.startswith("http") else component.file
                message_chain.append({"type": "image", "file": img_url})
            '''
        # 在on_group_message中使用
        message_chain = await ai_make.merge_messages(message_chain)

        user_id = event.get_sender_id()
        timestamp = event.message_obj.timestamp

        # 初始化数据结构
        if group_id not in MESSAGE_BUFFER:
            MESSAGE_BUFFER[group_id] = []
        if group_id not in self.last_message_time:
            self.last_message_time[group_id] = {}

        # 合并同一用户连续消息
        last_time = self.last_message_time[group_id].get(user_id, 0)
        if timestamp - last_time < MERGE_TIMEOUT and MESSAGE_BUFFER[group_id]:
            last_entry = MESSAGE_BUFFER[group_id][-1]
            if last_entry["user_id"] == user_id:
                last_entry["messages"].extend(message_chain)
                self.last_message_time[group_id][user_id] = timestamp
                return

        # 添加新消息条目
        MESSAGE_BUFFER[group_id].append({
            "user_id": user_id,
            "messages": message_chain,
            "timestamp": timestamp
        })
        self.last_message_time[group_id][user_id] = timestamp

        # 处理消息队列
        await ai_make.process_group_buffer(group_id)

    def load_rooms(self):
        dicts = []
        with open(self.file_path, 'r') as f:
            for line in f:
                dicts.append(json.loads(line.strip()))
        # 分配到各自的字典
        if not dicts:  # 如果 dicts 为空
            logger.warning("加载的数据为空")
            return
        else:
            self.vitsrooms = dicts[0]
            return

    def save_rooms(self):
        with open(self.file_path, 'w') as f:
            f.write(json.dumps(self.vitsrooms) + '\n')

    def load_game(self):
        dicts = []
        with open(self.ddzpath, 'r') as f:
            for line in f:
                dicts.append(json.loads(line.strip()))
        # 分配到各自的字典
        if not dicts:  # 如果 dicts 为空
            logger.warning("加载的数据为空")
            return
        else:
            self.rooms = dicts[0]
            self.player_rooms = dicts[1]
            return

    def save_game(self):
        with open(self.ddzpath, 'w') as f:
            for d in [self.rooms, self.player_rooms]:
                f.write(json.dumps(d) + '\n')

    def load(self):
        if os.path.exists(self.hashfile):
            with open(self.hashfile, 'r', encoding='utf-8') as f:
                self.hashs = json.load(f)

    def save(self):
        with open(self.hashfile, 'w', encoding='utf-8') as f:
            json.dump(self.hashs, f, ensure_ascii=False, indent=4)
    def _load_allowed_groups(self) -> set:
        """从JSONL文件加载允许的群组列表"""
        allowed = set()
        if not self.ALLOWED_GROUPS_FILE.exists():
            return allowed

        with open(self.ALLOWED_GROUPS_FILE, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    data = json.loads(line.strip())
                    allowed.add(data["group_id"])
                except (json.JSONDecodeError, KeyError):
                    continue
        return allowed

    def _save_group(self, group_id: str, enable: bool):
        """更新群组权限并保存到文件"""
        if enable:
            with open(self.ALLOWED_GROUPS_FILE, "a", encoding="utf-8") as f:
                f.write(json.dumps({"group_id": group_id}) + "\n")
            self.allowed_groups.add(group_id)
        else:
            lines = []
            if self.ALLOWED_GROUPS_FILE.exists():
                with open(self.ALLOWED_GROUPS_FILE, "r", encoding="utf-8") as f:
                    for line in f:
                        try:
                            data = json.loads(line.strip())
                            if data.get("group_id") != group_id:
                                lines.append(line.strip())
                        except json.JSONDecodeError:
                            continue

            with open(self.ALLOWED_GROUPS_FILE, "w", encoding="utf-8") as f:
                f.write("\n".join(lines))
            self.allowed_groups.discard(group_id)
