from astrbot.api.all import *
import requests
def movie():
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