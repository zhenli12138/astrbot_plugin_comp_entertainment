from astrbot.api.all import *
import requests
from typing import Optional
def play_gobang(qq: str, group: str, type: str, x: Optional[str] = None, y: Optional[str] = None):
    # API地址
    url = "https://www.hhlqilongzhu.cn/api/gobang.php"
    # 请求参数
    params = {
        "qq": qq,
        "group": group,
        "type": type
    }
    # 如果type为3（下棋），添加x和y参数
    if type == "3":
        if x is None or y is None:
            return None
        params["x"] = x
        params["y"] = y
    try:
        # 发送GET请求
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析返回的JSON数据
        result = MessageChain()
        result.chain = []
        if data:
            if "img" in data:
                result.chain.append(Image.fromURL(data["img"]))
            if "text" in data:
                result.chain.append(Plain(f"{data['text']}\n"))
            if "play_chess" in data:
                result.chain.append(Plain(f"轮到下棋的玩家ID: {data['play_chess']}\n"))
            if "katsuya" in data and "defeat" in data:
                result.chain.append(Plain(f"游戏结束！获胜者ID: {data['katsuya']}, 失败者ID: {data['defeat']}\n"))
        elif type =='0':
            result.chain.append(Plain("五子棋游戏菜单：【/五子棋 <数字> x y】(1为加入,2为退出,3为下棋【此时须填xy坐标】,4为跳过)"))
        else:
            result.chain.append(Plain("五子棋游戏操作失败，请稍后再试。"))
        return result
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None