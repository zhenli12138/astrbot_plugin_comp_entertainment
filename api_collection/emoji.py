from astrbot.api.all import *
import requests
from typing import Optional
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
        with open(f"./data/plugins/astrbot_plugin_moreapi/pe.png", "wb") as file:
            file.write(image_data)
        result = MessageChain()
        result.chain = []
        result.chain = [Image.fromFileSystem("./data/plugins/astrbot_plugin_moreapi/pe.png")]
        return result
    else:
        print(f"请求失败，状态码: {response.status_code}")