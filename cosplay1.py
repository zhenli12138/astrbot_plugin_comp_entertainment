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