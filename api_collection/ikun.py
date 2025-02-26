from astrbot.api.all import *
import requests
from typing import Optional
def get_ikun_image(lx: str = "bqb"):
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