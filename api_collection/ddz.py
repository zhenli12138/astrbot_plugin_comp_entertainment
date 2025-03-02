from astrbot.api.all import *
import random
import time
from collections import defaultdict
import json
from data.plugins.astrbot_plugin_moreapi.api_collection import daliya
from data.plugins.astrbot_plugin_moreapi.api_collection import pilcreate
op = 0
class Poker:
    suits = ['♠', '♥', '♦', '♣']
    values = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
    specials = ['BJ', 'RJ']
    colors = {'♠': (0, 0, 0), '♥': (255, 0, 0),
              '♦': (255, 0, 0), '♣': (0, 0, 0)}

async def exit_game(event: AstrMessageEvent,rooms,player_rooms):
    room_id = event.get_group_id()
    rooms.pop(room_id, None)
    players = rooms[room_id]['players']
    for p in players:
        player_rooms.pop(p, None)
    result = MessageChain()
    result.chain = [Plain("已解散房间，游戏结束！")]
    await event.send(result)
    return rooms,player_rooms

async def exit_room(event: AstrMessageEvent,rooms,player_rooms):
    user_id = event.get_sender_id()
    room_id = event.get_group_id()
    players = rooms[room_id]['players']
    is_host = players[0] == user_id
    if not room_id:
        result = MessageChain()
        result.chain = [Plain("该群没有游戏房间！")]
        await event.send(result)
        return rooms, player_rooms
    if user_id not in players:
        result = MessageChain()
        result.chain = [Plain("你没在游戏房间！")]
        await event.send(result)
        return rooms, player_rooms
    # 处理不同退出场景
    if is_host:
        exit_type = "房主" if is_host else "管理员"
        for p in players:
            player_rooms.pop(p, None)
        rooms.pop(room_id, None)
        result = MessageChain()
        result.chain = [Plain(f"{exit_type}已解散房间，游戏结束！")]
        await event.send(result)
        return rooms, player_rooms
    else:
        # 普通玩家退出
        if rooms[room_id]['state'] == "playing":
            result = MessageChain()
            result.chain = [Plain("游戏进行中无法退出！")]
            await event.send(result)
            return rooms, player_rooms
        # 从房间移除玩家
        rooms[room_id]['players'].remove(user_id)
        player_rooms.pop(user_id)
        if user_id in rooms[room_id]['game']['hands']:
            rooms[room_id]['game']['hands'].pop(user_id)
        result = MessageChain()
        result.chain = [Plain(f"玩家 {user_id} 已退出房间\n"),Plain(f"当前人数：{len(rooms[room_id]['players'])}")]
        await event.send(result)
        # 如果房间为空，清理房间
        if not players:
            rooms.pop(room_id)
            result = MessageChain()
            result.chain = [Plain(f"已解散房间，游戏结束！")]
            await event.send(result)
        return rooms, player_rooms
async def create_room(event: AstrMessageEvent,rooms,player_rooms):
    user_id = event.get_sender_id()
    group_id = event.get_group_id()
    room_id = group_id
    if user_id in player_rooms:
        result = MessageChain()
        result.chain = [Plain("您已经在房间中！")]
        await event.send(result)
        return rooms, player_rooms
    if room_id in rooms:
        result = MessageChain()
        result.chain = [Plain(f"房间 {room_id} 已存在！")]
        await event.send(result)
        return rooms, player_rooms
    player_rooms[user_id] = room_id
    rooms[room_id] = {
        'players': [user_id],
        'game': {'current_player':'',
                 'dipai':[],
                 'deck':[],
                 'hands':{},
                 'bid_count':'',
                 'dizhu':'',
                 'current_robber':'',
                 'current_bidder':'',
                 'last_played':{},
                 },
        'state': 'waiting'
    }
    result = MessageChain()
    result.chain = [Plain(f"房间创建成功！房间号：{room_id}\n等待其他玩家加入...")]
    await event.send(result)
    return rooms, player_rooms
