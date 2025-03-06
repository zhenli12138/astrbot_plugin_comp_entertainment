from astrbot.api.all import *
from typing import Dict, Any
import json
import datetime
import os
from typing import List, Dict, Optional
from typing import List, Dict
from data.plugins.astrbot_plugin_comp_entertainment.api_collection import pilcreate

class JsonlDatabase:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self._initialize_file()

    def _initialize_file(self):
        """确保数据文件存在"""
        if not os.path.exists(self.file_path):
            open(self.file_path, "a").close()

    async def _load_all(self) -> List[Dict]:
        """加载全部数据"""
        with open(self.file_path, "r") as f:
            return [json.loads(line) for line in f if line.strip()]

    async def _save_all(self, records: List[Dict]):
        """保存全部数据"""
        with open(self.file_path, "w") as f:
            for record in records:
                f.write(json.dumps(record) + "\n")

    async def get_user(self, user_id: str) -> Optional[Dict]:
        """获取完整用户记录"""
        records = await self._load_all()
        for record in records:
            if record.get("userid") == user_id:
                return record
        return None

    async def update_user(self, user_id: str, update_data: Dict):
        """更新用户记录（合并更新）"""
        records = await self._load_all()
        updated = False

        for record in records:
            if record.get("userid") == user_id:
                record.update(update_data)
                updated = True
                break

        if not updated:  # 新用户
            new_record = {"userid": user_id, **update_data}
            records.append(new_record)

        await self._save_all(records)


class ConfigManager:
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.default_config = {
            "currency": "鹿币",
            "maximum_helpsignin_times_per_day": 5,
            "enable_deerpipe": True,
            "Reset_Cycle": "每月",
            "cost": {
                "checkin_reward": {
                    "鹿": {"cost": 100},
                    "鹿@用户": {"cost": 100},
                    "补鹿": {"cost": -100},
                    "戒鹿": {"cost": -100},
                },
                "store_item": [
                    {"item": "锁", "cost": -50},
                    {"item": "钥匙", "cost": -250},
                ],
            },
        }
        self.config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if not os.path.exists(self.config_file):
            return self.default_config

        with open(self.config_file, "r") as f:
            for line in f:
                return {**self.default_config, ** json.loads(line.strip())}
        return self.default_config

    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)

