from astrbot.api.all import *
import requests
import random
def mix_emojis(emoji1: str, emoji2: str):
    # API地址
    url = "https://free.wqwlkj.cn/wqwlapi/emojimix.php"
    # 请求参数
    params = {
        "emoji1": emoji1,
        "emoji2": emoji2,
        "type": "json"  # 指定返回格式为JSON
    }
    try:
        # 发送GET请求
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析返回的JSON数据
        result = MessageChain()
        result.chain = []
        if data.get("code") == 1:
            if data and data.get("code") == 1:
                result.chain.append(Plain(f"混合结果: {data.get('text', 'N/A')}\n"))
                result.chain.append(Image.fromURL(data['data'].get('url', 'N/A')))
            else:
                result.chain.append(Plain(f"表情包混合失败: {data.get('text', '未知错误')}"))
            return result
        else:
            print(f"表情包混合失败: {data.get('text', '未知错误')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None
def get_qq_avatar(qq_number):
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
        result = MessageChain()
        result.chain = []
        result.chain = [Image.fromFileSystem("./data/plugins/astrbot_plugin_moreapi/pet.jpg")]
        return result
    else:
        print(f"请求失败，状态码: {response.status_code}")
def parse_target(event):
    """解析@目标或用户名"""
    for comp in event.message_obj.message:
        if isinstance(comp, At) and event.get_self_id() != str(comp.qq):
            return str(comp.qq)
def fetch_image_from_api(msg):
    # API地址
    '''根据用户要求的文字内容发送一张小人举牌图片，用户需要小人举牌图片，提到有关小人举牌，小人举牌图片，举牌时调用此工具
    Args:a(string): 用户提到的文字内容，可以模糊判断'''
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
        with open(f"./data/plugins/astrbot_plugin_moreapi/person.png", "wb") as file:
            file.write(image_data)
        result = MessageChain()
        result.chain = []
        result.chain = [Image.fromFileSystem("./data/plugins/astrbot_plugin_moreapi/person.png")]
        return result
    else:
        print(f"请求失败，状态码: {response.status_code}")
def generate_image12(prompt):
    '''根据用户提到的文字内容发送一张手写的该文字内容的图片，用户需要手写图片，提到有关手写图片，手写时调用此工具
    Args:a(string): 用户提到的文字内容，可以模糊判断'''
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
        with open(f"./data/plugins/astrbot_plugin_moreapi/hand.png", "wb") as file:
            file.write(response.content)
        result = MessageChain()
        result.chain = []
        result.chain = [Image.fromFileSystem("./data/plugins/astrbot_plugin_moreapi/hand.png")]
        return result
    else:
        print(f"请求失败，状态码: {response.status_code}")
def fetch_image(qq_number, flag):
    # 摸头
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
        "想看":"https://api.lolimi.cn/API/face_thsee/api.php",
        "点赞":"https://api.lolimi.cn/API/zan/api.php",
    }
    # 获取对应的函数并执行
    url = switch_dict.get(flag, '')
    params = {
        'QQ': qq_number
    }
    response = requests.get(url, params=params)
    result = MessageChain()
    result.chain = []
    if response.status_code == 200:
        image_data = response.content
        with open(f"./data/plugins/astrbot_plugin_emojiproduction/petemoji.gif", "wb") as file:
            file.write(image_data)
        result.chain = [Image.fromFileSystem("./data/plugins/astrbot_plugin_emojiproduction/petemoji.gif")]
        return result
    else:
        result.chain.append(Plain(f"表情包制作失败"))
        return result

def fetch_image2(qq_number, qq_number2,msg,msg2):
    url = "https://api.lolimi.cn/API/preview/api.php"
    # 生成 1 到 10 之间的随机整数
    types = random.randint(1, 166)
    params = {
        'qq': qq_number,
        'qq2': qq_number2,
        'msg':msg,
        'msg2':msg2,
        'type': types,
    }
    result = MessageChain()
    result.chain = []
    response = requests.get(url, params=params)
    if response.status_code == 200:
        image_data = response.content
        with open(f"./data/plugins/astrbot_plugin_emojiproduction/p.gif", "wb") as file:
            file.write(image_data)
        return f"./data/plugins/astrbot_plugin_emojiproduction/p.gif"
    else:
        result.chain.append(Plain(f"表情包制作失败"))
        return result

def parse_target2(event,ids):
    for comp in event.message_obj.message:
        if isinstance(comp, At) and event.get_self_id() != str(comp.qq) and ids!= str(comp.qq):
            return str(comp.qq)