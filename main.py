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
          "各种api调用【/api】看菜单",
          "v1.1.0")
class MyPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
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
    @filter.command("api")
    async def ddz_menu(self, event: AstrMessageEvent):
        img = self.generate_menu()
        yield event.make_result().message("MOREAPI菜单：\n").file_image(img)
    @filter.command("光遇任务")
    async def trap(self, event: AstrMessageEvent):
        '''【光遇任务】指令'''
        data = self.fetch_daily_tasks()
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        user_id = event.get_sender_id()
        chain = [
            At(qq=user_id),  # At 消息发送者
            Plain(f"Nowtime: {data['nowtime']}\n")
        ]
        # 打印每日任务
        for key, value in data.items():
            if key.isdigit():
                chain.append(Plain(f"Task {key}: {value[0]}"))
                chain.append(Image.fromURL(value[1]))
        yield event.chain_result(chain)

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
    @filter.command("xjj")
    async def trap1(self, event: AstrMessageEvent):
        '''指令'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        #id = self.parse_target(event)
        data = self.xjj()
        if data:
            chain = [Video.fromFileSystem(data)]
            yield event.chain_result(chain)
        else:
            yield event.plain_result("请求失败！")
    @filter.command("movie")
    async def trap2(self, event: AstrMessageEvent):
        '''指令'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.movie()
        if os.path.exists(data):
            with open(data, 'r',encoding="utf-8") as file:
                text = file.read()
        yield event.plain_result(text)
    @filter.command("bcomic")
    async def trap3(self, event: AstrMessageEvent,num:str):
        '''指令'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.get_update_days(num)
        chain = []
        if data:
            for item in data:
                chain.append(Plain(f"Name: {item['Name']}\n"))
                chain.append(Image.fromURL(item['Picture']))
                chain.append(Plain(f"Update: {item['Update']}\n"))
                chain.append(Plain(f"Time: {item['Time']}\n"))
                chain.append(Plain(f"Url: {item['Url']}\n"))
                chain.append(Plain("------------------\n"))
        yield event.chain_result(chain)

    @filter.command("cosplay")
    async def trap4(self, event: AstrMessageEvent):
        '''指令'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.fetch_cosplay_data()
        # 获取标题和图片链接
        title = data["data"]["Title"]
        image_urls = data["data"]["data"]
        chain = [Plain(f"标题: {title}\n")]
        for url in image_urls:
            chain.append(Image.fromURL(url))
        yield event.chain_result(chain)
    @filter.command("翻译")
    async def trap5(self, event: AstrMessageEvent,a:str):
        '''指令'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.translate_text(a)
        yield event.plain_result(data)
    @filter.command("随机段子")
    async def trap6(self, event: AstrMessageEvent):
        '''指令'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.get_random_text()
        yield event.plain_result(f"随机段子：{data}")

    @filter.command("搜狗搜图")
    async def trap7(self, event: AstrMessageEvent,a:str):
        '''指令'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.fetch_image_url(a)
        chain = [Plain(f"{a}搜图结果:\n")]
        chain.append(Image.fromURL(data))
        yield event.chain_result(chain)
    @filter.command("天气")
    async def trap8(self, event: AstrMessageEvent,num:str):
        '''指令'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.get_weather(num)
        chain = []
        if isinstance(data, dict):
            chain.append(Plain(f"Weather Data for {data.get('city')}\n"))
            chain.append(Plain(f"Temperature: {data.get('temp')}\n"))
            chain.append(Plain(f"Weather: {data.get('weather')}\n"))
            chain.append(Plain(f"Wind: {data.get('wind')}\n"))
            chain.append(Plain(f"Wind Speed: {data.get('windSpeed')}\n"))
        else:
            print(data)
        yield event.chain_result(chain)
    @filter.command("毒鸡汤")
    async def trap9(self, event: AstrMessageEvent):
        '''指令'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.get_dujitang()
        yield event.plain_result(f"毒鸡汤：{data}")
    @filter.command("头像框")
    async def trap10(self, event: AstrMessageEvent):
        ''''''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        id = self.parse_target(event)
        data = self.get_qq_avatar(id)
        if not data:
            yield event.plain_result("请求失败，该api已失效")
        else:
            yield event.image_result(data)
    @filter.command("小人举牌")
    async def trap11(self, event: AstrMessageEvent,a:str):
        ''''''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.fetch_image_from_api(a)
        if not data:
            yield event.plain_result("请求失败，该api已失效")
        else:
            yield event.image_result(data)
    @filter.command("音乐推荐")
    async def trap12(self, event: AstrMessageEvent):
        '''指令'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.get_music()
        chain = []
        # 拼接字符串
        chain.append(Plain(f"Music: {data['data'].get('Music', 'N/A')}\n"))
        chain.append(Plain(f"Name: {data['data'].get('name', 'N/A')}\n"))
        chain.append(Image.fromURL(data['data'].get('Picture', 'N/A')))
        chain.append(Plain(f"点此听歌: {data['data'].get('Url', 'N/A')}\n"))
        chain.append(Plain(f"ID: {data['data'].get('id', 'N/A')}\n"))
        chain.append(Plain(f"Content: {data['data'].get('Content', 'N/A')}\n"))
        chain.append(Plain(f"Nick: {data['data'].get('Nick', 'N/A')}\n"))
        # 将结果添加到 chain 中
        yield event.chain_result(chain)
    @filter.command("随机原神")
    async def trap13(self, event: AstrMessageEvent):
        ''''''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.call_api()
        chain = [Image.fromURL(data)]
        # 将结果添加到 chain 中
        yield event.chain_result(chain)
    @filter.command("随机龙图")
    async def trap14(self, event: AstrMessageEvent):
        ''''''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.call_api2()
        if not data:
            yield event.plain_result("请求失败，该api已失效")
        else:
            yield event.image_result(data)
    @filter.command("温柔语录")
    async def trap15(self, event: AstrMessageEvent):
        '''指令'''
        message_chain = event.get_messages()  # 用户所发的消息的消息链
        logger.info(message_chain)
        data = self.get_random_text2()
        yield event.plain_result(f"温柔语录：{data}")

    def get_random_text2(self):
        url = "https://api.lolimi.cn/API/wryl/api.php"
        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            return response.text
        except requests.exceptions.RequestException as e:
            return f"请求失败: {e}"
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
    def get_music(self):
        url = "https://api.lolimi.cn/API/wyrp/api.php"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            return data

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
    def get_random_text(self):
        url = "https://api.lolimi.cn/API/yiyan/dz.php"
        try:
            response = requests.get(url)
            response.raise_for_status()  # 检查请求是否成功
            return response.text
        except requests.exceptions.RequestException as e:
            return f"请求失败: {e}"
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
    def xjj(self):
        url = "https://api.lolimi.cn/API/xjj/xjj.php"
        # 发送GET请求
        response = requests.get(url)
        # 检查请求是否成功
        if response.status_code == 200:
            data = response.content
            with open(f"./data/plugins/astrbot_plugin_moreapi/xjj.mp4", "wb") as file:
                file.write(data)
            return f"./data/plugins/astrbot_plugin_moreapi/xjj.mp4"
        else:
            print(f"请求失败，状态码: {response.status_code}")
            return None

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

    def parse_target(self, event):
        """解析@目标或用户名"""
        for comp in event.message_obj.message:
            if isinstance(comp, At) and event.get_self_id() != str(comp.qq):
                return str(comp.qq)

    def generate_menu(self):
        img = PILImage.new('RGB', (800, 800), (73, 109, 137))
        d = ImageDraw.Draw(img)
        font = ImageFont.truetype('data/plugins/astrbot_plugin_moreapi/msyh.ttf', 24)
        menu = [
        "【MOREAPI菜单】",
        "/ba攻略 【关键词】",
        "/光遇任务",
        "/xjj（返回随机小姐姐视频）",
        "/movie（电影票房榜单）",
        "/bcomic 【数字】（b番更新表）",
        "/cosplay(返回一组cos图）",
        "/翻译 【要翻译的内容】",
        "/随机段子",
        "/搜狗搜图 【关键词】",
        "/天气 【地区】",
        "/毒鸡汤",
        "/头像框@xx",
        "/小人举牌 【内容】",
        "/音乐推荐（返回随机歌曲）",
        "/随机原神（返回一张原神美图）",
        "/随机龙图",
        "/温柔语录",
        ]
        y = 50
        for line in menu:
            d.text((100, y), line, fill=(255, 255, 0), font=font)
            y += 40

        output_path = f"./data/plugins/astrbot_plugin_moreapi/pic.png"
        img.save(output_path, format='PNG')
        return output_path


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

    @filter.command("ba攻略")
    async def handle_blue_archive(self, event: AstrMessageEvent,text:str):
        """碧蓝档案攻略查询"""
        message_chain = event.get_message_str()
        logger.info(message_chain)
        self.load_game()
        params = {
            "name": text,
            "size": 8,
            "method": 3  # 默认使用混合搜索
        }
        api_data = {}
        # 调用API
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            api_data = response.json()
        except Exception as e:
            logger.error(f"API请求异常：{str(e)}")
            return

        if not api_data:
            yield event.plain_result("攻略查询服务暂不可用，请稍后再试")
            return

        # 处理响应
        chain = []
        if api_data["code"] == 200:
            # 精确匹配
            results = self.process_results(api_data["data"])
            if results:
                best_match = results[0]
                chain.append(Plain(f"找到精确匹配：{best_match['name']}\n"))
                if best_match["type"] == "image":
                    oldhash = self.hash1.get(best_match['name'], '')
                    local_path = best_match["file"]
                    if best_match["hash"] == oldhash and os.path.exists(local_path):
                        chain.append(Image.fromFileSystem(local_path))
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
                        chain.append(Image.fromURL(best_match["urls"]))  # 使用小图
                else:
                    chain.append(Plain(best_match["content"]))
        elif api_data["code"] == 101:
            # 模糊查询
            if not api_data["data"]:
                yield event.plain_result("没有找到相关攻略")
                return
            results = self.process_results(api_data["data"])
            chain.append(Plain("找到以下相似结果：\n"))
            for idx, item in enumerate(results, 1):
                chain.append(Plain(f"{idx}. {item['name']}\n"))
                if item["type"] == "image":
                    oldhash = self.hash1.get(item['name'], '')
                    local_path = item["file"]
                    if item["hash"] == oldhash and os.path.exists(local_path):
                        chain.append(Image.fromFileSystem(local_path))
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
                        chain.append(Image.fromURL(item["urls"]))  # 使用小图
                else:
                    chain.append(Plain(item["content"] + "\n"))
                chain.append(Plain("-" * 20 + "\n"))
            chain.append(Plain("请输入更精确的名称获取具体内容"))
        else:
            yield event.plain_result(f"查询失败：{api_data.get('message', '未知错误')}")
            return

        yield event.chain_result(chain)
