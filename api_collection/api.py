from astrbot.api.all import *
import requests
import aiohttp
import asyncio
import aiohttp
async def get_menu(menu_path):
    # API地址
    api_url = "http://116.62.188.107:5000/images/menu"
    result = MessageChain()
    result.chain = []
    try:
        # 使用 aiohttp 发送异步 GET 请求
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                # 检查请求是否成功
                if response.status == 200:
                    # 读取图片内容
                    image_data = await response.read()
                    # 将图片保存到本地
                    with open(menu_path, "wb") as file:
                        file.write(image_data)
                    # 构造返回结果
                    result.chain = [Image.fromFileSystem(menu_path)]
                    return result
                else:
                    result.chain = [Plain("请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result

async def get_hash():
    # API地址
    url = "http://116.62.188.107:5000/api/menu"
    result = MessageChain()
    result.chain = []
    try:
        # 使用 aiohttp 发送异步 GET 请求
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                # 检查请求是否成功
                if response.status == 200:
                    # 解析返回的JSON数据
                    data = await response.json()
                    return data.get("hash")
                else:
                    # 请求失败时，将错误信息放入 MessageChain 中
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        # 请求异常时，将异常信息放入 MessageChain 中
        result.chain = [Plain(f"请求异常: {e}")]
        return result

async def get_version():
    # API地址
    api_url = "http://116.62.188.107:5000/api/version"
    result = MessageChain()
    result.chain = []
    try:
        # 使用 aiohttp 发送异步 GET 请求
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                # 检查请求是否成功
                if response.status == 200:
                    # 解析返回的JSON数据
                    data = await response.json()
                    version = data.get("version")
                    return version
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result