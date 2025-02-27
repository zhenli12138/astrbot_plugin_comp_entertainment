from astrbot.api.all import *
import requests

def get_menu():
    # API地址
    api_url = "https://116.62.188.107:5000/images/menu"
    try:
        # 发送GET请求
        response = requests.get(api_url)
        # 将返回的图片内容保存到本地
        image_data = response.content
        menu_path = f"./data/plugins/astrbot_plugin_moreapi/menu_output.png"
        with open(menu_path, "wb") as file:
            file.write(image_data)
        result = MessageChain()
        result.chain = []
        result.chain = [Plain(f"MOREAPI菜单：\n"), Image.fromFileSystem(menu_path)]
        return result
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None