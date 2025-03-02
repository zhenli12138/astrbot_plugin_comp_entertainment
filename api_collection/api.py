from astrbot.api.all import *
import requests

def get_menu(menu_path):
    # API地址
    api_url = "http://116.62.188.107:5000/images/menu"
    try:
        # 发送GET请求
        response = requests.get(api_url)
        # 将返回的图片内容保存到本地
        image_data = response.content
        with open(menu_path, "wb") as file:
            file.write(image_data)
        result = MessageChain()
        result.chain = []
        result.chain = [Plain(f"MOREAPI菜单：\n"), Image.fromFileSystem(menu_path)]
        return result
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None
def get_hash():
    # API地址
    api_url = "http://116.62.188.107:5000/api/menu"
    # 发送GET请求
    response = requests.get(api_url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析返回的JSON数据
        data = response.json()
        return data.get("hash")
    else:
        return None
def get_version():
    # API地址
    api_url = "http://116.62.188.107:5000/api/version"
    # 发送GET请求
    response = requests.get(api_url)
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析返回的JSON数据
        data = response.json()
        return data.get("version")
    else:
        return None