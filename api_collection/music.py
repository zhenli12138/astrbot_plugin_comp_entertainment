from astrbot.api.all import *
import requests
from typing import Optional
import aiohttp
from typing import Optional
import httpx
counter = 0
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
                            urls = data.get('music_url', 'N/A')
                            return result, urls
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
    det =''
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
                    urls = data['data'].get('Url', 'N/A')
                    return result, urls
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))
                    return result, det
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result, det
async def generate_music(url):
    global counter
    result = MessageChain()
    result.chain = []
    try:
        # 使用 httpx 发送异步 GET 请求
        async with httpx.AsyncClient() as client:
            response = await client.get(url,follow_redirects=True)
            # 检查请求是否成功
            if response.status_code == 200:
                if counter == 20:
                    counter = 0
                counter = counter + 1
                # 保存音乐文件到本地
                with open(f"./data/plugins/astrbot_plugin_comp_entertainment/music{counter}.wav", "wb") as file:
                    # 分块读取数据
                    async for chunk in response.aiter_bytes():
                        file.write(chunk)
                return f"./data/plugins/astrbot_plugin_comp_entertainment/music{counter}.wav"
            else:
                print(f"下载失败，状态码: {response.status_code}")
    except httpx.RequestError as e:
        print(f"请求异常: {e}")
async def wyy_music_info(url=None, ids=None, level='standard'):
    """
    调用网易云音乐API获取歌曲信息
    :param url: 音乐分享链接
    :param ids: 网易云音乐ID
    :param level: 音质等级 (standard/exhigh/lossless/hires/jyeffect/sky/jymaster)
    """
    api_url = 'https://api.kxzjoker.cn/api/163_music'
    # 参数验证
    if url and ids:
        raise ValueError("不能同时提供url和ids参数")
    if not url and not ids:
        raise ValueError("必须提供url或ids参数")
    resp_type = 'json'

    params = {
        'level': level,
        'type': resp_type
    }
    if url:
        params['url'] = url
    else:
        params['ids'] = ids
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params) as response:
                response.raise_for_status()  # 检查HTTP状态码
                # 根据响应类型处理结果
                if resp_type == 'json':
                    data = await response.json()
                    result.chain.append(Plain(f"专辑: {data.get('al_name', 'N/A')}\n"))
                    result.chain.append(Plain(f"歌手: {data.get('ar_name', 'N/A')}\n"))
                    result.chain.append(Plain(f"音质: {data.get('level', 'N/A')}\n"))
                    result.chain.append(Image.fromURL(data.get('pic', 'N/A')))
                    # result.chain.append(Plain(f"歌词: {data.get('lrc', 'N/A')}\n"))
                    urls = data.get('url', 'N/A')
                    return result, urls
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result
    except Exception as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result