async def join_room(event: AstrMessageEvent,rooms,player_rooms):
    user_id = event.get_sender_id()
    group_id = event.get_group_id()
    room_id = group_id
    if room_id not in rooms:
        result = MessageChain()
        result.chain = [Plain(f"房间 {room_id} 不存在！")]
        await event.send(result)
        return rooms, player_rooms
    if user_id in rooms[room_id]['players']:
        result = MessageChain()
        result.chain = [Plain(f"你已经加入房间 {room_id}！ ")]
        await event.send(result)
        return rooms, player_rooms
    if len(rooms[room_id]['players']) == 3:
        result = MessageChain()
        result.chain = [Plain(f"房间 {room_id} 人数已满！")]
        await event.send(result)
        return rooms, player_rooms
    rooms[room_id]['players'].append(user_id)
    logger.info(rooms[room_id]['players'])
    player_rooms[user_id] = room_id
    result = MessageChain()
    result.chain = [Plain(f"成功加入房间 {room_id}！当前人数：{len(rooms[room_id]['players'])}")]
    await event.send(result)
    return rooms, player_rooms
async def start_game(event: AstrMessageEvent,rooms,player_rooms):
    room_id = event.get_group_id()
    if len(rooms[room_id]['players']) == 3:
        players = rooms[room_id]['players']
        rooms[room_id]['state'] = "发牌阶段"
        logger.info(rooms[room_id]['state'])
        rooms[room_id]['game']['deck'] = generate_deck()
        deck =rooms[room_id]['game']['deck']# deck: 一副完整的扑克牌。
        random.shuffle(deck)
        rooms[room_id]['game']['hands'] = {p: sorted(deck[i * 17:(i + 1) * 17],
                                                          key=lambda x: card_value(x))
                                                for i, p in enumerate(players)}
        rooms[room_id]['game']['dipai'] = deck[51:54]
        result = MessageChain()
        result.chain = [Plain("发牌结束，请在bot的私聊看牌！")]
        await event.send(result)
        for player in rooms[room_id]['players']:
            await lookcard(event,player,rooms,player_rooms)
        rooms[room_id]['state'] = "叫地主阶段"
        logger.info(rooms[room_id]['state'])
        rooms[room_id]['game']['bid_count'] = '1'
        rooms[room_id]['game']['current_bidder'] = random.choice(players)
        result = MessageChain()
        result.chain = [
            Plain("叫地主开始！当前叫牌玩家："),
            At(qq=rooms[room_id]['game']['current_bidder']),  # At 消息发送者
        ]
        await event.send(result)
        global op
        op = 0
        idx = players.index(rooms[room_id]['game']['current_bidder']) + op
        rooms[room_id]['game']['current_robber'] = players[(idx + 1) % 3]
        result = MessageChain()
        result.chain = [
            Plain("抢地主阶段：请问你是否选择抢地主？"),
            At(qq=rooms[room_id]['game']['current_robber']),  # At 消息发送者
            Plain("发送【/抢地主】抢地主。"),
            Plain("发送【/不抢】不抢地主。"),
        ]
        await event.send(result)
        return rooms, player_rooms
    else:
        result = MessageChain()
        result.chain = [Plain(f"房间 {room_id}未满3人！当前人数：{len(rooms[room_id]['players'])}"),]
        await event.send(result)
        return rooms, player_rooms

#generate_deck: 类方法，生成一副完整的扑克牌，包括52张普通牌和2张特殊牌（大小王）。
def generate_deck():
    deck = [f"{s}{v}" for v in Poker.values for s in Poker.suits]
    deck += Poker.specials
    return deck

#card_value: 类方法，返回一张牌的数值大小，用于比较牌的大小。特殊牌（大小王）有更高的数值。
def card_value(card):
    order = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8,
             '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13,
             'A': 14, '2': 15, 'BJ': 16, 'RJ': 17}
    if card in Poker.specials:
        return order[card]
    return order[card[1:]]

async def lookcard(event: AstrMessageEvent,user_id,rooms,player_rooms):
    room_id = player_rooms.get(user_id)
    event.message_obj.sender.user_id = user_id
    event.message_obj.group_id = ''
    result = MessageChain()
    if not room_id:
        result.chain = [Plain(f"您还没有加入任何游戏房间")]
        await daliya.easy_send(event, result)
        return
    players = rooms[room_id]['players']
    if user_id in players:
        idx = players.index(user_id)
        hand_img = pilcreate.generate_hand_image(rooms[room_id]['game']['hands'][user_id],idx)
        result = MessageChain()
        result.chain = [Plain(f"您的手牌为："),Image.fromFileSystem(hand_img)]
        logger.info(rooms[room_id]['game']['hands'][user_id])
        await daliya.easy_send(event, result)
