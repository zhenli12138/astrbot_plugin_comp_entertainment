import aiohttp
import calendar
from typing import List, Dict
from astrbot.api.all import *
from PIL import Image, ImageDraw, ImageFont, ImageOps
from datetime import datetime as Pdatetime
class Poker:
    suits = ['♠', '♥', '♦', '♣']
    values = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
    specials = ['BJ', 'RJ']
    colors = {'♠': (0, 0, 0), '♥': (255, 0, 0),
              '♦': (255, 0, 0), '♣': (0, 0, 0)}
from PIL import Image, ImageDraw, ImageFont

async def generate_menu():
    # 背景图片路径
    background_image_path = './data/plugins/astrbot_plugin_comp_entertainment/background.jpg'
    if background_image_path:
        img = Image.open(background_image_path).convert('RGBA')
        img = img.resize((800, 600))  # 调整底图大小
    else:
        img = Image.new('RGB', (800, 600), (73, 109, 137))

    # 创建一个透明的图层用于绘制菜单
    overlay = Image.new('RGBA', img.size, (255, 255, 255, 0))
    d = ImageDraw.Draw(overlay)

    # 使用更美观的字体
    font = ImageFont.truetype('./data/plugins/astrbot_plugin_comp_entertainment/msyh.ttf', 28)
    shadow_font = ImageFont.truetype('./data/plugins/astrbot_plugin_comp_entertainment/msyh.ttf', 28)

    # 菜单内容
    menu = [
        "/创建房间",
        "/加入房间",
        "/退出房间",
        "/开始游戏",
        "/抢地主",
        "/出牌 [牌组]",
        "/pass（不出牌）",
        "【自动发牌，请查看私聊】",
        "/结束游戏（强制结束游戏）",
        "ps：指令不用打斜杠也可以"
    ]

    # 绘制圆角矩形背景
    background_box = [50, 50, 750, 550]  # 圆角矩形的位置和大小
    d.rounded_rectangle(background_box, radius=15, fill=(255, 255, 255, 178))  # 半透明白色背景

    # 绘制标题
    title = "【斗地主游戏菜单】"
    d.text((102, 62), title, fill=(0, 0, 0, 128), font=shadow_font)  # 阴影
    d.text((100, 60), title, fill=(255, 255, 0), font=font)  # 黄色标题

    # 绘制菜单内容
    y = 120  # 起始纵坐标
    for line in menu:
        # 绘制阴影
        d.text((102, y + 2), line, fill=(0, 0, 0, 128), font=shadow_font)
        # 绘制文本
        d.text((100, y), line, fill=(255, 105, 180), font=font)  # 粉色菜单内容
        y += 40  # 每行间距

    # 将菜单图层与底图合并
    img = Image.alpha_composite(img.convert('RGBA'), overlay)
    img = img.convert('RGB')  # 转换回RGB模式以便保存为PNG

    # 保存图片
    output_path = f"./data/plugins/astrbot_plugin_comp_entertainment/ddz.png"
    img.save(output_path, format='PNG')
    return output_path

async def generate_hand_image(cards,idx):
    font = './data/plugins/astrbot_plugin_comp_entertainment/msyh.ttf'
    card_width = 80
    card_height = 120
    spacing = 50
    img = Image.new('RGB', (max(card_width + (len(cards) - 1) * spacing, 500), 200), (56, 94, 15))
    d = ImageDraw.Draw(img)
    text = "【斗地主手牌】"
    bbox = d.textbbox((0, 0), text, font=ImageFont.truetype(font, 50))
    text_width = bbox[2] - bbox[0]  # 文本宽度
    x = (img.width - text_width) / 2  # 水平居中
    d.text((x, 0), text, fill=(0, 0, 0), font=ImageFont.truetype(font, 50))
    for i, card in enumerate(cards):
        if card in ['BJ', 'RJ']:
            color = (255, 0, 0) if card == 'BJ' else (0, 0, 0)
            card_img = Image.new('RGB', (card_width, card_height), (255, 255, 255))
            d = ImageDraw.Draw(card_img)
            x, y = 10, 0
            for char in 'JOKER':
                # 获取字符的边界框
                bbox = d.textbbox((x, y), char, font=ImageFont.truetype(font, 20))
                char_width, char_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
                # 绘制字符
                d.text((x, y), char, fill=color, font=ImageFont.truetype(font, 20))
                # 调整 y 坐标
                y += char_height + 5
        else:
            suit = card[0]
            value = card[1:]
            card_img = Image.new('RGB', (card_width, card_height), (255, 255, 255))
            d = ImageDraw.Draw(card_img)
            d.text((5, 60), suit, fill=Poker.colors[suit], font=ImageFont.truetype('arial.ttf', 50))
            d.text((5, 0), value, fill=(0, 0, 0), font=ImageFont.truetype(font, 40))
        border_width = 1
        border_color = (0, 0, 0)  # 红色边框
        bordered_img = ImageOps.expand(card_img, border=border_width, fill=border_color)
        img.paste(bordered_img, (i * spacing, 80))

    output_path = f"./data/plugins/astrbot_plugin_comp_entertainment/pic{idx}.png"
    img.save(output_path, format='PNG')
    return output_path

