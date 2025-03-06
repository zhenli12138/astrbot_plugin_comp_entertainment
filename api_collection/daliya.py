from typing import Optional
import asyncio
from astrbot.api.event import AstrMessageEvent, MessageChain
from astrbot.api.message_components import Plain, Image, Record, At, Node, Nodes
from astrbot.api.message_components import Node, Plain, Image
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent


async def get_name(event: AstrMessageEvent,ids:str):
    if event.get_platform_name() == "aiocqhttp":
        # qq
        client = event.bot  # 得到 client
        payloads = {
            "user_id": ids,
        }
        ret = await client.api.call_action('get_stranger_info', **payloads)  # 调用 协议端  API
        name = ret.get('nick')
        return name


async def easy_send(event: AstrMessageEvent,message: MessageChain):
    bot = event.bot
    ret = await AiocqhttpMessageEvent._parse_onebot_json(message)
    send_one_by_one = False
    for seg in message.chain:
        if isinstance(seg, (Node, Nodes)):
            # 转发消息不能和普通消息混在一起发送
            send_one_by_one = True
            break
    if event.message_obj.group_id:
        message_type = 'group'
    else:
        message_type = 'private'
    if send_one_by_one:
        for seg in message.chain:
            if isinstance(seg, Nodes):
                # 带有多个节点的合并转发消息
                payload = seg.toDict()
                if event.message_obj.group_id:
                    payload['group_id'] = event.message_obj.group_id
                    await bot.call_action('send_group_forward_msg', **payload)
                else:
                    payload['user_id'] = event.message_obj.sender.user_id
                    await bot.call_action('send_private_forward_msg', **payload)
            else:
                msg = await AiocqhttpMessageEvent._parse_onebot_json(MessageChain([seg]))
                payload = await build(msg,message_type, event.message_obj.sender.user_id, event.message_obj.group_id)
                await bot.call_action('send_msg', **payload)
                await asyncio.sleep(0.5)
    else:
        payload = await build(ret,message_type, event.message_obj.sender.user_id, event.message_obj.group_id)
        await bot.call_action('send_msg', **payload)


async def build(msg, message_type:Optional[str], user_id:Optional[str], group_id:Optional[str], discuss_id:Optional[str]=None) -> dict:
    message_dict = {}
    if message_type is not None:
        message_dict['message_type'] = message_type
    if user_id is not None:
        message_dict['user_id'] = user_id
    if group_id is not None:
        message_dict['group_id'] = group_id
    if discuss_id is not None:
        message_dict['discuss_id'] = discuss_id
    keys = {'message_type', 'user_id', 'group_id', 'discuss_id'}
    params = {k: v for k, v in message_dict.items() if k in keys}
    params['message'] = msg
    if 'message_type' not in params:
        if 'group_id' in params:
            params['message_type'] = 'group'
        elif 'discuss_id' in params:
            params['message_type'] = 'discuss'
        elif 'user_id' in params:
            params['message_type'] = 'private'
    return params