async def process_bid1(event: AstrMessageEvent,rooms,player_rooms):
    user_id = event.get_sender_id()
    group_id = event.get_group_id()
    room_id = group_id
    if user_id == rooms[room_id]['game']['current_bidder']:
        result = MessageChain()
        result.chain = [
            Plain("您已叫地主，当前地主玩家为"),
            At(qq=rooms[room_id]['game']['current_bidder']),  # At 消息发送者
        ]
        await event.send(result)
        return rooms, player_rooms
    elif user_id == rooms[room_id]['game']['current_robber']:
        rooms[room_id]['game']['bid_count'] = str(int(rooms[room_id]['game']['bid_count']) + 1)
        global op
        op =1
        result = MessageChain()
        result.chain = [
            Plain("您选择不抢地主"),
            At(qq=rooms[room_id]['game']['current_bidder']),  # At 消息发送者
        ]
        await event.send(result)
        rooms, player_rooms = await bid(event,rooms,player_rooms)
        return rooms, player_rooms
    else:
        result = MessageChain()
        result.chain = [
            Plain("目前不是你的回合"),
            At(qq=user_id),  # At 消息发送者
        ]
        await event.send(result)
        return rooms, player_rooms
async def process_bid2(event: AstrMessageEvent,rooms,player_rooms):
    user_id = event.get_sender_id()
    group_id = event.get_group_id()
    room_id = group_id
    if user_id == rooms[room_id]['game']['current_bidder']:
        result = MessageChain()
        result.chain = [
            Plain("您已叫地主，当前地主玩家为"),
            At(qq=rooms[room_id]['game']['current_bidder']),  # At 消息发送者
        ]
        await event.send(result)
        return rooms, player_rooms
    elif user_id == rooms[room_id]['game']['current_robber']:
        rooms[room_id]['game']['bid_count'] = str(int(rooms[room_id]['game']['bid_count']) + 1)
        rooms[room_id]['game']['current_bidder'] = rooms[room_id]['game']['current_robber']
        result = MessageChain()
        result.chain = [
            Plain("您已抢地主，当前地主玩家为"),
            At(qq=rooms[room_id]['game']['current_bidder']),  # At 消息发送者
        ]
        await event.send(result)
        rooms, player_rooms = await bid(event,rooms,player_rooms)
        return rooms, player_rooms
    else:
        result = MessageChain()
        result.chain = [
            Plain("目前不是你的回合"),
            At(qq=user_id),  # At 消息发送者
        ]
        await event.send(result)
        return rooms, player_rooms
async def bid(event: AstrMessageEvent, rooms, player_rooms):
    user_id = event.get_sender_id()
    room_id = player_rooms.get(user_id)
    players = rooms[room_id]['players']
    if rooms[room_id]['game']['bid_count'] == '3':
        rooms[room_id]['game']['dizhu'] = rooms[room_id]['game']['current_bidder']
        rooms[room_id]['game']['hands'][rooms[room_id]['game']['dizhu']].extend(rooms[room_id]['game']['dipai'])
        rooms[room_id]['game']['hands'][rooms[room_id]['game']['dizhu']].sort(key=lambda x: card_value(x))
        result = MessageChain()
        result.chain = [
            At(qq=rooms[room_id]['game']['dizhu']),  # At 消息发送者
            Plain("你是本局游戏的地主！"),
        ]
        await event.send(result)
        rooms[room_id]['state'] = "playing"
        logger.info(rooms[room_id]['state'])
        if not room_id:
            return rooms, player_rooms
        rooms[room_id]['game']['current_player'] = rooms[room_id]['game']['dizhu']
        result = MessageChain()
        result.chain = [
            Plain("地主确定！游戏开始！\n"),
            Plain(f"当前玩家：{rooms[room_id]['game']['current_player']} 请出牌\n"),
            At(qq=user_id),  # At 消息发送者
        ]
        await event.send(result)
        return rooms, player_rooms
    else:
        global op
        idx = players.index(rooms[room_id]['game']['current_bidder']) + op
        rooms[room_id]['game']['current_robber'] = players[(idx + 1) % 3]
        result = MessageChain()
        result.chain = [
            Plain("抢地主阶段：请问你是否选择抢地主？"),
            At(qq=rooms[room_id]['game']['current_robber']),  # At 消息发送者
            Plain("发送【/抢地主】抢地主。"),
            Plain("发送【/不抢】不抢地主。"),
        ]
        await event.send(result)
        return rooms, player_rooms

