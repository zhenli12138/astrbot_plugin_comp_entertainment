from astrbot.api.event import filter
from astrbot.api.all import *
from typing import (Dict, Any, Optional, AnyStr, Callable, Union, Awaitable,Coroutine)
import os
import json
from astrbot.api.provider import ProviderRequest
from astrbot.core.platform.sources.aiocqhttp.aiocqhttp_message_event import AiocqhttpMessageEvent
from data.plugins.astrbot_plugin_comp_entertainment.api_collection import daliya, ddz, deer, ai_make, lol, horse
from data.plugins.astrbot_plugin_comp_entertainment.api_collection import pilcreate
from data.plugins.astrbot_plugin_comp_entertainment.api_collection import api,emoji,image,text, search
from data.plugins.astrbot_plugin_comp_entertainment.api_collection import video, music,chess, blue_archive
from pathlib import Path
from typing import Dict, List
from astrbot.api.all import *

@register("astrbot_plugin_comp_entertainment", "达莉娅",
          "达莉娅群娱插件，60+超多功能集成调用插件，持续更新中，发【菜单】看菜单",
          "v2.2.0")