# 在插件中使用 ConfigManager
class Deer:
    def __init__(self):
        super().__init__()
        self.config = ConfigManager("./data/plugins/astrbot_plugin_comp_entertainment/config.jsonl")  # 初始化配置管理器
        # 初始化配置参数
        self.currency = self.config.get("currency", "鹿币")
        self.max_help_times = self.config.get("maximum_helpsignin_times_per_day", 5)
        #self.enable_deerpipe = self.config_manager.get("enable_deerpipe", False)
        self.reset_cycle = self.config.get("Reset_Cycle", "每月")
        self.cost_table = self.config.get("cost", {})
        # 初始化数据库和货币管理器
        self.database = JsonlDatabase("./data/plugins/astrbot_plugin_comp_entertainment/deerpipe.jsonl")
    async def create_user_record(self, user_id: str, user_name: str) -> Dict:
        """获取或创建用户记录（包含货币字段）"""
        user = await self.database.get_user(user_id)
        if not user:
            default_record = {
                "username": user_name,
                "recordtime": datetime.datetime.now().strftime("%Y-%m"),
                "checkindate": [],
                "helpsignintimes": "",
                "totaltimes": 0,
                "allowHelp": True,
                "itemInventory": [],
                "value": 0
            }
            await self.database.update_user(user_id, default_record)
            return default_record
        return user
    '''-------------------------------------------------------------'''
    async def get_user_record(self, user_id: str) -> Dict:
        '''获取用户记录'''
        record = await self.database.get_user(user_id)
        return record if record else None
    async def modify_currency(self, user_id: str, amount: int):
        """修改用户余额"""
        user = await self.database.get_user(user_id)
        if user:
            new_value = user.get("value", 0) + amount
            await self.database.update_user(user_id, {"value": new_value})
    async def get_currency(self, user_id: str) -> int:
        """获取用户余额"""
        user = await self.database.get_user(user_id)
        return user.get("value", 0) if user else 0

    async def parse_target(self, event):
        """解析@目标或用户名"""
        for comp in event.message_obj.message:
            if isinstance(comp, At) and event.get_self_id() != str(comp.qq):
                return str(comp.qq)
            else:
                return None

    async def reset_user_record(self, user_id: str,recordtime: str):
        '''重置用户记录（保留货币和道具）'''
        await self.database.update_user(user_id, {
            "recordtime": recordtime,
            "checkindate": [],
            "helpsignintimes": "",
            "totaltimes": 0,
            # 注意：不重置以下字段
            # "value": 保留原有余额
            # "itemInventory": 保留道具
            # "allowHelp": 保留原有设置
        })
    '''-------------------------------------------------------------'''
    async def view_calendar(self, event: AstrMessageEvent):
        '''查看用户签到日历'''
        user_id = event.get_sender_id()
        user_name = event.get_sender_name()

        current_date = datetime.datetime.now()
        year = current_date.year
        month = current_date.month

        record = await self.get_user_record(user_id)
        if not record:
            result = MessageChain()
            result.chain = [Plain("未找到该用户的签到记录。")]
            await event.send(result)
            return

        calendar_image = await pilcreate.render_sign_in_calendar(record, year, month, user_name)
        result = MessageChain()
        result.chain = [Image.fromFileSystem(calendar_image)]
        await event.send(result)
        '''-------------------------------------------------------------'''
    async def get_sign_in_record(self, record: Dict, day: int):
        '''检查签到次数是否达到上限'''
        day_record = next((d for d in record["checkindate"] if d.startswith(f"{day}=")), None)
        if day_record:
            count = int(day_record.split("=")[1])
            return count
        else:
            return 0

    async def update_sign_in_record(self, record: Dict, day: int):
        '''更新签到记录'''
        user_id = record["userid"]
        day_record = next((d for d in record["checkindate"] if d.startswith(f"{day}=")), None)
        # 更新签到数据
        new_checkindate = record["checkindate"].copy()
        if day_record:
            count = int(day_record.split("=")[1]) + 1
            new_checkindate.remove(day_record)
            new_checkindate.append(f"{day}={count}")
        else:
            new_checkindate.append(f"{day}=1")

        # 只更新必要字段
        await self.database.update_user(user_id, {
            "checkindate": new_checkindate,
            "totaltimes": record["totaltimes"] + 1
        })
    async def cancel_sign_in_on_day(self, record: Dict, day: int):
        '''取消某日签到'''
        user_id = record["userid"]
        day_record = next((d for d in record["checkindate"] if d.startswith(f"{day}=")), None)

        if day_record:
            new_checkindate = [d for d in record["checkindate"] if d != day_record]
            await self.database.update_user(user_id, {
                "checkindate": new_checkindate,
                "totaltimes": record["totaltimes"] - 1
            })
    async def deer_sign_in(self, event: AstrMessageEvent):
        """核心签到逻辑"""
        '''鹿管签到'''
        user_id = event.get_sender_id()
        user_name = event.get_sender_name()
        current_date = datetime.datetime.now()
        year = current_date.year
        month = current_date.month
        day = current_date.day
        #
        record = await self.get_user_record(user_id)
        if not record:
            record = await self.create_user_record(user_id, user_name)
        #
        if self.reset_cycle == "每月" and record["recordtime"] != f"{year}-{month}":
            await self.reset_user_record(user_id,f"{year}-{month}")
            record = await self.get_user_record(user_id)
        #
        times = await self.get_sign_in_record(record, day)
        if times >= 3:
            result = MessageChain()
            result.chain = [Plain("今天已经鹿过3次了，给牛牛放个假，请明天再鹿吧~")]
            await event.send(result)
            return
        #
        await self.update_sign_in_record(record, day)
        times = await self.get_sign_in_record(record, day)
        reward = self.cost_table["checkin_reward"]["鹿"]["cost"]
        await self.modify_currency(user_id, reward)
        currency = await self.get_currency(user_id)
        #
        result = MessageChain()
        result.chain = [Plain(
            f"你今天已经鹿了 {times} 次啦~ 继续加油咪~\n本次签到获得 {self.cost_table['checkin_reward']['鹿']['cost']} 个 {self.currency}。\n当前您总共拥有 {currency} 个 {self.currency}")]
        await event.send(result)
        #
        await self.view_calendar(event)

    async def resign(self, event: AstrMessageEvent, day: int):
        '''补签某日'''
        user_id = event.get_sender_id()
        current_date = datetime.datetime.now()
        year = current_date.year
        month = current_date.month
        record = await self.get_user_record(user_id)
        if not record:
            result = MessageChain()
            result.chain = [Plain("暂无鹿管记录哦，快去【鹿】吧~")]
            await event.send(result)
            return
        if day < 1 or day > 31 or day > current_date.day:
            result = MessageChain()
            result.chain = [Plain("日期不正确或未到，请输入有效的日期。\n示例：【补鹿 1】")]
            await event.send(result)
            return
        #
        times = await self.get_sign_in_record(record, day)
        if times >= 3:
            result = MessageChain()
            result.chain = [Plain("指定日期已经鹿过3次了，不能再补鹿了！")]
            await event.send(result)
            return
        #

        await self.update_sign_in_record(record, day)
        reward = self.cost_table["checkin_reward"]["补鹿"]["cost"]
        await self.modify_currency(user_id, reward)
        currency = await self.get_currency(user_id)

        result = MessageChain()
        result.chain = [Plain(f"你已成功补签{day}号。{self.currency} 变化：{self.cost_table['checkin_reward']['补鹿']['cost']}。\n当前您总共拥有 {currency} 个 {self.currency}")]
        await event.send(result)
        await self.view_calendar(event)

    async def cancel_sign_in(self, event: AstrMessageEvent, day: Optional[int] = None):
        '''取消某日签到'''
        user_id = event.get_sender_id()
        current_date = datetime.datetime.now()
        day = day if day else current_date.day

        record = await self.get_user_record(user_id)
        if not record:
            result = MessageChain()
            result.chain = [Plain("你没有签到记录。")]
            await event.send(result)
            return

        if day < 1 or day > 31 or day > current_date.day:
            result = MessageChain()
            result.chain = [Plain("日期不正确，请输入有效的日期。\n示例：【戒鹿 1】")]
            await event.send(result)
            return

        times = await self.get_sign_in_record(record, day)
        if times <= 0:
            result = MessageChain()
            result.chain = [Plain(f"你没有在{day}号签到。")]
            await event.send(result)
            return

        await self.cancel_sign_in_on_day(record, day)
        reward = self.cost_table["checkin_reward"]["戒鹿"]["cost"]
        await self.modify_currency(user_id, reward)

        result = MessageChain()
        result.chain = [Plain(f"你已成功取消{day}号的签到。点数变化：{self.cost_table['checkin_reward']['戒鹿']['cost']}")]
        await event.send(result)
        await self.view_calendar(event)
    async def help_sign_in(self, event: AstrMessageEvent):
        """帮助签到"""
        user_id = event.get_sender_id()
        target_user_id = await self.parse_target(event)
        if not target_user_id:
            result = MessageChain()
            result.chain = [Plain("请指定要帮鹿管的用户【帮鹿@xx】")]
            await event.send(result)
            return
        target_user_name = 'CESHI'
        current_date = datetime.datetime.now()
        year = current_date.year
        month = current_date.month
        day = current_date.day
        #
        if str(target_user_id) == event.get_self_id():
            await event.send(MessageChain([Plain("请@需要帮助的用户，不能自己帮自己鹿哦，自己鹿请发送【鹿】")]))
            return
        #
        record = await self.get_user_record(target_user_id)
        if not record:
            record = await self.create_user_record(target_user_id, target_user_name)
        #
        if self.reset_cycle == "每月" and record["recordtime"] != f"{year}-{month}":
            await self.reset_user_record(target_user_id,f"{year}-{month}")
            record = await self.get_user_record(target_user_id)
        #
        if not record["allowHelp"]:
            result = MessageChain()
            result.chain = [Plain("TA的牛牛带了锁，你帮不了TA鹿管了")]
            await event.send(result)
            return
        #
        times = await self.get_sign_in_record(record, day)
        if times >= 3:
            result = MessageChain()
            result.chain = [Plain("TA今天已经鹿过3次了，给好兄弟的牛牛放个假，明天再帮TA鹿吧~")]
            await event.send(result)
            return
        #
        if await self.is_help_sign_in_limit_reached(user_id, day):
            result = MessageChain()
            result.chain = [Plain("你今天已经帮助别人签到达到上限，无法继续帮助~")]
            await event.send(result)
            return

        # 执行帮助操作
        await self.update_sign_in_record(record, day)
        reward = self.cost_table["checkin_reward"]["鹿"]["cost"]
        await self.modify_currency(target_user_id, reward)
        reward = self.cost_table["checkin_reward"]["鹿@用户"]["cost"]
        await self.modify_currency(user_id, reward)
        currency = await self.get_currency(user_id)
        #
        times = await self.get_sign_in_record(record, day)
        result = MessageChain()
        result.chain = [Plain(
            f"你成功帮助 {target_user_name} 鹿管！他今天已经鹿了 {times} 次了！您获得 {self.cost_table['checkin_reward']['鹿@用户']['cost']} 个 {self.currency}。\n当前您总共拥有 {currency} 个 {self.currency}")]
        await event.send(result)

    async def is_help_sign_in_limit_reached(self, user_id: str, day: int) -> bool:
        record = await self.get_user_record(user_id)
        if not record:
            return False
        helpsignintimes = record.get("helpsignintimes", "")
        if helpsignintimes:
            helpsignintimes_dict = dict(entry.split("=") for entry in helpsignintimes.split(",") if "=" in entry)
            day_count = int(helpsignintimes_dict.get(str(day), 0))
            return day_count >= self.max_help_times
        return False
    '''------------------------------------------------------------------------'''
    async def get_leader_records(self) -> List[Dict]:
        records = []
        try:
            with open("deerpipe.jsonl", "r") as f:
                for line in f:
                    record = json.loads(line.strip())
                    records.append(record)
            current_month = datetime.datetime.now().month
            current_year = datetime.datetime.now().year
            valid_records = [record for record in records if
                             record["recordtime"] == f"{current_year}-{current_month}" and record["totaltimes"] > 0]
            valid_records.sort(key=lambda x: x["totaltimes"], reverse=True)
            return valid_records
        except FileNotFoundError:
            # 如果文件不存在，返回空列表
            return []

    async def leaderboard(self, event: AstrMessageEvent):
        '''查看签到排行榜'''
        current_month = datetime.datetime.now().month
        top_records = await self.get_leader_records()
        leaderboard_image = await pilcreate.render_leaderboard(top_records, current_month)
        result = MessageChain()
        result.chain = [Image.fromURL(leaderboard_image)]
        await event.send(result)

    async def toggle_lock(self, event: AstrMessageEvent):
        '''允许/禁止别人帮你鹿'''
        user_id = event.get_sender_id()
        record = await self.get_user_record(user_id)
        if not record:
            result = MessageChain()
            result.chain = [Plain("用户未找到，请先进行签到。")]
            await event.send(result)
            return

        if "锁" not in record["itemInventory"]:
            result = MessageChain()
            result.chain = [Plain("你没有道具【锁】，无法执行此操作。\n请使用指令：购买 锁")]
            await event.send(result)
            return

        record["allowHelp"] = not record["allowHelp"]
        record["itemInventory"].remove("锁")
        await self.database.update_user(user_id, record)

        status = "允许" if record["allowHelp"] else "禁止"
        result = MessageChain()
        result.chain = [Plain(f"你已经{status}别人帮助你鹿管。")]
        await event.send(result)

    async def use_item(self, event: AstrMessageEvent, item_name: str):
        """
        使用道具

        参数:
            item_name (str): 道具名称
        """
        user_id = event.get_sender_id()

        # 获取用户记录
        record = await self.get_user_record(user_id)
        if not record:
            result = MessageChain()
            result.chain = [Plain("未找到你的签到记录。")]
            await event.send(result)
            return

        # 检查用户是否拥有该道具
        if "itemInventory" not in record or item_name not in record["itemInventory"]:
            result = MessageChain()
            result.chain = [Plain(f"你没有道具：{item_name}。")]
            await event.send(result)
            return

        # 执行道具效果
        if item_name == "钥匙":
            # 使用钥匙强制帮助签到
            target_user_id = await self.parse_target(event)
            if not target_user_id:
                result = MessageChain()
                result.chain = [Plain("请指定要帮助的用户。")]
                await event.send(result)
                return

            # 调用帮助签到逻辑
            await self.help_sign_in(event)

            # 移除道具
            record["itemInventory"].remove(item_name)
            await self.database.update_user(user_id, record)

            result = MessageChain()
            result.chain = [Plain(f"你使用了【钥匙】强制帮 {target_user_id} 鹿管。")]
            await event.send(result)
        else:
            result = MessageChain()
            result.chain = [Plain(f"道具 {item_name} 暂无使用效果。")]
            await event.send(result)

    async def buy_item(self, event: AstrMessageEvent, item_name: str):
        """道具购买系统"""
        user_id = event.get_sender_id()
        user = await self.database.get_user(user_id)

        # 查找商品
        item_info = next(
            (item for item in self.cost_table["store_item"] if item["item"] == item_name),
            None
        )

        if not item_info:
            await event.send(MessageChain([Plain("没有这个商品哦~")]))
            return

        cost = abs(item_info["cost"])
        if user["value"] < cost:
            await event.send(MessageChain([Plain(f"余额不足，需要 {cost} {self.currency}")]))
            return

        # 扣款并添加道具
        await self.modify_currency(user_id, -cost)
        new_items = user["itemInventory"] + [item_name]
        await self.database.update_user(user_id, {"itemInventory": new_items})

        await event.send(MessageChain([
            Plain(f"成功购买 {item_name}！"),
            Plain(f"当前余额：{user['value'] - cost} {self.currency}")
        ]))