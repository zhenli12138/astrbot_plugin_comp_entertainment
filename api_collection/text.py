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
            result.chain = [Plain(f"毒鸡汤：{data.get('text')}")]
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
def get_random_text2():
    '''发送一段温柔语录的文字内容，用户需要温柔语录，提到有关温柔语录时调用此工具'''
    url = "https://api.lolimi.cn/API/wryl/api.php"
    try:
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        result = MessageChain()
        result.chain = []
        result.chain = [Plain(f"温柔语录：{response.text}")]
        return result
    except requests.exceptions.RequestException as e:
        return f"请求失败: {e}"
def get_tv_show_heat_ranking():
    '''获取当前电视剧热度排行榜，用户需要电视剧排行榜，提到有关电视剧热度，电视剧排行，电视剧时调用此工具'''
    # API地址
    url = "https://api.52vmy.cn/api/wl/top/tv"
    # 请求参数
    params = {
        "type": "text"  # 默认返回JSON格式
    }
    result = MessageChain()
    result.chain = []
    try:
        # 发送GET请求
        response = requests.get(url,params=params)
        result.chain.append(Plain("当前电视剧热度排行榜：\n"))
        result.chain.append(Plain(response.text))
        return result
    except requests.exceptions.RequestException as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result