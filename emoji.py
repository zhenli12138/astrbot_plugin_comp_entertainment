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