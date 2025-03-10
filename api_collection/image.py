from astrbot.api.all import *
import requests
from typing import Optional
import aiohttp
import aiohttp
import asyncio


async def take_screenshot(url:str,element_selector:str,branch:str):
    # 定义请求参数（与原始代码相同）
    payload = {
        "url": url,
        "element_selector": element_selector,
        "scroll_retry": 3,
        "branch": branch
    }

    async with aiohttp.ClientSession() as session:
        try:
            # 发送异步 POST 请求
            async with session.post(
                    "http://116.62.188.107:7100/screenshot",
                    json=payload
            ) as response:

                # 处理响应
                if response.status == 200:
                    data = await response.json()
                    original_url = data["image_url"]
                    new_url = original_url.replace("localhost", "116.62.188.107")
                    print(new_url)
                    return new_url
                else:
                    print("请求失败，状态码：", response.status)
                    error_text = await response.text()
                    print("错误信息：", error_text)

        except aiohttp.ClientError as e:
            print("请求发生错误:", str(e))

async def get_random_genshin_cosplay():
    url = "https://v2.xxapi.cn/api/yscos"
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("code") == 200:
                        result.chain.append(Image.fromURL(data.get("data")))
                        return result
                    else:
                        result.chain.append(Plain(f"获取失败: {data.get('msg', '未知错误')}"))
                        return result
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))
                    return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result

async def fetch_cosplay_data():
    url = "https://api.lolimi.cn/API/cosplay/api.php"
    params = {"type": "json"}
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("code") == "1":
                        dist = []
                        dat = []
                        title = data["data"]["Title"]
                        image_urls = data["data"]["data"][:15]
                        urlss = [image_urls[i:i + 5] for i in range(0, len(image_urls), 5)]
                        for urls in urlss:
                            for url in urls:
                                node = Node(
                                    name="鼠鼠的最爱",
                                    content=[
                                        Plain(f"标题：{title}"),
                                        Image.fromURL(url),
                                    ]
                                )
                                dist.append(node)
                            reg = Nodes(dist)
                            dat.append(reg)
                            dist.clear()
                        return dat
                    else:
                        result.chain.append(Plain(f"获取失败: {data.get('text')}"))
                        return result
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))
                    return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result

async def call_api():
    url = "https://api.lolimi.cn/API/yuan/api.php"
    params = {"type": "json"}
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    result.chain.append(Image.fromURL(data.get("text")))
                    return result
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))
                    return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result

async def call_api2():
    url = "https://api.lolimi.cn/API/longt/l.php"
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    with open(f"./data/plugins/astrbot_plugin_comp_entertainment/long.png", "wb") as file:
                        file.write(image_data)
                    result.chain.append(Image.fromFileSystem("./data/plugins/astrbot_plugin_comp_entertainment/long.png"))
                    return result
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))
                    return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result

async def get_random_superpower():
    url = "https://api.pearktrue.cn/api/superpower/"
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("code") == 200:
                        result.chain.append(Plain(f"超能力: {data.get('superpower', 'N/A')}\n"))
                        result.chain.append(Plain(f"副作用: {data.get('sideeffect', 'N/A')}\n"))
                        result.chain.append(Image.fromURL(data.get('image_url', 'N/A')))
                        return result
                    else:
                        result.chain.append(Plain(f"获取失败: {data.get('msg', '未知错误')}"))
                        return result
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))
                    return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result

async def get_daily_60s_news():
    url = "https://api.52vmy.cn/api/wl/60s"
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    image_data = await response.read()
                    output_path = f"./data/plugins/astrbot_plugin_comp_entertainment/daily_60s_news.png"
                    with open(output_path, "wb") as file:
                        file.write(image_data)
                    result.chain.append(Image.fromFileSystem(output_path))
                    return result
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))
                    return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result

async def get_doutu_images(msg):
    url = "https://api.52vmy.cn/api/wl/doutu"
    params = {"msg": msg}
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("code") == 201:
                        data = data.get("data")
                        if data:
                            result.chain.append(Plain(f"关键词: {msg}\n"))
                            for item in data:
                                result.chain.append(Plain(f"标题: {item['title']}\n"))
                                result.chain.append(Image.fromURL(item['url']))
                        else:
                            result.chain.append(Plain("获取斗图失败，请稍后再试。"))
                        return result
                    else:
                        result.chain.append(Plain(f"获取失败: {data.get('msg', '未知错误')}"))
                        return result
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))
                    return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result

async def get_ikun_image(lx: str = "bqb"):
    url = "https://free.wqwlkj.cn/wqwlapi/ikun.php"
    params = {"type": "image", "lx": lx}
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    image_data = await response.read()
                    image_path = f"./data/plugins/astrbot_plugin_comp_entertainment/ikun_{lx}.png"
                    with open(image_path, "wb") as file:
                        file.write(image_data)
                    result.chain.append(Image.fromFileSystem(image_path))
                    return result
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))
                    return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result

async def get_webpage_screenshot(url):
    api_url = "https://api.pearktrue.cn/api/screenweb/"
    params = {"url": url, "type": "image"}
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params) as response:
                if response.status == 200:
                    image_data = await response.read()
                    screenshot_path = f"./data/plugins/astrbot_plugin_comp_entertainment/screenshot.png"
                    with open(screenshot_path, "wb") as file:
                        file.write(image_data)
                    result.chain.append(Plain("截图结果：\n"))
                    result.chain.append(Image.fromFileSystem(screenshot_path))
                    return result
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))
                    return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result

async def get_tarot_reading():
    url = "https://oiapi.net/API/Tarot"
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("code") == 1:
                        for card in data.get("data", []):
                            result.chain.append(Plain(f"位置: {card.get('position', 'N/A')}\n"))
                            result.chain.append(Plain(f"含义: {card.get('meaning', 'N/A')}\n"))
                            result.chain.append(Plain(f"中文名: {card.get('name_cn', 'N/A')}\n"))
                            result.chain.append(Plain(f"英文名: {card.get('name_en', 'N/A')}\n"))
                            if card.get("type") == "正位":
                                result.chain.append(Plain(f"正位: {card.get('正位', 'N/A')}\n"))
                            else:
                                result.chain.append(Plain(f"逆位: {card.get('逆位', 'N/A')}\n"))
                            result.chain.append(Image.fromURL(card.get("pic", "N/A")))
                            result.chain.append(Plain("-" * 20 + "\n"))
                        return result
                    else:
                        result.chain.append(Plain(f"获取失败: {data.get('message', '未知错误')}"))
                        return result
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))
                    return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result