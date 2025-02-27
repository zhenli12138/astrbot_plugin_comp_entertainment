from astrbot.api.all import *
import requests
def fetch_image_url(search_term):
    # API接口地址
    '''对用户给出的关键词使用搜狗搜索引擎进行搜图操作，当用户需要搜图，提到有关搜索什么图片时调用此工具
    Args:a(string): 用户给出的关键词或用户提到的文字内容，可以模糊判断'''
    url = "https://api.lolimi.cn/API/sgst/api.php"
    response_type = 'json'
    # 请求参数
    params = {
        'msg': search_term,
        'type': response_type
    }
    # 发送GET请求
    response = requests.get(url, params=params)
    # 检查请求是否成功
    if response.status_code == 200:
        # 解析返回的JSON数据
        data = response.json()
        # 检查状态码
        if data.get('code') == 1:
            # 获取图片链接
            image_url = data['data']['url']
            result = MessageChain()
            result.chain = []
            result.chain = [Plain(f"{search_term}搜图结果:\n"), Image.fromURL(image_url)]
            return result
        else:
            print(f"获取失败: {data.get('text')}")
    else:
        print(f"请求失败，状态码: {response.status_code}")

def get_update_days(num):
    '''发送b站番剧更新表，当用户需要番剧更新列表，提到有关番剧，动画，动漫，b站番剧更新表或b站番剧时调用此工具
        Args:num(string): 用户需要发送的数量，如果用户没有明确指出，请设置为为5
    '''
    url = "https://api.lolimi.cn/API/B_Update_Days/api.php"
    return_type = 'json'
    params = {
        'num': num,
        'type': return_type
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['code'] == 1:
            data = data['data']
            result = MessageChain()
            result.chain = []
            for item in data:
                result.chain.append(Plain(f"Name: {item['Name']}\n"))
                result.chain.append(Image.fromURL(item['Picture']))
                result.chain.append(Plain(f"Update: {item['Update']}\n"))
                result.chain.append(Plain(f"Time: {item['Time']}\n"))
                result.chain.append(Plain(f"Url: {item['Url']}\n"))
                result.chain.append(Plain("------------------\n"))
            return result
        else:
            print(f"Error: {data['text']}")
            return
    else:
        print(f"Failed to fetch data. Status code: {response.status_code}")
        return
def get_weather(city):
    # API地址
    '''查询用户给出的地点的天气情况，当用户需要什么地方的天气，提到有关天气时调用此工具
    Args:a(string): 用户给出的地点，如北京/上海/重庆/深圳，等等，可以模糊判断'''
    url = "https://api.lolimi.cn/API/weather/api.php"
    # 请求参数
    params = {
        "city": city,
        "type": "json"  # 指定返回格式为JSON
    }
    try:
        # 发送GET请求
        response = requests.get(url, params=params)
        # 检查请求是否成功
        if response.status_code == 200:
            # 解析JSON响应
            data = response.json()
            # 检查返回的状态码
            if data.get("code") == 1:
                # 获取成功，返回数据
                data = data.get("data")
                result = MessageChain()
                result.chain = []
                if isinstance(data, dict):
                    result.chain.append(Plain(f"Weather Data for {data.get('city')}\n"))
                    result.chain.append(Plain(f"Temperature: {data.get('temp')}\n"))
                    result.chain.append(Plain(f"Weather: {data.get('weather')}\n"))
                    result.chain.append(Plain(f"Wind: {data.get('wind')}\n"))
                    result.chain.append(Plain(f"Wind Speed: {data.get('windSpeed')}\n"))
                    return result
                else:
                    print(data)
            else:
                # 获取失败，返回错误信息
                return f"Error: {data.get('text')}"
        else:
            # 请求失败，返回状态码
            return f"Request failed with status code: {response.status_code}"
    except Exception as e:
        # 捕获异常并返回错误信息
        return f"An error occurred: {str(e)}"
def get_baike_info(msg):
    '''根据用户提供的关键词查询百科内容，用户需要百科查询，需要查询什么具体的事务，提到有关百科，或者查询什么东西时调用此工具
    Args:msg(string): 用户提供的关键词，可以模糊判断'''
    # API地址
    url = "https://api.52vmy.cn/api/query/baike"
    # 请求参数
    params = {
        "msg": msg,
        "type": "json"  # 默认返回JSON格式
    }
    result = MessageChain()
    result.chain = []
    try:
        # 发送GET请求
        response = requests.get(url, params=params)
        response.raise_for_status()  # 检查请求是否成功
        data = response.json()  # 解析返回的JSON数据
        if data.get("code") == 200:
            result.chain.append(Plain(f"百科内容: {data['data'].get('text', 'N/A')}\n"))
            if data['data'].get('img_url'):
                result.chain.append(Image.fromURL(data['data']['img_url']))
            if data['data'].get('url'):
                result.chain.append(Plain(f"更多信息请访问: {data['data']['url']}"))
            return result
        else:
            print(f"获取失败: {data.get('msg', '未知错误')}")
            return None
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None
def get_baidu_tiku_answer(question):
    '''通过用户输入的问题对接百度题库进行回答，用户需要查询问题答案，提到有关题库、百度题库时调用此工具
    Args:
        question (string): 用户输入的问题，可以模糊判断
    '''
    # API地址
    url = "https://api.pearktrue.cn/api/baidutiku/"
    # 请求参数
    params = {
        "question": question
    }
    result = MessageChain()
    result.chain = []
    try:
        # 发送GET请求
        response = requests.get(url, params=params)
        data = response.json()  # 解析返回的JSON数据
        if data.get("code") == 200:
            result.chain.append(Plain(f"问题: {data['data'].get('question', 'N/A')}\n"))
            result.chain.append(Plain(f"选项: {', '.join(data['data'].get('options', []))}\n"))
            result.chain.append(Plain(f"答案: {data['data'].get('answer', 'N/A')}\n"))
            return result
        else:
            result.chain.append(Plain(f"查询失败: {data.get('msg', '未知错误')}"))
            return result
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
        return None