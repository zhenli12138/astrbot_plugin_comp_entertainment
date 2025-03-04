import re
from astrbot.api.all import *
import aiohttp

async def get_random_text():
    url = "https://api.lolimi.cn/API/yiyan/dz.php"
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    result.chain = [Plain(f"随机段子：{text}")]
                    return result
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result

async def get_dujitang():
    url = "https://api.lolimi.cn/API/du/api.php"
    params = {"type": "json"}
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get("code") == "1":
                        result.chain = [Plain(f"毒鸡汤：{data.get('text')}")]
                        return result
                    else:
                        result.chain = [Plain("Failed to retrieve dujitang.")]
                        return result
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result

async def movie():
    url = "https://api.lolimi.cn/API/piao/dy.php"
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    data = await response.read()
                    file_path = "./data/plugins/astrbot_plugin_comp_entertainment/movie.txt"
                    with open(file_path, "wb") as file:
                        file.write(data)
                    with open(file_path, 'r', encoding="utf-8") as file:
                        text = file.read()
                    result.chain = [Plain(text)]
                    return result
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result

async def get_random_text2():
    url = "https://api.lolimi.cn/API/wryl/api.php"
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    text = await response.text()
                    result.chain = [Plain(f"温柔语录：{text}")]
                    return result
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result

async def get_tv_show_heat_ranking():
    url = "https://api.52vmy.cn/api/wl/top/tv"
    params = {"type": "text"}
    result = MessageChain()
    result.chain = []
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                if response.status == 200:
                    text = await response.text()
                    result.chain = [Plain("当前电视剧热度排行榜：\n"), Plain(text)]
                    return result
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result

async def translate_text(msg):
    url = "https://api.lolimi.cn/API/qqfy/api.php"
    output_format = 'json'
    # 请求参数
    params = {
        'msg': msg,
        'type': output_format
    }

    result = MessageChain()
    result.chain = []
    try:
        # 使用 aiohttp 发送异步 GET 请求
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                # 检查请求是否成功
                if response.status == 200:
                    # 根据返回格式处理响应
                    if output_format == 'json':
                        data = await response.json()
                        result.chain = [Plain(f"翻译结果：{data['text']}")]
                        return result  # 返回JSON格式的数据
                    else:
                        text = await response.text()
                        result.chain = [Plain(text)]
                        return result  # 返回纯文本格式的数据
                else:
                    result.chain = [Plain(f"请求失败，状态码: {response.status}")]
                    return result
    except aiohttp.ClientError as e:
        result.chain = [Plain(f"请求异常: {e}")]
        return result
async def remove_complex_emoticons(text):
    pattern = r"""
            \([^()]+\)              # 匹配括号内的复杂颜表情
            |                       # 或
            [^\u4e00-\u9fff，。？！、]  # 匹配非中文、非标点符号、非空格的字符
    """
    regexs = re.compile(pattern, re.VERBOSE)
    cleaned_text = regexs.sub('', text)
    return cleaned_text
