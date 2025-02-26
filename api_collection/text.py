from astrbot.api.all import *
import requests
def get_random_text():
    url = "https://api.lolimi.cn/API/yiyan/dz.php"
    try:
        response = requests.get(url)
        result = MessageChain()
        result.chain = []
        result.chain = [Plain(f"随机段子：{response.text}")]
        return result
    except requests.exceptions.RequestException as e:
        return f"请求失败: {e}"

def get_dujitang():
    url = "https://api.lolimi.cn/API/du/api.php"
    params = {
        "type": "json"  # 你可以根据需要选择返回格式，这里选择json
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析返回的JSON数据

        if data.get("code") == "1":
            result = MessageChain()
            result.chain = []
            result.chain = [Plain(f"毒鸡汤：{data.get("text")}")]
            return result
        else:
            return "Failed to retrieve dujitang."

    except requests.exceptions.RequestException as e:
        return f"An error occurred: {e}"
def movie():
    '''发送电影票房排行榜单,当用户需要电影票房排行榜单，提到有关电影票房时调用此工具'''
    # 接口地址
    url = "https://api.lolimi.cn/API/piao/dy.php"
    # 发送GET请求
    response = requests.get(url)
    if response.status_code == 200:
        data = response.content
        with open(f"./data/plugins/astrbot_plugin_moreapi/movie.txt", "wb") as file:
            file.write(data)
        data = f"./data/plugins/astrbot_plugin_moreapi/movie.txt"
        if os.path.exists(data):
            with open(data, 'r',encoding="utf-8") as file:
                text = file.read()
            result = MessageChain()
            result.chain = []
            result.chain = [Plain(text)]
            return result
    else:
        print(f"请求失败，状态码: {response.status_code}")