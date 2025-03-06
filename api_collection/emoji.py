from astrbot.api.all import *
import requests
import random
import aiohttp
async def mix_emojis(emoji1: str, emoji2: str):
    # API地址
    url = "https://free.wqwlkj.cn/wqwlapi/emojimix.php"
    # 请求参数
    params = {
        "emoji1": emoji1,
        "emoji2": emoji2,
        "type": "json"  # 指定返回格式为JSON
    }

    result = MessageChain()
    result.chain = []

    try:
        # 使用 aiohttp 发送异步 GET 请求
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                # 检查请求是否成功
                if response.status == 200:
                    # 解析返回的JSON数据
                    data = await response.json()

                    if data.get("code") == 1:
                        result.chain.append(Plain(f"混合结果: {data.get('text', 'N/A')}\n"))
                        result.chain.append(Image.fromURL(data['data'].get('url', 'N/A')))
                    else:
                        result.chain.append(Plain(f"表情包混合失败: {data.get('text', '未知错误')}"))
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))

                return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result
async def get_qq_avatar(qq_number):
    # API地址
    url = "https://api.lolimi.cn/API/head/api.php"
    # 请求参数
    params = {
        "QQ": qq_number
    }
    result = MessageChain()
    result.chain = []
    try:
        # 使用 aiohttp 发送异步 GET 请求
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                # 检查请求是否成功
                if response.status == 200:
                    # 读取图片内容
                    image_data = await response.read()
                    # 将图片保存到本地
                    with open("./data/plugins/astrbot_plugin_comp_entertainment/pet.jpg", "wb") as file:
                        file.write(image_data)
                    # 构造返回结果
                    result.chain = [Image.fromFileSystem("./data/plugins/astrbot_plugin_comp_entertainment/pet.jpg")]
                    return result
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result

async def fetch_image_from_api(msg):
    # API地址
    url = "https://api.lolimi.cn/API/pai/api.php"
    # 请求参数
    params = {
        'msg': msg
    }
    result = MessageChain()
    result.chain = []
    try:
        # 使用 aiohttp 发送异步 GET 请求
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                # 检查请求是否成功
                if response.status == 200:
                    # 读取图片内容
                    image_data = await response.read()
                    # 将图片保存到本地
                    with open("./data/plugins/astrbot_plugin_comp_entertainment/person.png", "wb") as file:
                        file.write(image_data)
                    # 构造返回结果
                    result.chain = [Image.fromFileSystem("./data/plugins/astrbot_plugin_comp_entertainment/person.png")]
                    return result
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result

async def generate_image12(prompt):
    # API地址
    url = "https://api.52vmy.cn/api/img/tw"
    # 请求参数
    params = {
        "msg": prompt
    }
    result = MessageChain()
    result.chain = []
    try:
        # 使用 aiohttp 发送异步 GET 请求
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                # 检查请求是否成功
                if response.status == 200:
                    # 读取图片内容
                    image_data = await response.read()
                    # 将图片保存到本地
                    with open("./data/plugins/astrbot_plugin_comp_entertainment/hand.png", "wb") as file:
                        file.write(image_data)
                    # 构造返回结果
                    result.chain = [Image.fromFileSystem("./data/plugins/astrbot_plugin_comp_entertainment/hand.png")]
                    return result
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result

async def fetch_image(qq_number, flag):
    # 定义字典映射
    switch_dict = {
        "摸头": "https://api.lolimi.cn/API/face_petpet/api.php",
        "感动哭了": "https://api.lolimi.cn/API/face_touch/api.php",
        "膜拜": "https://api.lolimi.cn/API/face_worship/api.php",
        "咬": "https://api.lolimi.cn/API/face_suck/api.php",
        "可莉吃": "https://api.lolimi.cn/API/chi/api.php",
        "吃掉": "https://api.lolimi.cn/API/face_bite/api.php",
        "捣": "https://api.lolimi.cn/API/face_pound/api.php",
        "咸鱼": "https://api.lolimi.cn/API/face_yu/api.php",
        "玩": "https://api.lolimi.cn/API/face_play/api.php",
        "舔": "https://api.lolimi.cn/API/tian/api.php",
        "拍": "https://api.lolimi.cn/API/face_pat/api.php",
        "丢": "https://api.lolimi.cn/API/diu/api.php",
        "撕": "https://api.lolimi.cn/API/si/api.php",
        "求婚": "https://api.lolimi.cn/API/face_propose/api.php",
        "爬": "https://api.lolimi.cn/API/pa/api.php",
        "你可能需要他": "https://api.lolimi.cn/API/face_need/api.php",
        "想看": "https://api.lolimi.cn/API/face_thsee/api.php",
        "点赞": "https://api.lolimi.cn/API/zan/api.php",
    }
    # 获取对应的URL
    url = switch_dict.get(flag, '')
    params = {
        'QQ': qq_number
    }
    result = MessageChain()
    result.chain = []
    try:
        # 使用 aiohttp 发送异步 GET 请求
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                # 检查请求是否成功
                if response.status == 200:
                    # 读取图片内容
                    image_data = await response.read()
                    # 将图片保存到本地
                    with open("./data/plugins/astrbot_plugin_comp_entertainment/petemoji.gif", "wb") as file:
                        file.write(image_data)
                    # 构造返回结果
                    result.chain = [Image.fromFileSystem("./data/plugins/astrbot_plugin_comp_entertainment/petemoji.gif")]
                    return result
                else:
                    result.chain = [Plain(f"表情包制作失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result

async def fetch_image2(qq_number, qq_number2, msg, msg2):
    url = "https://api.lolimi.cn/API/preview/api.php"
    # 生成 1 到 166 之间的随机整数
    types = random.randint(1, 166)
    params = {
        'qq': qq_number,
        'qq2': qq_number2,
        'msg': msg,
        'msg2': msg2,
        'type': types,
    }
    result = MessageChain()
    result.chain = []
    try:
        # 使用 aiohttp 发送异步 GET 请求
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                # 检查请求是否成功
                if response.status == 200:
                    # 读取图片内容
                    image_data = await response.read()
                    # 将图片保存到本地
                    with open("./data/plugins/astrbot_plugin_comp_entertainment/p1.gif", "wb") as file:
                        file.write(image_data)
                    # 构造返回结果
                    result.chain = [Image.fromFileSystem("./data/plugins/astrbot_plugin_comp_entertainment/p1.gif")]
                    return result
                else:
                    result.chain = [Plain(f"表情包制作失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result

async def parse_target2(event,ids):
    for comp in event.message_obj.message:
        if isinstance(comp, At) and event.get_self_id() != str(comp.qq) and ids!= str(comp.qq):
            return str(comp.qq)
        else:
            return event.get_self_id()
async def parse_target(event):
    """解析@目标或用户名"""
    for comp in event.message_obj.message:
        if isinstance(comp, At) and event.get_self_id() != str(comp.qq):
            return str(comp.qq)
    return None