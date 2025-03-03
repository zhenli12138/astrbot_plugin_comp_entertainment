from astrbot.api.all import *
import requests
import asyncio
import aiohttp
async def fetch_image_url(search_term):
    url = "https://api.lolimi.cn/API/sgst/api.php"
    params = {
        'msg': search_term,
        'type': 'json'
    }
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('code') == 1:
                        image_url = data['data']['url']
                        result.chain = [Plain(f"{search_term}搜图结果:\n"), Image.fromURL(image_url)]
                        return result
                    else:
                        result.chain = [Plain(f"获取失败: {data.get('text', '未知错误')}")]
                        return result
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result

async def get_update_days(num):
    url = "https://api.lolimi.cn/API/B_Update_Days/api.php"
    params = {
        'num': num,
        'type': 'json'
    }
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('code') == 1:
                        for item in data['data']:
                            result.chain.append(Plain(f"Name: {item['Name']}\n"))
                            result.chain.append(Image.fromURL(item['Picture']))
                            result.chain.append(Plain(f"Update: {item['Update']}\n"))
                            result.chain.append(Plain(f"Time: {item['Time']}\n"))
                            result.chain.append(Plain(f"Url: {item['Url']}\n"))
                            result.chain.append(Plain("------------------\n"))
                        return result
                    else:
                        result.chain = [Plain(f"获取失败: {data.get('text', '未知错误')}")]
                        return result
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result
async def get_weather(city):
    url = "https://api.lolimi.cn/API/weather/api.php"
    params = {
        "city": city,
        "type": "json"
    }
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("code") == 1:
                        weather_data = data.get("data", {})
                        result.chain.append(Plain(f"Weather Data for {weather_data.get('city')}\n"))
                        result.chain.append(Plain(f"Temperature: {weather_data.get('temp')}\n"))
                        result.chain.append(Plain(f"Weather: {weather_data.get('weather')}\n"))
                        result.chain.append(Plain(f"Wind: {weather_data.get('wind')}\n"))
                        result.chain.append(Plain(f"Wind Speed: {weather_data.get('windSpeed')}\n"))
                        return result
                    else:
                        result.chain = [Plain(f"获取失败: {data.get('text', '未知错误')}")]
                        return result
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result
async def get_baike_info(msg):
    url = "https://api.52vmy.cn/api/query/baike"
    params = {
        "msg": msg,
        "type": "json"
    }
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("code") == 200:
                        result.chain.append(Plain(f"百科内容: {data['data'].get('text', 'N/A')}\n"))
                        if data['data'].get('img_url'):
                            result.chain.append(Image.fromURL(data['data']['img_url']))
                        if data['data'].get('url'):
                            result.chain.append(Plain(f"更多信息请访问: {data['data']['url']}"))
                        return result
                    else:
                        result.chain = [Plain(f"获取失败: {data.get('msg', '未知错误')}")]
                        return result
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result
async def get_baidu_tiku_answer(question):
    url = "https://api.pearktrue.cn/api/baidutiku/"
    params = {
        "question": question
    }
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("code") == 200:
                        result.chain.append(Plain(f"问题: {data['data'].get('question', 'N/A')}\n"))
                        result.chain.append(Plain(f"选项: {', '.join(data['data'].get('options', []))}\n"))
                        result.chain.append(Plain(f"答案: {data['data'].get('answer', 'N/A')}\n"))
                        return result
                    else:
                        result.chain = [Plain(f"查询失败: {data.get('msg', '未知错误')}")]
                        return result
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result