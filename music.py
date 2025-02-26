from astrbot.api.all import *
import requests
from typing import Optional
op = ''
def search_music(song_name: str, n: Optional[int] = None):
    # API地址
    url = "https://www.hhlqilongzhu.cn/api/dg_wyymusic.php"
    # 请求参数
    params = {
        "gm": song_name,
        "type": "json"  # 指定返回格式为JSON
    }
    if n:
        params["n"] = n
    try:
        # 发送GET请求
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析返回的JSON数据
        result = MessageChain()
        result.chain = []
        if data.get("code") == 200:
            if n:
                # 返回单曲详细信息
                result.chain.append(Plain(f"歌曲: {data.get('title', 'N/A')}\n"))
                result.chain.append(Plain(f"歌手: {data.get('singer', 'N/A')}\n"))
                result.chain.append(Plain(f"音质: {data.get('id', 'N/A')}\n"))
                result.chain.append(Image.fromURL(data.get('cover', 'N/A')))
                #result.chain.append(Plain(f"歌词: {data.get('lrc', 'N/A')}\n"))
                global op
                op = data.get('music_url', 'N/A')
                return result
            else:
                # 返回歌曲列表
                result.chain.append(Plain(f"找到以下歌曲:\n"))
                for item in data.get("data", []):
                    result.chain.append(Plain(f"{item['n']}. {item['title']} - {item['singer']}\n"))
                result.chain.append(Plain("请输入序号获取具体歌曲信息"))
                return result
        else:
            result.chain.append(Plain("搜索失败，请稍后再试。"))
            return result
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None
def search_music2():
    return op