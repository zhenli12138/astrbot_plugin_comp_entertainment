from astrbot.api.all import *
import requests
from typing import Optional
def play_gobang(qq: str, group: str, type: str, x: Optional[str] = None, y: Optional[str] = None):
    # API地址
    '''五子棋游戏操作，用户需要五子棋游戏，提到有关五子棋时调用此工具
    Args:
        type (string): 指令(1为加入,2为退出,3为下棋,4为跳过,5为图片)
        x (string, optional): 下棋X坐标（type=3时必填）
        y (string, optional): 下棋Y坐标（type=3时必填）
    '''
    url = "https://www.hhlqilongzhu.cn/api/gobang.php"
    # 请求参数
    params = {
        "qq": qq,
        "group": group,
        "type": type
    }
    result = MessageChain()
    result.chain = []
    if type == '0':
        result.chain.append(Plain("五子棋游戏菜单：【/五子棋 <数字> x y】(1为加入,2为退出,3为下棋【此时须填xy坐标】,4为跳过)"))
        return result
    # 如果type为3（下棋），添加x和y参数
    if type == "3":
        if x is None or y is None:
            result.chain.append(Plain("请输入下棋位置参数，例如：【五子棋 3 8 8】"))
            return result
        params["x"] = x
        params["y"] = y
    try:
        # 发送GET请求
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析返回的JSON数据
        if data:
            if "img" in data:
                result.chain.append(Image.fromURL(data["img"]))
            if "text" in data:
                result.chain.append(Plain(f"{data['text']}\n"))
            if "play_chess" in data:
                result.chain.append(Plain(f"轮到下棋的玩家ID: {data['play_chess']}\n"))
            if "katsuya" in data and "defeat" in data:
                result.chain.append(Plain(f"游戏结束！获胜者ID: {data['katsuya']}, 失败者ID: {data['defeat']}\n"))
        else:
            result.chain.append(Plain("五子棋游戏操作失败，请稍后再试。"))
        return result
    except requests.exceptions.RequestException as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result