async def handle_play(event: AstrMessageEvent,cards_str:str,rooms, player_rooms):
    user_id = event.get_sender_id()
    group_id = event.get_group_id()
    room_id = group_id
    players = rooms[room_id]['players']
    flag = await check(event,rooms)
    if not flag:
        return rooms, player_rooms

    # 解析出牌
    parsed_cards = parse_cards(cards_str, rooms[room_id]['game']['hands'][user_id])
    if not parsed_cards:
        result = MessageChain()
        result.chain = [Plain("出牌无效！请检查牌型或是否拥有这些牌")]
        await event.send(result)
        return rooms, player_rooms
    # 获取牌型信息
    logger.warning(parsed_cards)
    play_type = validate_type(parsed_cards)
    logger.warning(play_type)
    if not play_type[0]:
        result = MessageChain()
        result.chain = [Plain("不合法的牌型！")]
        await event.send(result)
        return rooms, player_rooms

    # 验证是否符合出牌规则
    if rooms[room_id]['game']['last_played']:
        if play_type[0] in ['rocket']:
            result = MessageChain()
            result.chain = [Plain("火箭发射！")]
            await event.send(result)
        elif play_type[0] in ['bomb']:
            if rooms[room_id]['game']['last_played']['type'][0] in ['rocket'] or not compare_plays(rooms[room_id]['game']['last_played']['type'], play_type):
                result = MessageChain()
                result.chain = [Plain("出牌不够大！")]
                await event.send(result)
                return rooms, player_rooms
        else:
            if len(parsed_cards) != len(rooms[room_id]['game']['last_played']['cards']):
                result = MessageChain()
                result.chain = [Plain("出牌数量不一致！")]
                await event.send(result)
                return rooms, player_rooms
            if not compare_plays(rooms[room_id]['game']['last_played']['type'], play_type):
                result = MessageChain()
                result.chain = [Plain("出牌不够大！")]
                await event.send(result)
                return rooms, player_rooms

    # 执行出牌
    for c in parsed_cards:
        rooms[room_id]['game']['hands'][user_id].remove(c)
    rooms[room_id]['game']['last_played'] = {
        'player': user_id,
        'cards': parsed_cards,
        'type': play_type
    }
    result = MessageChain()
    result.chain = [Plain(f"{user_id} 出牌：{' '.join(parsed_cards)}")]
    await event.send(result)
    await lookcard(event,user_id,rooms,player_rooms)

    # 检查是否获胜否则计算下一个出牌人
    if not rooms[room_id]['game']['hands'][user_id]:
        if user_id == rooms[room_id]['game']['dizhu']:
            winners = [user_id]
            results = f"地主获胜！胜者：{winners}"
        else:
            winners = [p for p in players if p != rooms[room_id]['game']['dizhu']]
            results = f"农民获胜！胜者：{winners}"
        for p in players:
            player_rooms.pop(p, None)
        rooms.pop(room_id, None)
        result = MessageChain()
        result.chain = [Plain(f"游戏结束！{results}，房间已解散")]
        await event.send(result)
        return rooms, player_rooms
    else:
        idx = players.index(rooms[room_id]['game']['current_player'])
        next_players = players[idx+1:] + players[:idx+1]
        for p in next_players:
            if p != rooms[room_id]['game']['current_player'] and len(rooms[room_id]['game']['hands'][p]) > 0:
                rooms[room_id]['game']['current_player'] = p
                break
        result = MessageChain()
        result.chain = [
            Plain("轮到玩家:"),
            At(qq=rooms[room_id]['game']['current_player']),  # At 消息发送者
            Plain("发送【/出牌 []】出牌。"),
        ]
        await event.send(result)
        return rooms, player_rooms
async def handle_pass(event: AstrMessageEvent,rooms, player_rooms):
    user_id = event.get_sender_id()
    group_id = event.get_group_id()
    room_id = group_id
    players = rooms[room_id]['players']
    flag = await check(event,rooms)
    if not flag:
        return rooms, player_rooms
    if not rooms[room_id]['game']['last_played']:
        result = MessageChain()
        result.chain = [Plain("首出不能选择不出！")]
        await event.send(result)
        return rooms, player_rooms

    # 传递出牌权
    idx = players.index(rooms[room_id]['game']['current_player'])
    next_players = players[idx+1:] + players[:idx+1]
    for p in next_players:
        if p == rooms[room_id]['game']['last_played']['player']:
            # 一轮结束
            rooms[room_id]['game']['last_played'] = {}
            rooms[room_id]['game']['current_player'] = p
            result = MessageChain()
            result.chain = [
                Plain("新一轮开始，轮到玩家:"),
                At(qq=rooms[room_id]['game']['current_player']),  # At 消息发送者
                Plain("发送【/出牌 []】出牌。"),
            ]
            await event.send(result)
            return rooms, player_rooms
        if p != rooms[room_id]['game']['current_player'] and len(rooms[room_id]['game']['hands'][p]) > 0:
            rooms[room_id]['game']['current_player'] = p
            result = MessageChain()
            result.chain = [
                Plain("轮到玩家:"),
                At(qq=rooms[room_id]['game']['current_player']),  # At 消息发送者
                Plain("发送【/出牌 []】出牌。"),
            ]
            await event.send(result)
            return rooms, player_rooms
