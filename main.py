import urllib.request
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.all import *
import requests
from typing import List, Dict, Optional
import os
import json
from urllib.parse import quote
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.all import *
import os
from queue import Queue
import requests
from PIL import ImageDraw, ImageFont, ImageOps
from PIL import Image as PILImage

@register("astrbot_plugin_moreapi", "达莉娅",
          "自然语言进行各种api调用【/api】看菜单",
          "v1.4.0")
class MyPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.user_background_path = "./data/plugins/astrbot_plugin_moreapi/menu.png"
        self.flag = 0
        self.data = {}
        self.counter = 0
        self.enabled = True
        self.config = config
        self.base_url = "https://arona.diyigemt.com/api/v2/image"
        self.cdn_base = "https://arona.cdn.diyigemt.com/image"
        self.small_cdn_base = "https://arona.cdn.diyigemt.com/image/s"
        self.hash_file = "./data/plugins/astrbot_plugin_moreapi/hash.json"
        self.apt = "./data/plugins/astrbot_plugin_moreapi/"
        self.hash1 = {}
        #self.api_name = config.get('name', 'FunAudioLLM/CosyVoice2-0.5B')

    '''---------------------------------------------------'''
    '''---------------------------------------------------'''
    def generate_music(self,url):
        response = requests.get(url)
        # 检查请求是否成功
        if response.status_code == 200:
            # 保存音乐文件到本地
            with open("./data/plugins/astrbot_plugin_moreapi/music.mp3", "wb") as file:
                file.write(response.content)
            return "./data/plugins/astrbot_plugin_moreapi/music.mp3"
        else:
            print(f"下载失败，状态码: {response.status_code}")

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
    @llm_tool("api")
    async def menu(self, event: AstrMessageEvent)-> MessageEventResult:
        '''Send a list image of all API features available'''
        img = "./data/plugins/astrbot_plugin_moreapi/menu_output.png"
        result = event.make_result()
        result.chain = [Plain(f"MOREAPI菜单：\n"),Image.fromFileSystem(img)]
        return event.set_result(result)

    '''0---------------------------------------------------'''
    @llm_tool("Sky_Children_of_the_Light_mission")
    async def trap(self, event: AstrMessageEvent)-> MessageEventResult:
        '''发送光遇这个游戏的每日任务，当用户需要光遇任务，提到有关光遇，光遇任务时调用此工具'''
        data = self.fetch_daily_tasks()
        result = event.make_result()
        result.chain = [Plain(f"Nowtime: {data['nowtime']}\n")]
        # 打印每日任务
        for key, value in data.items():
            if key.isdigit():
                result.chain.append(Plain(f"Task {key}: {value[0]}"))
                result.chain.append(Image.fromURL(value[1]))
        return event.set_result(result)

    def fetch_daily_tasks(self):
        task_type = "rw"  # rw是每日任务
        # 接口地址
        url = "https://api.lolimi.cn/API/gy/"
        # 请求参数
        params = {
            'type': task_type
        }
        # 发送GET请求
        response = requests.get(url, params=params)
        # 检查请求是否成功
        if response.status_code == 200:
            try:
            # 解析返回的JSON数据
                data = response.json()
                return data
            except requests.exceptions.JSONDecodeError:
                print("Error: Response is not valid JSON.")
        else:
            logger.error(f"Failed to fetch data. Status code: {response.status_code}")

    '''1---------------------------------------------------'''
    @llm_tool("Little_Sister_Video")
    async def trap1(self, event: AstrMessageEvent)-> MessageEventResult:
        '''发送小姐姐视频/美女视频/抖音视频，当用户需要小姐姐视频，提到有关小姐姐，美女视频，小姐姐视频时调用此工具'''
        data = self.xjj()
        if self.flag == 1:
            result = event.make_result()
            result.chain = [Video.fromURL(data.get('download_url'))]
            return event.set_result(result)
        elif self.flag == 2:
            result = event.make_result()
            result.chain = [Video.fromFileSystem(data)]
            return event.set_result(result)
        else:
            result2 = event.make_result()
            result2.chain = [Plain(f"请求失败！\n")]
            return event.set_result(result2)

    def xjj(self):
        api_url = "https://api.kxzjoker.cn/API/Beautyvideo.php"
        params = {
            'type': 'json'
        }
        try:
            response = requests.get(api_url, params=params)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()  # 解析JSON数据
            self.flag = 1
            return data
        except requests.exceptions.RequestException as e:
            print(f"请求出错: {e}")

        url = "https://api.lolimi.cn/API/xjj/xjj.php"
        # 发送GET请求
        response = requests.get(url)
        # 检查请求是否成功
        if response.status_code == 200:
            data = response.content
            self.flag = 2
            with open(f"./data/plugins/astrbot_plugin_moreapi/xjj.mp4", "wb") as file:
                file.write(data)
            return f"./data/plugins/astrbot_plugin_moreapi/xjj.mp4"
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None
    '''2---------------------------------------------------'''
    @llm_tool("box_office")
    async def trap2(self, event: AstrMessageEvent)-> MessageEventResult:
        '''发送电影票房排行榜单,当用户需要电影票房排行榜单，提到有关电影票房时调用此工具'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.movie()
        if os.path.exists(data):
            with open(data, 'r',encoding="utf-8") as file:
                text = file.read()
        result = event.make_result()
        result.chain = [Plain(text)]
        return event.set_result(result)
    def movie(self):
        # 接口地址
        url = "https://api.lolimi.cn/API/piao/dy.php"
        # 发送GET请求
        response = requests.get(url)
        if response.status_code == 200:
            data = response.content
            with open(f"./data/plugins/astrbot_plugin_moreapi/movie.txt", "wb") as file:
                file.write(data)
            return f"./data/plugins/astrbot_plugin_moreapi/movie.txt"
        else:
            print(f"请求失败，状态码: {response.status_code}")

    '''3---------------------------------------------------'''
    @llm_tool("Bilibili_Drama_Update_Table")
    async def trap3(self, event: AstrMessageEvent,num:str)-> MessageEventResult:
        '''发送b站番剧更新表，当用户需要番剧更新列表，提到有关番剧，动画，动漫，b站番剧更新表或b站番剧时调用此工具
            Args:num(string): 用户需要发送的数量，如果用户没有明确指出，请设置为为5
        '''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        if not num:
            num = 5
        data = self.get_update_days(num)
        result = event.make_result()

        result.chain = []
        if data:
            for item in data:
                result.chain.append(Plain(f"Name: {item['Name']}\n"))
                result.chain.append(Image.fromURL(item['Picture']))
                result.chain.append(Plain(f"Update: {item['Update']}\n"))
                result.chain.append(Plain(f"Time: {item['Time']}\n"))
                result.chain.append(Plain(f"Url: {item['Url']}\n"))
                result.chain.append(Plain("------------------\n"))
        return event.set_result(result)

    def get_update_days(self,num):
        url = "https://api.lolimi.cn/API/B_Update_Days/api.php"
        return_type = 'json'
        params = {
            'num': num,
            'type': return_type
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = response.json()
            if data['code'] == 1:
                return data['data']
            else:
                print(f"Error: {data['text']}")
                return
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return
    '''4---------------------------------------------------'''
    @llm_tool("cosplay_image")
    async def trap4(self, event: AstrMessageEvent)-> MessageEventResult:
        '''发送cosplay图片,当用户需要cosplay图片，提到有关cosplay图片，cosplay时调用此工具'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.fetch_cosplay_data()
        result = event.make_result()
        title = data["data"]["Title"]
        image_urls = data["data"]["data"]
        result.chain = [Plain(f"标题: {title}\n")]
        for url in image_urls:
            result.chain.append(Image.fromURL(url))
        return event.set_result(result)
    def fetch_cosplay_data(self):
        # API地址
        url = "https://api.lolimi.cn/API/cosplay/api.php"
        # 请求参数
        params = {
            "type": "json"  # 可以改为 "text" 或 "image" 根据需求
        }
        try:
            # 发送GET请求
            response = requests.get(url, params=params)
            # 检查请求是否成功
            if response.status_code == 200:
                # 解析返回的JSON数据
                data = response.json()
                # 检查返回的状态码
                if data.get("code") == "1":
                    return data

                else:
                    print(f"获取失败: {data.get('text')}")
            else:
                print(f"请求失败，状态码: {response.status_code}")
        except requests.exceptions.RequestException as e:
            print(f"请求出错: {e}")

    '''5---------------------------------------------------'''
    @llm_tool("translate")
    async def trap5(self, event: AstrMessageEvent,a:str)-> MessageEventResult:
        '''翻译用户提供的内容文字（翻译为英文）,当用户需要翻译，提到有关翻译什么时调用此工具
        Args:a(string): 用户提供的内容文字（即需要翻译的内容），可以模糊判断
        '''
        data = self.translate_text(a)
        result = event.make_result()
        result.chain = [Plain(f"翻译结果：{data}")]
        return event.set_result(result)
    def translate_text(self,msg):
        # 接口地址
        url = "https://api.lolimi.cn/API/qqfy/api.php"
        output_format = 'json'
        # 请求参数
        params = {
            'msg': msg,
            'type': output_format
        }
        # 发送GET请求
        response = requests.get(url, params=params)
        # 检查请求是否成功
        if response.status_code == 200:
            # 根据返回格式处理响应
            if output_format == 'json':
                data = response.json()
                return data['text']# 返回JSON格式的数据
            else:
                return response.text  # 返回纯文本格式的数据
        else:
            return f"请求失败，状态码: {response.status_code}"
    '''6---------------------------------------------------'''
    @llm_tool("Random_paragraph")
    async def trap6(self, event: AstrMessageEvent)-> MessageEventResult:
        '''发送一段随机的段子，当用户需要段子，提到有关段子，随即段子时调用此工具'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.get_random_text()
        result = event.make_result()
        result.chain = [Plain(f"随机段子：{data}")]
        return event.set_result(result)
    def get_random_text(self):
        url = "https://api.lolimi.cn/API/yiyan/dz.php"
        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            return response.text
        except requests.exceptions.RequestException as e:
            return f"请求失败: {e}"
    '''7---------------------------------------------------'''
    @llm_tool("Search_for_pictures")
    async def trap7(self, event: AstrMessageEvent,a:str)-> MessageEventResult:
        '''对用户给出的关键词使用搜狗搜索引擎进行搜图操作，当用户需要搜图，提到有关搜索什么图片时调用此工具
        Args:a(string): 用户给出的关键词或用户提到的文字内容，可以模糊判断'''
        data = self.fetch_image_url(a)
        result = event.make_result()
        result.chain = [Plain(f"{a}搜图结果:\n"), Image.fromURL(data)]
        return event.set_result(result)
    def fetch_image_url(self,search_term):
        # API接口地址
        url = "https://api.lolimi.cn/API/sgst/api.php"
        response_type = 'json'
        # 请求参数
        params = {
            'msg': search_term,
            'type': response_type
        }
        # 发送GET请求
        response = requests.get(url, params=params)
        # 检查请求是否成功
        if response.status_code == 200:
            # 解析返回的JSON数据
            data = response.json()
            # 检查状态码
            if data.get('code') == 1:
                # 获取图片链接
                image_url = data['data']['url']
                print(f"获取成功，图片链接: {image_url}")
                return image_url
            else:
                print(f"获取失败: {data.get('text')}")
        else:
            print(f"请求失败，状态码: {response.status_code}")
    '''8---------------------------------------------------'''
    @llm_tool("weather")
    async def trap8(self, event: AstrMessageEvent,a:str)-> MessageEventResult:
        '''查询用户给出的地点的天气情况，当用户需要什么地方的天气，提到有关天气时调用此工具
        Args:a(string): 用户给出的地点，如北京/上海/重庆/深圳，等等，可以模糊判断'''
        data = self.get_weather(a)
        result = event.make_result()
        result.chain = []
        if isinstance(data, dict):
            result.chain.append(Plain(f"Weather Data for {data.get('city')}\n"))
            result.chain.append(Plain(f"Temperature: {data.get('temp')}\n"))
            result.chain.append(Plain(f"Weather: {data.get('weather')}\n"))
            result.chain.append(Plain(f"Wind: {data.get('wind')}\n"))
            result.chain.append(Plain(f"Wind Speed: {data.get('windSpeed')}\n"))
        else:
            print(data)
        return event.set_result(result)
    def get_weather(self,city):
        # API地址
        url = "https://api.lolimi.cn/API/weather/api.php"
        # 请求参数
        params = {
            "city": city,
            "type": "json"  # 指定返回格式为JSON
        }
        try:
            # 发送GET请求
            response = requests.get(url, params=params)
            # 检查请求是否成功
            if response.status_code == 200:
                # 解析JSON响应
                data = response.json()
                # 检查返回的状态码
                if data.get("code") == 1:
                    # 获取成功，返回数据
                    return data.get("data")
                else:
                    # 获取失败，返回错误信息
                    return f"Error: {data.get('text')}"
            else:
                # 请求失败，返回状态码
                return f"Request failed with status code: {response.status_code}"
        except Exception as e:
            # 捕获异常并返回错误信息
            return f"An error occurred: {str(e)}"
    '''9---------------------------------------------------'''
    @llm_tool("Poisonous_Chicken_Soup")
    async def trap9(self, event: AstrMessageEvent)-> MessageEventResult:
        '''发送一段毒鸡汤文字内容，用户需要毒鸡汤，提到有关毒鸡汤时调用此工具'''
        data = self.get_dujitang()
        result = event.make_result()
        result.chain = [Plain(f"毒鸡汤：{data}")]
        return event.set_result(result)
    def get_dujitang(self):
        url = "https://api.lolimi.cn/API/du/api.php"
        params = {
            "type": "json"  # 你可以根据需要选择返回格式，这里选择json
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()  # 解析返回的JSON数据

            if data.get("code") == "1":
                return data.get("text")
            else:
                return "Failed to retrieve dujitang."

        except requests.exceptions.RequestException as e:
            return f"An error occurred: {e}"
    '''---------------------------------------------------'''
    @llm_tool("Avatar_Frame")
    async def trap10(self, event: AstrMessageEvent)-> MessageEventResult:
        '''发送一张头像框图片，用户需要制作头像框，提到有关头像框时调用此工具'''
        id = self.parse_target(event)
        data = self.get_qq_avatar(id)
        result = event.make_result()
        result.chain = [Image.fromFileSystem(data)]
        return event.set_result(result)
    def get_qq_avatar(self,qq_number):
        # API地址
        url = "https://api.lolimi.cn/API/head/api.php"

        # 请求参数
        params = {
            "QQ": qq_number
        }

        # 发送GET请求
        response = requests.get(url, params=params)

        # 检查请求是否成功
        if response.status_code == 200:
            image_data = response.content
            with open(f"./data/plugins/astrbot_plugin_moreapi/pet.jpg", "wb") as file:
                file.write(image_data)
            return f"./data/plugins/astrbot_plugin_moreapi/pet.jpg"
        else:
            print(f"请求失败，状态码: {response.status_code}")
    def parse_target(self, event):
        """解析@目标或用户名"""
        for comp in event.message_obj.message:
            if isinstance(comp, At) and event.get_self_id() != str(comp.qq):
                return str(comp.qq)

    '''---------------------------------------------------'''
    @llm_tool("Little_person_holding_a_sign")
    async def trap11(self, event: AstrMessageEvent,a:str)-> MessageEventResult:
        '''根据用户要求的文字内容发送一张小人举牌图片，用户需要小人举牌图片，提到有关小人举牌，小人举牌图片，举牌时调用此工具
        Args:a(string): 用户提到的文字内容，可以模糊判断'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.fetch_image_from_api(a)
        result = event.make_result()
        result.chain = [Image.fromFileSystem(data)]
        return event.set_result(result)
    def fetch_image_from_api(self,msg):
        # API地址
        url = "https://api.lolimi.cn/API/pai/api.php"

        # 请求参数
        params = {
            'msg': msg
        }

        # 发送GET请求
        response = requests.get(url, params=params)

        # 检查请求是否成功
        if response.status_code == 200:
            # 将返回的图片内容保存到本地
            image_data = response.content
            with open(f"./data/plugins/astrbot_plugin_moreapi/pe.png", "wb") as file:
                file.write(image_data)
            return f"./data/plugins/astrbot_plugin_moreapi/pe.png"
        else:
            print(f"请求失败，状态码: {response.status_code}")
    '''---------------------------------------------------'''
    @llm_tool("Music_recommendation")
    async def trap12(self, event: AstrMessageEvent)-> MessageEventResult:
        '''给用户发送音乐推荐内容，用户需要音乐推荐，提到有关音乐推荐，音乐时调用此工具'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.get_music()
        det = self.generate_music(data['data'].get('Url', 'N/A'))
        result = event.make_result()
        result.chain = []
        # 拼接字符串
        result.chain.append(Plain(f"Music: {data['data'].get('Music', 'N/A')}\n"))
        result.chain.append(Plain(f"Name: {data['data'].get('name', 'N/A')}\n"))
        result.chain.append(Image.fromURL(data['data'].get('Picture', 'N/A')))
        result.chain.append(Plain(f"ID: {data['data'].get('id', 'N/A')}\n"))
        result.chain.append(Plain(f"Content: {data['data'].get('Content', 'N/A')}\n"))
        result.chain.append(Plain(f"Nick: {data['data'].get('Nick', 'N/A')}\n"))
        voice = MessageChain()
        voice.chain.append(Record(file=det))
        await event.send(voice)
        return event.set_result(result)
    def get_music(self):
        url = "https://api.lolimi.cn/API/wyrp/api.php"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data
    '''---------------------------------------------------'''
    @llm_tool("Random_Genshin_Impact_pictures")
    async def trap13(self, event: AstrMessageEvent)-> MessageEventResult:
        '''发送一张随机的关于原神的图片，用户需要原神图片，提到有关原神图片，原神时调用此工具'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.call_api()
        result = event.make_result()
        result.chain = [Image.fromURL(data)]
        # 将结果添加到 chain 中
        return event.set_result(result)
    def call_api(self):
        # 接口地址
        url = "https://api.lolimi.cn/API/yuan/api.php"

        # 请求参数
        params = {
            "type": "json"  # 可以根据需要修改为 "text" 或 "image"
        }

        # 发送GET请求
        response = requests.get(url, params=params)

        # 检查请求是否成功
        if response.status_code == 200:
            # 解析返回的JSON数据
            data = response.json()
            return data.get("text")
        else:
            print("请求失败，状态码:", response.status_code)
    '''---------------------------------------------------'''
    @llm_tool("Random_Dragon_Chart")
    async def trap14(self, event: AstrMessageEvent)-> MessageEventResult:
        '''发送一张随机的‘龙图‘，用户需要龙图，提到有关龙图时调用此工具’'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.call_api2()
        result = event.make_result()
        result.chain = [Image.fromFileSystem(data)]
        return event.set_result(result)
    def call_api2(self):
        # 接口地址
        url = "https://api.lolimi.cn/API/longt/l.php"
        # 发送GET请求
        response = requests.get(url)
        if response.status_code == 200:
            # 将返回的图片内容保存到本地
            image_data = response.content
            with open(f"./data/plugins/astrbot_plugin_moreapi/p.png", "wb") as file:
                file.write(image_data)
            return f"./data/plugins/astrbot_plugin_moreapi/p.png"
        else:
            print(f"请求失败，状态码: {response.status_code}")

    '''---------------------------------------------------'''
    @llm_tool("Gentle_quotes")
    async def trap15(self, event: AstrMessageEvent)-> MessageEventResult:
        '''发送一段温柔语录的文字内容，用户需要温柔语录，提到有关温柔语录时调用此工具'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.get_random_text2()
        result = event.make_result()
        result.chain = [Plain(f"温柔语录：{data}")]
        return event.set_result(result)
    def get_random_text2(self):
        url = "https://api.lolimi.cn/API/wryl/api.php"
        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            return response.text
        except requests.exceptions.RequestException as e:
            return f"请求失败: {e}"
    '''---------------------------------------------------'''
    @llm_tool("Handwritten_text_to_images")
    async def trap114(self, event: AstrMessageEvent,a:str)-> MessageEventResult:
        '''根据用户提到的文字内容发送一张手写的该文字内容的图片，用户需要手写图片，提到有关手写图片，手写时调用此工具
        Args:a(string): 用户提到的文字内容，可以模糊判断'''
        data = self.generate_image12(a)
        result = event.make_result()
        result.chain = [Image.fromFileSystem(data)]
        return event.set_result(result)

    def generate_image12(self, prompt):
        url = "https://api.52vmy.cn/api/img/tw"

        # 请求参数
        params = {
            "msg": prompt
        }

        # 发送GET请求
        response = requests.get(url, params=params)

        # 检查请求是否成功
        if response.status_code == 200:
            # 保存返回的图片
            with open(f"./data/plugins/astrbot_plugin_moreapi/pu.png", "wb") as file:
                file.write(response.content)
            return f"./data/plugins/astrbot_plugin_moreapi/pu.png"
        else:
            print(f"请求失败，状态码: {response.status_code}")

    '''---------------------------------------------------'''

    @llm_tool("ai_drawing")
    async def trap112(self, event: AstrMessageEvent,a:str)-> MessageEventResult:
        '''根据用户提供的关键词发送一张根据关键词的ai绘图的图片，用户需要ai绘图，画一张图，提到有关ai绘图，画一张图时调用此工具
        Args:a(string): 用户提到的关键词，可以模糊判断'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.generate_imageai(a)
        result = event.make_result()
        result.chain = []
        if data:
            result.chain.append(Plain(f"绘画词: {data['prompt']}\n"))
            result.chain.append(Image.fromURL(data['imgurl']))
        return event.set_result(result)
    def generate_imageai(self,prompt):
        # API地址
        model = "normal"
        url = "https://api.pearktrue.cn/api/stablediffusion/"

        # 请求参数
        params = {
            "prompt": prompt,
            "model": model
        }

        try:
            # 发送GET请求
            response = requests.get(url, params=params)

            # 检查请求是否成功
            if response.status_code == 200:
                # 解析返回的JSON数据
                data = response.json()

                if data["code"] == 200:
                    print("AI绘画成功！")
                    return data
                else:
                    print(f"请求失败: {data['msg']}")
            else:
                print(f"请求失败，状态码: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
    '''---------------------------------------------------'''

    @llm_tool("Random_Superpower")
    async def trapa1544(self, event: AstrMessageEvent) -> MessageEventResult:
        '''随机生成超能力及其副作用，用户需要随机超能力，提到有关超能力时调用此工具'''
        data = self.get_random_superpower()
        result = event.make_result()
        result.chain = []
        if data:
            result.chain.append(Plain(f"超能力: {data.get('superpower', 'N/A')}\n"))
            result.chain.append(Plain(f"副作用: {data.get('sideeffect', 'N/A')}\n"))
            result.chain.append(Image.fromURL(data.get('image_url', 'N/A')))
        else:
            result.chain.append(Plain("获取超能力失败，请稍后再试。"))
        return event.set_result(result)

    def get_random_superpower(self):
        # API地址
        url = "https://api.pearktrue.cn/api/superpower/"

        try:
            # 发送GET请求
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()  # 解析返回的JSON数据

            if data.get("code") == 200:
                return data
            else:
                print(f"获取失败: {data.get('msg', '未知错误')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            return None
    '''--------------------------------------------'''

    @llm_tool("Daily_60s_News")
    async def trap11237(self, event: AstrMessageEvent) -> MessageEventResult:
        '''获取每日60秒早报，用户需要每日新闻，提到有关60秒早报,早报，新闻，每日新闻时调用此工具'''
        data = self.get_daily_60s_news()
        result = event.make_result()
        result.chain = []
        if data:
            result.chain.append(Image.fromFileSystem(data))
        else:
            result.chain.append(Plain("获取每日60秒早报失败，请稍后再试。"))

        return event.set_result(result)

    def get_daily_60s_news(self):
        # API地址
        url = "https://api.52vmy.cn/api/wl/60s"

        # 请求参数
        params = {'id': 21}

        try:
            # 发送GET请求
            response = requests.get(url, params=params)
            response.raise_for_status()  # 检查请求是否成功
                # 默认返回图片，保存到本地
            image_data = response.content
            output_path = f"./data/plugins/astrbot_plugin_moreapi/daily_60s_news.png"
            with open(output_path, "wb") as file:
                file.write(image_data)
            return output_path
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            return None

    @llm_tool("Bilibili_Video_Search")
    async def trap17453(self, event: AstrMessageEvent, msg: str, n: str = "1") -> MessageEventResult:
        '''根据用户提供的关键词搜索B站视频，用户需要搜索B站视频，提到有关搜索B站视频，B站视频时调用此工具
        Args:
            msg (string): 用户提供的关键词，如“少年”
            n (string): 返回结果的序号，默认为1
        '''
        data = self.search_bilibili_video(msg, n)
        result = event.make_result()
        result.chain = []
        if data:
            result.chain.append(Plain(f"标题: {data.get('title', 'N/A')}\n"))
            result.chain.append(Plain(f"UP主: {data.get('user', 'N/A')}\n"))
            result.chain.append(Image.fromURL(data.get('img_url', 'N/A')))
            voice = MessageChain()
            voice.chain.append(Video.fromURL(data.get('url', 'N/A')))
            await event.send(voice)
        else:
            result.chain.append(Plain("未找到相关视频，请尝试其他关键词。"))
        return event.set_result(result)

    def search_bilibili_video(self, msg: str, n: str = "1"):
        # API地址
        url = "https://api.52vmy.cn/api/query/bilibili/video"
        # 请求参数
        params = {
            "msg": msg,
            "n": n
        }
        try:
            # 发送GET请求
            response = requests.get(url, params=params)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()  # 解析返回的JSON数据

            if data:
                return data
            else:
                print("未找到相关视频。")
                return None
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            return None

    @llm_tool("Baike_Search")
    async def trap178907(self, event: AstrMessageEvent, msg: str) -> MessageEventResult:
        '''根据用户提供的关键词查询百科内容，用户需要百科查询，需要查询什么具体的事务，提到有关百科，或者查询什么东西时调用此工具
        Args:msg(string): 用户提供的关键词，可以模糊判断'''
        data = self.get_baike_info(msg)
        result = event.make_result()
        result.chain = []
        if data and data.get("code") == 200:
            result.chain.append(Plain(f"百科内容: {data['data'].get('text', 'N/A')}\n"))
            if data['data'].get('img_url'):
                result.chain.append(Image.fromURL(data['data']['img_url']))
            if data['data'].get('url'):
                result.chain.append(Plain(f"更多信息请访问: {data['data']['url']}"))
        else:
            result.chain.append(Plain("百科查询失败，请稍后再试。"))
        return event.set_result(result)

    def get_baike_info(self, msg):
        # API地址
        url = "https://api.52vmy.cn/api/query/baike"

        # 请求参数
        params = {
            "msg": msg,
            "type": "json"  # 默认返回JSON格式
        }

        try:
            # 发送GET请求
            response = requests.get(url, params=params)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()  # 解析返回的JSON数据

            if data.get("code") == 200:
                return data
            else:
                print(f"获取失败: {data.get('msg', '未知错误')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            return None

    @llm_tool("TV_Show_Heat_Ranking")
    async def trap1565567(self, event: AstrMessageEvent) -> MessageEventResult:
        '''获取当前电视剧热度排行榜，用户需要电视剧排行榜，提到有关电视剧热度，电视剧排行，电视剧时调用此工具'''
        data = self.get_tv_show_heat_ranking()
        result = event.make_result()
        result.chain = []
        if data:
            result.chain.append(Plain("当前电视剧热度排行榜：\n"))
            result.chain.append(Plain(data))
        else:
            result.chain.append(Plain("获取电视剧热度排行榜失败，请稍后再试。"))
        return event.set_result(result)

    def get_tv_show_heat_ranking(self)->str:
        # API地址
        url = "https://api.52vmy.cn/api/wl/top/tv"
        # 请求参数
        params = {
            "type": "text"  # 默认返回JSON格式
        }
        try:
            # 发送GET请求
            response = requests.get(url,params=params)
            data = response
            return data
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            return ''

    @llm_tool("Random_Doutu")
    async def trap17656(self, event: AstrMessageEvent, msg: str) -> MessageEventResult:
        '''根据用户提供的关键词发送一组斗图/表情包图片，用户需要斗图，需要表情包，提到有关斗图，表情包时调用此工具
        Args:msg(string): 用户提供的关键词，可以模糊判断'''
        data = self.get_doutu_images(msg)
        result = event.make_result()
        result.chain = []
        if data:
            result.chain.append(Plain(f"关键词: {msg}\n"))
            for item in data:
                result.chain.append(Plain(f"标题: {item['title']}\n"))
                result.chain.append(Image.fromURL(item['url']))
        else:
            result.chain.append(Plain("获取斗图失败，请稍后再试。"))
        return event.set_result(result)

    def get_doutu_images(self, msg):
        # API地址
        url = "https://api.52vmy.cn/api/wl/doutu"

        # 请求参数
        params = {
            "msg": msg,
            "type": "json"  # 默认返回JSON格式
        }

        try:
            # 发送GET请求
            response = requests.get(url, params=params)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()  # 解析返回的JSON数据

            if data.get("code") == 201:
                return data.get("data", [])
            else:
                print(f"获取失败: {data.get('msg', '未知错误')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            return None

    @llm_tool("Image_Recognition")
    async def trap1566(self, event: AstrMessageEvent, image_url: str) -> MessageEventResult:
        '''根据用户提供的图片URL进行图片识别，返回动漫相关信息。用户需要图片识别，提到有关图片识别时调用此工具。
        Args:
            image_url (string): 用户提供的图片URL，可以模糊判断
        '''
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

    @llm_tool("Baidu_Tiku")
    async def trap1111237(self, event: AstrMessageEvent, question: str) -> MessageEventResult:
        '''通过用户输入的问题对接百度题库进行回答，用户需要查询问题答案，提到有关题库、百度题库时调用此工具
        Args:
            question (string): 用户输入的问题，可以模糊判断
        '''
        data = self.get_baidu_tiku_answer(question)
        result = event.make_result()
        result.chain = []
        if data and data.get("code") == 200:
            result.chain.append(Plain(f"问题: {data['data'].get('question', 'N/A')}\n"))
            result.chain.append(Plain(f"选项: {', '.join(data['data'].get('options', []))}\n"))
            result.chain.append(Plain(f"答案: {data['data'].get('answer', 'N/A')}\n"))
        else:
            result.chain.append(Plain("查询失败，请稍后再试或检查问题是否正确。"))
        return event.set_result(result)

    def get_baidu_tiku_answer(self, question):
        # API地址
        url = "https://api.pearktrue.cn/api/baidutiku/"

        # 请求参数
        params = {
            "question": question
        }

        try:
            # 发送GET请求
            response = requests.get(url, params=params)
            response.raise_for_status()  # 检查请求是否成功
            data = response.json()  # 解析返回的JSON数据

            if data.get("code") == 200:
                return data
            else:
                print(f"查询失败: {data.get('msg', '未知错误')}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"请求异常: {e}")
            return None
    @llm_tool("Blue_Archive_Strategy_Search")
    async def handle_blue_archive(self, event: AstrMessageEvent,text:str)-> MessageEventResult:
        '''根据用户提供的关键词进行碧蓝档案攻略查询，用户需要什么的碧蓝档案攻略，ba攻略，攻略，提到有关碧蓝档案攻略，ba攻略，攻略时调用此工具
        Args:text(string): 用户提供的关键词，比如‘国际服，可以模糊识别’'''
        self.load_game()
        params = {
            "name": text,
            "size": 8,
            "method": 3  # 默认使用混合搜索
        }
        api_data = {}
        result = event.make_result()
        result.chain = []
        # 调用API
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            api_data = response.json()
        except Exception as e:
            result.chain = [Plain(f"API请求异常：{str(e)}")]
            return event.set_result(result)

        if not api_data:
            result.chain = [Plain("攻略查询服务暂不可用，请稍后再试")]

        if api_data["code"] == 200:
            # 精确匹配
            results = self.process_results(api_data["data"])
            if results:
                best_match = results[0]
                result.chain.append(Plain(f"找到精确匹配：{best_match['name']}\n"))
                if best_match["type"] == "image":
                    oldhash = self.hash1.get(best_match['name'], '')
                    local_path = best_match["file"]
                    if best_match["hash"] == oldhash and os.path.exists(local_path):
                        result.chain.append(Image.fromFileSystem(local_path))
                    else:
                        url = best_match["urls"]
                        # 对 URL 中的路径部分进行编码
                        parsed_url = urllib.parse.urlsplit(url)
                        encoded_path = quote(parsed_url.path)  # 编码路径部分
                        safe_url = urllib.parse.urlunsplit(
                            (parsed_url.scheme, parsed_url.netloc, encoded_path, parsed_url.query, parsed_url.fragment)
                        )
                        with urllib.request.urlopen(safe_url) as resp:
                            data = resp.read()
                        with open(local_path, "wb") as f:
                            f.write(data)
                        self.hash1[best_match['name']] = best_match['hash']
                        self.save_game()
                        result.chain.append(Image.fromURL(best_match["urls"]))  # 使用小图
                else:
                    result.chain.append(Plain(best_match["content"]))
        elif api_data["code"] == 101:
            # 模糊查询
            if not api_data["data"]:
                result.chain = [Plain("没有找到相关攻略")]
            results = self.process_results(api_data["data"])
            result.chain.append(Plain("找到以下相似结果：\n"))
            for idx, item in enumerate(results, 1):
                result.chain.append(Plain(f"{idx}. {item['name']}\n"))
                if item["type"] == "image":
                    oldhash = self.hash1.get(item['name'], '')
                    local_path = item["file"]
                    if item["hash"] == oldhash and os.path.exists(local_path):
                        result.chain.append(Image.fromFileSystem(local_path))
                    else:
                        url = item["urls"]
                        # 对 URL 中的路径部分进行编码
                        parsed_url = urllib.parse.urlsplit(url)
                        encoded_path = quote(parsed_url.path)  # 编码路径部分
                        safe_url = urllib.parse.urlunsplit(
                            (parsed_url.scheme, parsed_url.netloc, encoded_path, parsed_url.query, parsed_url.fragment)
                        )
                        with urllib.request.urlopen(safe_url) as resp:
                            data = resp.read()
                        with open(local_path, "wb") as f:
                            f.write(data)
                        self.hash1[item['name']] = item["hash"]
                        self.save_game()
                        result.chain.append(Image.fromURL(item["urls"]))  # 使用小图
                else:
                    result.chain.append(Plain(item["content"] + "\n"))
                result.chain.append(Plain("-" * 20 + "\n"))
            result.chain.append(Plain("请输入更精确的名称获取具体内容"))
        else:
            result.chain = [Plain(f"查询失败：{api_data.get('message', '未知错误')}")]
        return event.set_result(result)

    def load_game(self):
        if os.path.exists(self.hash_file):
            with open(self.hash_file, 'r', encoding='utf-8') as f:
                self.hash1 = json.load(f)

    def save_game(self):
        with open(self.hash_file, 'w', encoding='utf-8') as f:
            json.dump(self.hash1, f, ensure_ascii=False, indent=4)

    def process_results(self, data: List[Dict]) -> List[Dict]:
        """处理API返回结果"""
        processed = []
        for item in data:
            if item["type"] == "file":
                processed.append({
                    "name": item["name"],
                    "hash": item["hash"],
                    "urls": f"{self.small_cdn_base}{item['content']}",
                    "file": f"{self.apt}{item['name']}.png",
                    "type": "image"
                })
            else:
                processed.append({
                    "name": item["name"],
                    "hash": item["hash"],
                    "content": item["content"],
                    "file": f"{self.apt}{item['name']}.png",
                    "type": "text"
                })
        return processed



'''            voice = MessageChain()
            voice.chain.append(Record(file=output_audio_path))
            await event.send(voice)'''