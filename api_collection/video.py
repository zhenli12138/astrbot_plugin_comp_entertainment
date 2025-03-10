from astrbot.api.all import *
import requests
import aiohttp
async def xjj():
    '''发送小姐姐视频/美女视频/抖音视频，当用户需要小姐姐视频，提到有关小姐姐，美女视频，小姐姐视频时调用此工具'''
    api_url = "https://api.kxzjoker.cn/API/Beautyvideo.php"
    params = {
        'type': 'json'
    }
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url, params=params) as response:
                if response.status == 200:
                    data = await response.json()  # 解析JSON数据
                    result.chain = [Video.fromURL(data.get('download_url'))]
                    return result
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result
async def search_bilibili_video(msg: str, n: str = "1"):
    '''根据用户提供的关键词搜索B站视频，用户需要搜索B站视频，提到有关搜索B站视频，B站视频时调用此工具
    Args:
        msg (string): 用户提供的关键词，如“少年”
        n (string): 返回结果的序号，默认为1
    '''
    url = "https://api.52vmy.cn/api/query/bilibili/video"
    params = {
        "msg": msg,
        "n": n
    }
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()  # 解析返回的JSON数据
                    if data:
                        result.chain.append(Plain(f"标题: {data.get('title', 'N/A')}\n"))
                        result.chain.append(Plain(f"UP主: {data.get('user', 'N/A')}\n"))
                        result.chain.append(Image.fromURL(data.get('img_url', 'N/A')))
                        urls1 = data.get('url', 'N/A')
                        return result, urls1
                    else:
                        result.chain.append(Plain("未找到相关视频，请尝试其他关键词。"))
                        return result
                else:
                    result.chain.append(Plain(f"请求失败，状态码: {response.status}"))
                    return result
    except aiohttp.ClientError as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result