async def check(event: AstrMessageEvent,rooms):
    user_id = event.get_sender_id()
    group_id = event.get_group_id()
    room_id = group_id
    players = rooms[room_id]['players']
    if not room_id:
        result = MessageChain()
        result.chain = [Plain("没有游戏房间")]
        await event.send(result)
        return False
    if user_id not in players:
        result = MessageChain()
        result.chain = [Plain("你不在游戏中！")]
        await event.send(result)
        return False
    if rooms[room_id]['state'] != "playing":
        result = MessageChain()
        result.chain = [Plain("游戏尚未开始！")]
        await event.send(result)
        return False
    if rooms[room_id]['game']['current_player'] != user_id:
        result = MessageChain()
        result.chain = [Plain("现在不是你的回合！")]
        await event.send(result)
        return False
    return True
def validate_type(cards):
    values = [card_value(c) for c in cards]
    values.sort()
    count = len(values)
    value_counts = defaultdict(int)
    for v in values:
        value_counts[v] += 1
    # 火箭
    if set(cards) == {'BJ', 'RJ'}:
        return ('rocket', 17)

    # 炸弹
    if count == 4 and len(set(values)) == 1:
        return ('bomb', values[0])

    # 单牌
    if count == 1:
        return ('single', values[0])

    # 对子
    if count == 2 and len(set(values)) == 1:
        return ('pair', values[0])

    # 三张
    if count == 3 and len(set(values)) == 1:
        return ('triple', values[0])

    # 三带一
    if count == 4:
        counter = defaultdict(int)
        for v in values:
            counter[v] += 1
        if sorted(counter.values()) == [1, 3]:
            return ('triple_plus_single', max(k for k, v in counter.items() if v == 3))

    # 单顺（至少5张）
    if count >= 5 and all(values[i] == values[i - 1] + 1 for i in range(1, count)):
        if max(values) < 15:  # 2不能出现在顺子中
            return ('straight', max(values))

    if count == 5:  # 三带一对的情况
        triples = [v for v, cnt in value_counts.items() if cnt == 3]
        pairs = [v for v, cnt in value_counts.items() if cnt == 2]
        if len(triples) == 1 and len(pairs) == 1:
            return ('triple_plus_pair', triples[0])

    # 双顺（至少3对）
    if count >= 6 and count % 2 == 0:
        pairs = [values[i] for i in range(0, count, 2)]
        if all(pairs[i] == values[2 * i + 1] for i in range(len(pairs))) and \
                all(pairs[i] == pairs[i - 1] + 1 for i in range(1, len(pairs))) and \
                max(pairs) < 15:
            return ('double_straight', max(pairs))

    # 四带二
    if count == 6:
        counter = defaultdict(int)
        for v in values:
            counter[v] += 1
        if 4 in counter.values():
            quad_value = max(k for k, v in counter.items() if v == 4)
            return ('quad_plus_two', quad_value)

    # 飞机（至少2组三张）
    if count >= 6 and count % 3 == 0:
        triples = [values[i] for i in range(0, count, 3)]
        if all(triples[i] == triples[i - 1] for i in range(1, len(triples))) and \
                all(triples[i] == triples[i - 1] + 1 for i in range(1, len(triples))) and \
                max(triples) < 15:
            return ('airplane', max(triples))

    if count >= 6:
        # 找出所有可能的三张组合
        triple_values = sorted([v for v, cnt in value_counts.items() if cnt >= 3])
        # 寻找最长的连续三张序列
        max_sequence = []
        current_seq = []
        for v in triple_values:
            if not current_seq or v == current_seq[-1] + 1:
                current_seq.append(v)
            else:
                if len(current_seq) > len(max_sequence):
                    max_sequence = current_seq
                current_seq = [v]
            if v >= 15:  # 2和王不能出现在三顺中
                current_seq = []
                break
        if len(current_seq) > len(max_sequence):
            max_sequence = current_seq

        if len(max_sequence) >= 2:
            # 计算实际使用的三张牌
            used_triples = []
            for v in max_sequence:
                used_triples.extend([v] * 3)

            # 剩余牌必须是翅膀（单或对）
            remaining = []
            for v in values:
                if v in max_sequence and used_triples.count(v) > 0:
                    used_triples.remove(v)
                else:
                    remaining.append(v)

            # 翅膀数量必须等于三顺数量或两倍三顺数量
            if len(remaining) not in [len(max_sequence), 2 * len(max_sequence)]:
                return (None, 0)

            # 翅膀类型判断
            wing_counts = defaultdict(int)
            for v in remaining:
                wing_counts[v] += 1

            if len(remaining) == len(max_sequence):
                # 翅膀必须是单牌
                for v, cnt in wing_counts.items():
                    if cnt != 1:
                        return (None, 0)
            elif len(remaining) == 2 * len(max_sequence):
                # 翅膀必须是对子
                for v, cnt in wing_counts.items():
                    if cnt != 2:
                        return (None, 0)

            return ('airplane_with_wings', max(max_sequence))

    return (None, 0)


