from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.api.all import *
from PIL import Image, ImageDraw, ImageFont, ImageOps
class Poker:
    suits = ['♠', '♥', '♦', '♣']
    values = ['3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A', '2']
    specials = ['BJ', 'RJ']
    colors = {'♠': (0, 0, 0), '♥': (255, 0, 0),
              '♦': (255, 0, 0), '♣': (0, 0, 0)}
from PIL import Image, ImageDraw, ImageFont

def generate_menu():
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

def generate_hand_image(cards,idx):
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