async def render_leaderboard(records: List[Dict], month: int) -> str:
    """
    渲染排行榜并返回图片的 URL。
    使用外部 API 将 HTML 模板渲染为图片。
    """
    # 定义 HTML 模板
    TMPL = '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>鹿管排行榜</title>
    <style>
    body {
    font-family: 'Microsoft YaHei', Arial, sans-serif;
    background-color: #f0f4f8;
    margin: 0;
    padding: 20px;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    }
    .container {
    background-color: white;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    padding: 30px;
    width: 100%;
    width: 500px;
    }
    h1 {
    text-align: center;
    color: #2c3e50;
    margin-bottom: 30px;
    font-size: 28px;
    }
    .ranking-list {
    list-style-type: none;
    padding: 0;
    margin: 0;
    }
    .ranking-item {
    display: flex;
    align-items: center;
    padding: 15px 10px;
    border-bottom: 1px solid #ecf0f1;
    transition: background-color 0.3s;
    }
    .ranking-item:hover {
    background-color: #f8f9fa;
    }
    .ranking-number {
    font-size: 18px;
    font-weight: bold;
    margin-right: 15px;
    min-width: 30px;
    color: #7f8c8d;
    }
    .medal {
    font-size: 24px;
    margin-right: 15px;
    }
    .name {
    flex-grow: 1;
    font-size: 18px;
    }
    .channels {
    font-size: 14px;
    color: #7f8c8d;
    margin-left: 10px;
    }
    .count {
    font-weight: bold;
    color: #e74c3c;
    font-size: 18px;
    }
    .count::after {
    content: ' 次';
    font-size: 14px;
    color: #95a5a6;
    }
    </style>
    </head>
    <body>
    <div class="container">
    <h1>🦌 {{ month }}月鹿管排行榜 🦌</h1>
    <ol class="ranking-list">
    {% for record in records %}
    <li class="ranking-item">
    <span class="ranking-number">{{ loop.index }}</span>
    {% if loop.index == 1 %}<span class="medal">🥇</span>{% endif %}
    {% if loop.index == 2 %}<span class="medal">🥈</span>{% endif %}
    {% if loop.index == 3 %}<span class="medal">🥉</span>{% endif %}
    <span class="name">{{ record.username }}</span>
    <span class="count">{{ record.totaltimes }}</span>
    </li>
    {% endfor %}
    </ol>
    </div>
    </body>
    </html>
    '''
    render_data = {
        "month": month,
        "records": records,
    }
    payload = {
    "tmpl": TMPL,
    "render_data": render_data,
    "width": 500,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
                "http://116.62.188.107:8000/render",
                json=payload
        ) as response:
            return (await response.json())["url"]

async def render_sign_in_calendar(record: Dict, year: int, month: int, user_name: str) -> str:
    """
    渲染签到日历为图片，并返回图片的 Base64 编码
    参数:
        record (Dict): 用户签到记录
        year (int): 年份
        month (int): 月份
        user_name (str): 用户名
    """
    # 获取签到记录
    checkindate = record.get("checkindate", [])
    checkin_days = set()
    for entry in checkindate:
        if "=" in entry:
            day, _ = entry.split("=")
            checkin_days.add(int(day))
        else:
            checkin_days.add(int(entry))

    # 生成日历
    cal = calendar.monthcalendar(year, month)
    month_name = calendar.month_name[month]
    month_name = Pdatetime.strptime(month_name, '%B').month
    # 创建图片
    cell_size = 50
    padding = 20
    width = cell_size * 7 + padding * 2
    height = cell_size * (len(cal) + 1) + padding * 3
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    # 加载字体
    try:
        font = ImageFont.truetype("./data/plugins/astrbot_plugin_test/MiSans-Regular.ttf", 16)
    except IOError:
        font = ImageFont.load_default()

    # 绘制标题
    title = f"{year}-{month_name}  鹿了\n{user_name}"
    bbox = draw.textbbox((0, 0), title, font=font)  # 获取文本的边界框
    title_width = bbox[2] - bbox[0]  # 计算文本宽度
    title_height = bbox[3] - bbox[1]  # 计算文本高度
    draw.text((10, padding), title, fill="black", font=font)

    # 绘制星期标题
    weekdays = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    for i, day in enumerate(weekdays):
        x = padding + i * cell_size
        y = padding + title_height + 10
        draw.text((x, y), day, fill="black", font=font)

    # 加载背景图片和签到标记图片
    day_bg_path = "./data/plugins/astrbot_plugin_test/day.png"
    check_mark_path = "./data/plugins/astrbot_plugin_test/check.png"

    if not os.path.exists(day_bg_path) or not os.path.exists(check_mark_path):
        raise FileNotFoundError("背景图片或签到标记图片未找到。")

    day_bg = Image.open(day_bg_path).resize((cell_size, cell_size))
    check_mark = Image.open(check_mark_path).resize((cell_size, cell_size))

    # 绘制日历
    for week_idx, week in enumerate(cal):
        for day_idx, day in enumerate(week):
            if day == 0:
                continue  # 跳过空白日期
            x = padding + day_idx * cell_size
            y = padding + title_height + 40 + week_idx * cell_size

            # 绘制背景图片
            image.paste(day_bg, (x, y))

            # 绘制日期
            draw.text((x + 10, y + 10), str(day), fill="black", font=font)

            # 标记已签到日期
            if day in checkin_days:
                image.paste(check_mark, (x, y), check_mark)

    # 将图片保存为 Base64 编码
    save_path = "./data/plugins/astrbot_plugin_test/calendar.png"  # 请替换为实际的保存路径和文件名
    image.save(save_path, format="PNG")
    return save_path