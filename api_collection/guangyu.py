from astrbot.api.all import *
import requests
import aiohttp
import asyncio
async def fetch_daily_tasks():
    '''发送光遇这个游戏的每日任务，当用户需要光遇任务，提到有关光遇，光遇任务时调用此工具'''
    task_type = "rw"  # rw是每日任务
    url = "https://api.lolimi.cn/API/gy/"  # 接口地址
    params = {'type': task_type}  # 请求参数
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                # 检查请求是否成功
                if response.status == 200:
                    # 解析返回的JSON数据
                    data = await response.json()
                    result.chain.append(Plain(f"Nowtime: {data['nowtime']}\n"))

                    for key, value in data.items():
                        if key.isdigit():
                            result.chain.append(Plain(f"Task {key}: {value[0]}"))
                            result.chain.append(Image.fromURL(value[1]))  # 假设 Image.fromURL 是异步方法

                    return result
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result
    except ValueError as e:
        result.chain = [Plain(f"JSON 解析错误: {e}")]
        return result

