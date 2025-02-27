from astrbot.api.all import *
import requests
def fetch_daily_tasks():
    '''发送光遇这个游戏的每日任务，当用户需要光遇任务，提到有关光遇，光遇任务时调用此工具'''
    task_type = "rw"  # rw是每日任务
    # 接口地址
    url = "https://api.lolimi.cn/API/gy/"
    # 请求参数
    params = {
        'type': task_type
    }
    # 发送GET请求
    response = requests.get(url, params=params)
    # 检查请求是否成功
    if response.status_code == 200:
        try:
            # 解析返回的JSON数据
            data = response.json()
            result = MessageChain()
            result.chain = []
            result.chain = [Plain(f"Nowtime: {data['nowtime']}\n")]
            # 打印每日任务
            for key, value in data.items():
                if key.isdigit():
                    result.chain.append(Plain(f"Task {key}: {value[0]}"))
                    result.chain.append(Image.fromURL(value[1]))
            return result
        except requests.exceptions.JSONDecodeError:
            print("Error: Response is not valid JSON.")
    else:
        logger.error(f"Failed to fetch data. Status code: {response.status_code}")