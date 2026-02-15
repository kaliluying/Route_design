"""
应用程序常量配置
"""

import platform
from pathlib import Path

# 系统信息
SYSTEM_NAME = platform.system()
IS_WINDOWS = SYSTEM_NAME == 'Windows'
IS_MACOS = SYSTEM_NAME == 'Darwin'

# 应用程序信息
APP_NAME = "路线设计"
APP_VERSION = "2.0.0"
APP_AUTHOR = "山东体育学院"
VERSION_URL = "https://github.com/kaliluying/Route_design/raw/dev/version.txt"

# 路径配置
BASE_DIR = Path(__file__).parent.parent.parent
IMG_DIR = BASE_DIR / "img"
BACKUP_DIR = BASE_DIR / "backup"
AUTO_BACKUP_DIR = BASE_DIR / "auto_backup"
DOWNLOAD_DIR = BASE_DIR / "ms_download"

# UI配置
UI_CONFIG = {
    'font': ("微软雅黑", 15) if IS_MACOS else ("微软雅黑", 12),
    'confirm_style': 'success-outline',
    'button_style': 'outline',
    'default_width': 900,
    'default_height': 600,
    'canvas_padding': 50,
    'canvas_height_padding': 180,
    'canvas_x': 250,
    'canvas_y': 100,
}

# 障碍物配置
OBSTACLE_CONFIG = {
    'default_length': 4.0,
    'default_width': 90,
    'default_height': 60,
    'small_rect_size': 10,
    'rect_left_offset': 130,
    'rect_right_offset': 50,
    'font_size': 1,
    'remove_size': 1,
}

# 图片资源路径
IMAGE_PATHS = {
    'force': "img/force.png",
    'compass': "img/compass.png",
    'water_barrier': "img/water_barrier.png",
    'brick_wall': "img/brick_wall.png",
    'line': "img/start_end.png",
    'gate': "img/gate.png",
    'tree': "img/tree.png",
    'joker': "img/joker.png",
    'circular': "img/circular.png",
    'direction': "img/direction2.png",
    'one': "img/one.png",
    'liverpool': "img/liverpool3.png",
    'icon': "img/ic.png",
}

# 障碍物类型
OBSTACLE_TYPES = {
    'monorail': '单横木',
    'oxer': '双横木',
    'tirail': '三横木',
    'four': '四横木',
    'combination_ab': 'AB组合障碍',
    'combination_abc': 'ABC组合障碍',
    'live': '利物浦',
    'water': '水障',
    'brick_wall': '砖墙',
    'gate': '进出口',
    'compass': '指北针',
    'line': '起/终点线',
    'force': '强制通过点',
    'tree': '树',
    'joker': '小丑',
    'circular': '圆',
    'diy': '自定义障碍',
}

# 赛事信息字段
EVENT_INFO_FIELDS = [
    '比赛名称', '级别赛制', '比赛日期', '路线查看时间', '开赛时间', 
    '判罚表', '障碍高度', '行进速度', '路线长度', '允许时间', 
    '限制时间', '障碍数量', '跳跃数量', '附加赛', '路线设计师'
]

# 操作模式
OPERATION_MODES = {
    'DRAG': 0,
    'DRAW': 1,
    'ERASE': 2,
    'ROTATE': 3,
}

# 文件类型
FILE_TYPES = {
    'json': [("JSON files", "*.json")],
    'image': [("JPEG", ".jpg"), ("PNG", ".png")],
    'all_images': [("image", "*.jpg"), ("image", "*.png")],
}
