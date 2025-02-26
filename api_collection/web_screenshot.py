from astrbot.api.all import *
import requests

def get_webpage_screenshot(url):
    # API地址
    api_url = "https://api.pearktrue.cn/api/screenweb/"
    # 请求参数
    params = {
        "url": url,
        "type": "image",
    }
    try:
        # 发送GET请求
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # 检查请求是否成功\
        # 将返回的图片内容保存到本地
        image_data = response.content
        screenshot_path = f"./data/plugins/astrbot_plugin_moreapi/screenshot.png"
        with open(screenshot_path, "wb") as file:
            file.write(image_data)
        result = MessageChain()
        result.chain = []
        if screenshot_path:
            result.chain.append(Plain("截图结果：\n"))
            result.chain.append(Image.fromFileSystem(screenshot_path))
        else:
            result.chain.append(Plain("网页截图失败，请检查URL是否正确或稍后再试。"))
        return result
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None