def compare_plays(last_type, new_type):
    """比较两次出牌的大小"""
    type_order = ['single', 'pair', 'triple', 'straight',
                  'double_straight', 'airplane', 'triple_plus_single',
                  'triple_plus_pair', 'quad_plus_two', 'bomb', 'rocket']

    # 特殊牌型比较
    if last_type[0] == 'rocket':
        return False
    if new_type[0] == 'rocket':
        return True
    if last_type[0] == 'bomb' and new_type[0] == 'bomb':
        return new_type[1] > last_type[1]
    if last_type[0] == 'bomb' and new_type[0] != 'bomb':
        return False
    if new_type[0] == 'bomb':
        return True
    # 普通牌型比较
    if last_type[0] != new_type[0]:
        return False
    return new_type[1] > last_type[1]


def parse_cards(input_str, hand):
    """
    解析简写输入并自动匹配花色
    示例输入："2223" -> 自动选择三个2和一个3的合法组合
    """
    # 转换输入为牌值列表
    card_values = convert_input(input_str)
    if not card_values:
        return None

    # 统计需求牌值
    required = defaultdict(int)
    for v in card_values:
        required[v] += 1

    # 获取手牌按牌值分类的候选牌
    candidates = group_by_value(hand)

    # 查找可能的组合
    matched = []
    for value, count in required.items():
        if value not in candidates or len(candidates[value]) < count:
            return None  # 牌值数量不足
        matched.append(candidates[value][:count])  # 优先取前面的花色

    # 展开组合并排序
    result = [card for group in matched for card in group]
    return sorted(result, key=card_value)

def convert_input(input_str):
    """将用户输入转换为标准牌值列表"""
    # 转换映射表
    convert_map = {
        'bj': 'BJ', 'rj': 'RJ',
        'j': 'J', 'q': 'Q', 'k': 'K', 'a': 'A',
        '0': '10', '1': '10',  # 处理10的特殊输入
        '2': '2', '3': '3', '4': '4', '5': '5',
        '6': '6', '7': '7', '8': '8', '9': '9'
    }

    values = []
    i = 0
    while i < len(input_str):
        char = input_str[i].lower()

        # 处理10的情况
        if char == '1' and i + 1 < len(input_str) and input_str[i + 1] in ('0', 'o'):
            values.append('10')
            i += 2
            continue
        if char == '0':
            values.append('10')
            i += 1
            continue

        # 处理特殊牌
        if char in ('小','大') and i + 1 < len(input_str):
            next_char = input_str[i + 1].lower()
            if char == '大' and next_char == '王':
                values.append('BJ')
                i += 2
                continue
            if char == '小' and next_char == '王':
                values.append('RJ')
                i += 2
                continue

        # 普通牌值转换
        converted = convert_map.get(char)
        if not converted:
            return None
        values.append(converted)
        i += 1

    return values

def group_by_value(hand):
    """将手牌按牌值分组"""
    groups = defaultdict(list)
    for card in hand:
        if card in ['BJ', 'RJ']:
            value = card
        value = card[1:] if card[0] in Poker.suits else card
        groups[value].append(card)
    # 按花色排序：♠ > ♥ > ♦ > ♣
    for v in groups.values():
        v.sort(key=lambda x: Poker.suits.index(x[0]) if x[0] in Poker.suits else 0)
    return groups