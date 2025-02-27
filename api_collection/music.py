from astrbot.api.all import *
import requests
from typing import Optional
urls1 = ''
urls2 = ''
def search_music(song_name: str, n: Optional[int] = None):
    '''Args:song_name (string): 歌曲名/n (string, optional): 选择对应的歌曲序号，为空返回列表（用户没给出则默认为空，无需要求）'''
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
                global urls1
                urls1 = data.get('music_url', 'N/A')
                return result
            else:
                # 返回歌曲列表
                result.chain.append(Plain(f"找到以下歌曲:\n"))
                for item in data.get("data", []):
                    result.chain.append(Plain(f"{item['n']}. {item['title']} - {item['singer']}\n"))
                result.chain.append(Plain("请输入【音乐 <序号>】获取具体歌曲"))
                return result
        else:
            result.chain.append(Plain("搜索失败，请稍后再试。"))
            return result
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None
def search_music2():
    global urls1
    det = generate_music(urls1)
    return det
def get_music():
    '''给用户发送音乐推荐内容，用户需要音乐推荐，提到有关音乐推荐，音乐时调用此工具'''
    url = "https://api.lolimi.cn/API/wyrp/api.php"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        result = MessageChain()
        result.chain = []
        # 拼接字符串
        result.chain.append(Plain(f"Music: {data['data'].get('Music', 'N/A')}\n"))
        result.chain.append(Plain(f"Name: {data['data'].get('name', 'N/A')}\n"))
        result.chain.append(Image.fromURL(data['data'].get('Picture', 'N/A')))
        result.chain.append(Plain(f"ID: {data['data'].get('id', 'N/A')}\n"))
        result.chain.append(Plain(f"Content: {data['data'].get('Content', 'N/A')}\n"))
        result.chain.append(Plain(f"Nick: {data['data'].get('Nick', 'N/A')}\n"))
        global urls2
        urls2 = data['data'].get('Url', 'N/A')
        return result
def search_music3():
    global urls2
    det = generate_music(urls2)
    return det
def generate_music(url):
    response = requests.get(url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 保存音乐文件到本地
        with open("./data/plugins/astrbot_plugin_moreapi/music.mp3", "wb") as file:
            file.write(response.content)
        return "./data/plugins/astrbot_plugin_moreapi/music.mp3"
    else:
        print(f"下载失败，状态码: {response.status_code}")