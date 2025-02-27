from astrbot.api.all import *
import requests
from typing import Optional
def get_random_genshin_cosplay():
    # API地址
    url = "https://v2.xxapi.cn/api/yscos"
    try:
        # 发送GET请求
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析返回的JSON数据

        if data.get("code") == 200:
            result = MessageChain()
            result.chain = []
            result.chain.append(Image.fromURL(data.get("data")))
            return result
        else:
            print(f"获取失败: {data.get('msg', '未知错误')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None
def fetch_cosplay_data():
    '''发送cosplay图片,当用户需要cosplay图片，提到有关cosplay图片，cosplay时调用此工具'''
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
                result = MessageChain()
                result.chain = []
                title = data["data"]["Title"]
                image_urls = data["data"]["data"]
                result.chain = [Plain(f"标题: {title}\n")]
                for url in image_urls:
                    result.chain.append(Image.fromURL(url))
                return result
            else:
                print(f"获取失败: {data.get('text')}")
        else:
            print(f"请求失败，状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"请求出错: {e}")
def call_api():
    # 接口地址
    '''发送一张随机的关于原神的图片，用户需要原神图片，提到有关原神图片，原神时调用此工具'''
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
        result = MessageChain()
        result.chain = []
        result.chain.append(Image.fromURL(data.get("text")))
        return result
    else:
        print("请求失败，状态码:", response.status_code)
def call_api2():
    '''发送一张随机的‘龙图‘，用户需要龙图，提到有关龙图时调用此工具’'''
    # 接口地址
    url = "https://api.lolimi.cn/API/longt/l.php"
    # 发送GET请求
    response = requests.get(url)
    if response.status_code == 200:
        # 将返回的图片内容保存到本地
        image_data = response.content
        with open(f"./data/plugins/astrbot_plugin_moreapi/long.png", "wb") as file:
            file.write(image_data)
        result = MessageChain()
        result.chain = []
        result.chain = [Image.fromFileSystem("./data/plugins/astrbot_plugin_moreapi/long.png")]
        return result
    else:
        print(f"请求失败，状态码: {response.status_code}")
def get_random_superpower():
    '''随机生成超能力及其副作用，用户需要随机超能力，提到有关超能力时调用此工具'''
    # API地址
    url = "https://api.pearktrue.cn/api/superpower/"
    try:
        # 发送GET请求
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析返回的JSON数据

        if data.get("code") == 200:
            result = MessageChain()
            result.chain = []
            if data:
                result.chain.append(Plain(f"超能力: {data.get('superpower', 'N/A')}\n"))
                result.chain.append(Plain(f"副作用: {data.get('sideeffect', 'N/A')}\n"))
                result.chain.append(Image.fromURL(data.get('image_url', 'N/A')))
            else:
                result.chain.append(Plain("获取超能力失败，请稍后再试。"))
            return result
        else:
            print(f"获取失败: {data.get('msg', '未知错误')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None
def get_daily_60s_news():
    # API地址
    '''获取每日60秒早报，用户需要每日新闻，提到有关60秒早报,早报，新闻，每日新闻时调用此工具'''
    url = "https://api.52vmy.cn/api/wl/60s"
    result = MessageChain()
    result.chain = []
    try:
        # 发送GET请求
        response = requests.get(url)
        image_data = response.content
        output_path = f"./data/plugins/astrbot_plugin_moreapi/daily_60s_news.png"
        with open(output_path, "wb") as file:
            file.write(image_data)
        result.chain.append(Image.fromFileSystem(output_path))
        return result
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        result.chain.append(Plain("获取每日60秒早报失败，请稍后再试。"))
        return result
def get_doutu_images(msg):
    '''根据用户提供的关键词发送一组斗图图片，用户需要斗图，提到有关斗图时调用此工具
    Args:msg(string): 用户提供的关键词，可以模糊判断'''
    # API地址
    url = "https://api.52vmy.cn/api/wl/doutu"
    # 请求参数
    params = {
        "msg": msg,
    }
    result = MessageChain()
    result.chain = []
    try:
        # 发送GET请求
        response = requests.get(url, params=params)
        data = response.json()  # 解析返回的JSON数据
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
            print(f"获取失败: {data.get('msg', '未知错误')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None
def get_ikun_image(lx: str = "bqb"):
    '''Args:lx(string): 图片类型，可选 bqb（表情包）或 tx（头像），默认为 bqb'''
    # API地址
    url = "https://free.wqwlkj.cn/wqwlapi/ikun.php"
    # 请求参数
    params = {
        "type": "image",  # 直接返回图片
        "lx": lx  # 图片类型，默认为表情包（bqb）
    }
    try:
        # 发送GET请求
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查请求是否成功

        # 将返回的图片保存到本地
        image_path = f"./data/plugins/astrbot_plugin_moreapi/ikun_{lx}.png"
        with open(image_path, "wb") as file:
            file.write(response.content)
        result = MessageChain()
        result.chain = []
        if image_path:
            result.chain = [Image.fromFileSystem(image_path)]
        else:
            result.chain = [Plain("获取ikun图片失败，请稍后再试。")]
        return result
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None
def get_webpage_screenshot(url):
    # API地址
    api_url = "https://api.pearktrue.cn/api/screenweb/"
    # 请求参数
    params = {
        "url": url,
        "type": "image",
    }
    try:
        # 发送GET请求
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # 检查请求是否成功\
        # 将返回的图片内容保存到本地
        image_data = response.content
        screenshot_path = f"./data/plugins/astrbot_plugin_moreapi/screenshot.png"
        with open(screenshot_path, "wb") as file:
            file.write(image_data)
        result = MessageChain()
        result.chain = []
        if screenshot_path:
            result.chain.append(Plain("截图结果：\n"))
            result.chain.append(Image.fromFileSystem(screenshot_path))
        else:
            result.chain.append(Plain("网页截图失败，请检查URL是否正确或稍后再试。"))
        return result
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None
def get_tarot_reading():
    '''随机生成塔罗牌占卜结果，用户需要塔罗牌占卜，提到有关塔罗牌时调用此工具'''
    # API地址
    url = "https://oiapi.net/API/Tarot"
    try:
        # 发送GET请求
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析返回的JSON数据
        result = MessageChain()
        result.chain = []
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
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None