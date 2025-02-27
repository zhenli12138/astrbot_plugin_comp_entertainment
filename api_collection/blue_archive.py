import urllib.request
from typing import List, Dict, Optional
from urllib.parse import quote
from astrbot.api.all import *
import os
import requests


class Baarchive:
    def __init__(self):
        self.base_url = "https://arona.diyigemt.com/api/v2/image"
        self.cdn_base = "https://arona.cdn.diyigemt.com/image"
        self.small_cdn_base = "https://arona.cdn.diyigemt.com/image/s"
        self.hash_file = "./data/plugins/astrbot_plugin_moreapi/hash.json"
        self.apt = "./data/plugins/astrbot_plugin_moreapi/"
        self.hash1 = {}
        self.data = {}

    def handle_blue_archive(self,text: str):
        '''根据用户提供的关键词进行碧蓝档案攻略查询，用户需要什么的碧蓝档案攻略，ba攻略，攻略，提到有关碧蓝档案攻略，ba攻略，攻略时调用此工具
        Args:text(string): 用户提供的关键词，比如‘国际服，可以模糊识别’'''
        self.load_game()
        params = {
            "name": text,
            "size": 8,
            "method": 3  # 默认使用混合搜索
        }
        result = MessageChain()
        result.chain = []
        # 调用API
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            api_data = response.json()
        except Exception as e:
            result.chain = [Plain(f"API请求异常：{str(e)}")]
            return result
        if not api_data:
            result.chain = [Plain("攻略查询服务暂不可用，请稍后再试")]
            return result
        if api_data["code"] == 200:
            # 精确匹配
            results = self.process_results(api_data['data'])
            if results:
                best_match = results[0]
                result.chain.append(Plain(f"找到精确匹配：{best_match['name']}\n"))
                if best_match['type'] == "image":
                    oldhash = self.hash1.get(best_match['name'], '')
                    local_path = best_match["file"]
                    if best_match["hash"] == oldhash and os.path.exists(local_path):
                        result.chain.append(Image.fromFileSystem(local_path))
                    else:
                        url = best_match["urls"]
                        # 对 URL 中的路径部分进行编码
                        parsed_url = urllib.parse.urlsplit(url)
                        encoded_path = quote(parsed_url.path)  # 编码路径部分
                        safe_url = urllib.parse.urlunsplit(
                            (parsed_url.scheme, parsed_url.netloc, encoded_path, parsed_url.query, parsed_url.fragment)
                        )
                        with urllib.request.urlopen(safe_url) as resp:
                            data = resp.read()
                        with open(local_path, "wb") as f:
                            f.write(data)
                        self.hash1[best_match['name']] = best_match['hash']
                        self.save_game()
                        result.chain.append(Image.fromURL(best_match["urls"]))  # 使用小图
                else:
                    result.chain.append(Plain(best_match["content"]))
        elif api_data["code"] == 101:
            # 模糊查询
            if not api_data["data"]:
                result.chain = [Plain("没有找到相关攻略")]
            results = self.process_results(api_data["data"])
            result.chain.append(Plain("找到以下相似结果：\n"))
            for idx, item in enumerate(results, 1):
                result.chain.append(Plain(f"{idx}. {item['name']}\n"))
                if item["type"] == "image":
                    oldhash = self.hash1.get(item['name'], '')
                    local_path = item["file"]
                    if item["hash"] == oldhash and os.path.exists(local_path):
                        result.chain.append(Image.fromFileSystem(local_path))
                    else:
                        url = item["urls"]
                        # 对 URL 中的路径部分进行编码
                        parsed_url = urllib.parse.urlsplit(url)
                        encoded_path = quote(parsed_url.path)  # 编码路径部分
                        safe_url = urllib.parse.urlunsplit(
                            (parsed_url.scheme, parsed_url.netloc, encoded_path, parsed_url.query, parsed_url.fragment)
                        )
                        with urllib.request.urlopen(safe_url) as resp:
                            data = resp.read()
                        with open(local_path, "wb") as f:
                            f.write(data)
                        self.hash1[item['name']] = item["hash"]
                        self.save_game()
                        result.chain.append(Image.fromURL(item["urls"]))  # 使用小图
                else:
                    result.chain.append(Plain(item["content"] + "\n"))
                result.chain.append(Plain("-" * 20 + "\n"))
            result.chain.append(Plain("请输入更精确的名称获取具体内容"))
        else:
            result.chain = [Plain(f"查询失败：{api_data.get('message', '未知错误')}")]
        return result


    def load_game(self):
        if os.path.exists(self.hash_file):
            with open(self.hash_file, 'r', encoding='utf-8') as f:
                self.hash1 = json.load(f)


    def save_game(self):
        with open(self.hash_file, 'w', encoding='utf-8') as f:
            json.dump(self.hash1, f, ensure_ascii=False, indent=4)


    def process_results(self, data: List[Dict]) -> List[Dict]:
        """处理API返回结果"""
        processed = []
        for item in data:
            if item["type"] == "file":
                processed.append({
                    "name": item["name"],
                    "hash": item["hash"],
                    "urls": f"{self.small_cdn_base}{item['content']}",
                    "file": f"{self.apt}{item['name']}.png",
                    "type": "image"
                })
            else:
                processed.append({
                    "name": item["name"],
                    "hash": item["hash"],
                    "content": item["content"],
                    "file": f"{self.apt}{item['name']}.png",
                    "type": "text"
                })
        return processed