from astrbot.api.all import *
import requests
def xjj():
    '''发送小姐姐视频/美女视频/抖音视频，当用户需要小姐姐视频，提到有关小姐姐，美女视频，小姐姐视频时调用此工具'''
    api_url = "https://api.kxzjoker.cn/API/Beautyvideo.php"
    params = {
        'type': 'json'
    }
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析JSON数据
        result = MessageChain()
        result.chain = []
        result.chain = [Video.fromURL(data.get('download_url'))]
        return result

    except requests.exceptions.RequestException as e:
        result = MessageChain()
        result.chain = []
        result.chain = [Plain(f"请求失败！\n")]
        print(f"请求出错: {e}")
        return result


'''
    url = "https://api.lolimi.cn/API/xjj/xjj.php"
    # 发送GET请求
    response = requests.get(url)
    # 检查请求是否成功
    if response.status_code == 200:
        data = response.content
        self.flag = 2
        with open(f"./data/plugins/astrbot_plugin_moreapi/xjj.mp4", "wb") as file:
            file.write(data)
        return f"./data/plugins/astrbot_plugin_moreapi/xjj.mp4"
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return None
        
elif self.flag == 2:
    result = event.make_result()
    result.chain = [Video.fromFileSystem(data)]
    return event.set_result(result)
'''