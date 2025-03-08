from pathlib import Path
from astrbot.api.all import *
from typing import (Dict, Any, Optional, AnyStr, Callable, Union, Awaitable,Coroutine,List)
import json
import aiohttp
import asyncio

ALLOWED_GROUPS_FILE = Path("./data/plugins/astrbot_plugin_comp_entertainment/allowed_groups.jsonl")
MESSAGE_BUFFER: Dict[str, List[dict]] = {}  # {group_id: [{"user_id": str, "messages": list}, ...]}
BUFFER_LIMIT = 2  # 一问一答的对话对数量
MERGE_TIMEOUT = 60  # 同一用户消息合并时间窗口（秒）

async def process_group_buffer(group_id: str):
    """处理指定群组的消息缓冲区"""
    buffer = MESSAGE_BUFFER.get(group_id, [])
    send_queue = []

    # 收集有效对话对
    i = 0
    while i < len(buffer) - 1:
        current = buffer[i]
        next_msg = buffer[i + 1]

        # 确保是不同用户且时间顺序正确
        if current["user_id"] != next_msg["user_id"]:
            send_queue.append((current["messages"], next_msg["messages"]))
            i += 2
        else:
            i += 1

    # 发送收集到的对话对
    if send_queue:
        for pair in send_queue:
            await send_train_request(pair)

        # 更新缓冲区（移除已发送的消息）
        MESSAGE_BUFFER[group_id] = buffer[i:]


async def send_train_request(message_pairs: tuple):
    """发送训练请求到后端"""
    train_payload = {
        "messages_list": list(message_pairs)
    }
    print(f"上传消息:{train_payload}")
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    "http://116.62.188.107:7000/train",
                    json=train_payload,
                    timeout=aiohttp.ClientTimeout(total=30)
            ) as response:
                if response.status != 200:
                    logger.error(f"训练失败: {response.status}")
                    if response.status != 200:
                        logger.error(f"训练失败: {response.status} {await response.text()}")
    except aiohttp.ClientConnectorError:
        logger.error("无法连接到训练服务器")
    except asyncio.TimeoutError:
        logger.error("训练请求超时")
    except json.JSONDecodeError:
        logger.error("响应解析失败")


async def merge_messages(messages: List[dict]) -> List[dict]:
    merged = []
    last_type = None
    for msg in messages:
        if msg["type"] == last_type == "text":
            merged[-1]["content"] += f"，{msg['content']}"
        else:
            merged.append(msg)
            last_type = msg["type"]
    return merged


async def ask_question(event: AstrMessageEvent, question: str):
    """发送询问请求"""
    ask_payload = {
        "message_chain": [{"type": "text", "content": question}]
    }
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                    "http://116.62.188.107:7000/ask",
                    json=ask_payload,
                    timeout=aiohttp.ClientTimeout(total=10)
            ) as response:
                if response.status == 200:
                    reply = await response.json()
                    logger.warning(f"回复消息: {reply}")
                    result.chain = []
                    reg = ''
                    for elem in reply.get("reply", []):
                        if elem["type"] == "text":
                            result.chain.append(Plain(elem["content"]))
                            reg += elem["content"]
                        elif elem["type"] == "image":
                            result.chain.append(Image.fromURL(elem["url"]))
                        else:
                            result.chain.append(Plain('不理你！'))
                            reg += '空'
                    # await event.send(result)
                    # return result
                    return reg
                else:
                    error_info = await response.text()
                    logger.warning(f'请提醒用户程序出错：询问失败: {response.status} {error_info}')

    except aiohttp.ClientConnectorError:
        logger.warning('请提醒用户程序出错：api访问失败')
    except asyncio.TimeoutError:
        logger.warning('请提醒用户程序出错：api访问失败')
    except Exception as e:
        logger.warning(f'请提醒用户程序出错：{str(e)}')