from astrbot.api.all import *
import requests
def translate_text(msg):
    # 接口地址
    '''翻译用户提供的内容文字（翻译为英文）,当用户需要翻译，提到有关翻译什么时调用此工具
    Args:a(string): 用户提供的内容文字（即需要翻译的内容），可以模糊判断
    '''
    url = "https://api.lolimi.cn/API/qqfy/api.php"
    output_format = 'json'
    # 请求参数
    params = {
        'msg': msg,
        'type': output_format
    }
    # 发送GET请求
    response = requests.get(url, params=params)
    # 检查请求是否成功
    if response.status_code == 200:
        # 根据返回格式处理响应
        if output_format == 'json':
            data = response.json()
            result = MessageChain()
            result.chain = []
            result.chain = [Plain(f"翻译结果：{data['text']}")]
            return result   # 返回JSON格式的数据
        else:
            return response.text  # 返回纯文本格式的数据
    else:
        return f"请求失败，状态码: {response.status_code}"