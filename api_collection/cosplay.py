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