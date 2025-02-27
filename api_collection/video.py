from astrbot.api.all import *
import requests
urls1 = ''
def xjj():
    '''发送小姐姐视频/美女视频/抖音视频，当用户需要小姐姐视频，提到有关小姐姐，美女视频，小姐姐视频时调用此工具'''
    api_url = "https://api.kxzjoker.cn/API/Beautyvideo.php"
    params = {
        'type': 'json'
    }
    result = MessageChain()
    result.chain = []
    try:
        response = requests.get(api_url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析JSON数据
        result.chain = [Video.fromURL(data.get('download_url'))]
        return result
    except requests.exceptions.RequestException as e:
        result.chain = [Plain(f"请求出错: {e}")]
        return result

def search_bilibili_video(msg: str, n: str = "1"):
    '''根据用户提供的关键词搜索B站视频，用户需要搜索B站视频，提到有关搜索B站视频，B站视频时调用此工具
    Args:
        msg (string): 用户提供的关键词，如“少年”
        n (string): 返回结果的序号，默认为1
    '''
    url = "https://api.52vmy.cn/api/query/bilibili/video"
    # 请求参数
    params = {
        "msg": msg,
        "n": n
    }
    result = MessageChain()
    result.chain = []
    try:
        # 发送GET请求
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析返回的JSON数据
        if data:
            if data:
                result.chain.append(Plain(f"标题: {data.get('title', 'N/A')}\n"))
                result.chain.append(Plain(f"UP主: {data.get('user', 'N/A')}\n"))
                result.chain.append(Image.fromURL(data.get('img_url', 'N/A')))
                global urls1
                urls1 = data.get('url', 'N/A')
            else:
                result.chain.append(Plain("未找到相关视频，请尝试其他关键词。"))
            return result
        else:
            result.chain.append(Plain("未找到相关视频，请尝试其他关键词。"))
            return result
    except requests.exceptions.RequestException as e:
        result.chain.append(Plain(f"请求异常: {e}"))
        return result
def movie1():
    global urls1
    return urls1
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