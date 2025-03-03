from astrbot.api.all import *
import requests
from typing import Optional
import aiohttp
from typing import Optional
from your_module import MessageChain, Plain, Image, Record  # 请根据实际情况导入相应的类

async def search_music(song_name: str, n: Optional[int] = None):
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

    result = MessageChain()
    result.chain = []
    try:
        # 使用 aiohttp 发送异步 GET 请求
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                # 检查请求是否成功
                if response.status == 200:
                    data = await response.json()  # 解析返回的JSON数据
                    if data.get("code") == 200:
                        if n:
                            # 返回单曲详细信息
                            result.chain.append(Plain(f"歌曲: {data.get('title', 'N/A')}\n"))
                            result.chain.append(Plain(f"歌手: {data.get('singer', 'N/A')}\n"))
                            result.chain.append(Plain(f"音质: {data.get('id', 'N/A')}\n"))
                            result.chain.append(Image.fromURL(data.get('cover', 'N/A')))
                            #result.chain.append(Plain(f"歌词: {data.get('lrc', 'N/A')}\n"))
                            urls1 = data.get('music_url', 'N/A')
                            det = await generate_music(urls1)
                            return result, det
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
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))
                    return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result

async def get_music():
    '''给用户发送音乐推荐内容，用户需要音乐推荐，提到有关音乐推荐，音乐时调用此工具'''
    url = "https://api.lolimi.cn/API/wyrp/api.php"
    result = MessageChain()
    result.chain = []
    try:
        # 使用 aiohttp 发送异步 GET 请求
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # 检查请求是否成功
                if response.status == 200:
                    data = await response.json()  # 解析返回的JSON数据
                    # 拼接字符串
                    result.chain.append(Plain(f"Music: {data['data'].get('Music', 'N/A')}\n"))
                    result.chain.append(Plain(f"Name: {data['data'].get('name', 'N/A')}\n"))
                    result.chain.append(Image.fromURL(data['data'].get('Picture', 'N/A')))
                    result.chain.append(Plain(f"ID: {data['data'].get('id', 'N/A')}\n"))
                    result.chain.append(Plain(f"Content: {data['data'].get('Content', 'N/A')}\n"))
                    result.chain.append(Plain(f"Nick: {data['data'].get('Nick', 'N/A')}\n"))
                    urls2 = data['data'].get('Url', 'N/A')
                    det = await generate_music(urls2)
                    return result, det
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))
                    return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result

async def generate_music(url):
    result = MessageChain()
    result.chain = []
    try:
        # 使用 aiohttp 发送异步 GET 请求
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # 检查请求是否成功
                if response.status == 200:
                    # 保存音乐文件到本地
                    with open("./data/plugins/astrbot_plugin_comp_entertainment/music.mp3", "wb") as file:
                        file.write(await response.read())
                    return "./data/plugins/astrbot_plugin_comp_entertainment/music.mp3"
                else:
                    result.chain.append(Plain(f"下载失败，状态码: {response.status}"))
                    return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result

async def generate_voice(text: str, model: str):
    '''根据用户提供的文本生成语音，用户需要生成语音，提到有关语音合成时调用此工具
    Args:
        text (string): 用户提供的文本内容，支持中英日三语，超过200字符会自动切割。
        model (string): 语音模型，支持8个：菈妮，玛莲妮亚，梅琳娜，帕奇，米莉森，蒙葛特，女v，银手。默认值为"菈妮"。
    '''
    # API地址
    url = "http://uapi.dxx.gd.cn/voice/add"
    speed_factor = 1.0 #语速，取值范围0.5-1.5，默认值为1.0。
    types = "url" #音频返回形式，仅支持url和base64，默认值为"url"。
    # 请求参数
    params = {
        "text": text,
        "model": model,
        "speed_factor": speed_factor,
        "type": types
    }
    result = MessageChain()
    result.chain = []
    try:
        # 使用 aiohttp 发送异步 POST 请求
        async with aiohttp.ClientSession() as session:
            async with session.post(url, data=params) as response:
                # 检查请求是否成功
                if response.status == 200:
                    data = await response.json()  # 解析返回的JSON数据
                    if data.get("code") == 200:
                        if types == "url":
                            output_audio_path = data.get('url', 'N/A')
                            result.chain.append(Record(file=output_audio_path))
                        return result
                    else:
                        result.chain.append(Plain(f"语音生成失败: {data.get('msg', '未知错误')}"))
                        return result
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))
                    return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result
