"""
应用常量定义
集中管理所有常量，避免魔法数字
"""

import platform
import os

# ===== 系统检测 =====
SYS_NAME = platform.system()
IS_MACOS = SYS_NAME == "Darwin"
IS_WINDOWS = SYS_NAME == "Windows"

# ===== 默认场地尺寸（米） =====
DEFAULT_ARENA_WIDTH = 60
DEFAULT_ARENA_HEIGHT = 90

# ===== 画布尺寸（像素，10:1比例） =====
CANVAS_WIDTH = 900
CANVAS_HEIGHT = 600
CANVAS_OFFSET_X = 30
CANVAS_OFFSET_Y = 80

# ===== 比例：1像素 = 0.1米 =====
SCALE_FACTOR = 10
COORD_OFFSET_X = 1.5
COORD_OFFSET_Y = 5.0

# ===== 默认字体配置 =====
if IS_MACOS:
    DEFAULT_FONT = ("微软雅黑", 15)
    FONT_SIZE_LARGE = 21
    FONT_SIZE_SMALL = 13
    WATERMARK_FONT_SCALE = 0.16
    BUTTON_WIDTH = 5
else:
    DEFAULT_FONT = ("微软雅黑", 12)
    FONT_SIZE_LARGE = 15
    FONT_SIZE_SMALL = 11
    WATERMARK_FONT_SCALE = 0.12
    BUTTON_WIDTH = 10

FONT_FAMILY_PRIMARY = "微软雅黑"
FONT_FAMILY_SPECIAL = "行楷"
FONT_FAMILY_SIMPLE = "宋体"

# ===== 默认障碍长度（米） =====
DEFAULT_BAR_LENGTH = 4.0

# ===== 障碍物默认值 =====
DEFAULT_WATER_WIDTH = 3
DEFAULT_WATER_HEIGHT = 4
DEFAULT_LIVE_WIDTH = 2
DEFAULT_LIVE_HEIGHT = 4
DEFAULT_COMBINATION_DISTANCE = 3
DEFAULT_OXER_DISTANCE = 30  # 厘米

# ===== 目录路径 =====
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMG_DIR = os.path.join(BASE_DIR, "img")
TEMP_DIR = os.path.join(BASE_DIR, "temp_img")
DOWNLOAD_DIR = os.path.join(BASE_DIR, "ms_download")

# ===== 图像路径 =====
IMAGE_PATHS = {
    "force": os.path.join(IMG_DIR, "force.png"),
    "compass": os.path.join(IMG_DIR, "compass.png"),
    "water_barrier": os.path.join(IMG_DIR, "water_barrier.png"),
    "brick_wall": os.path.join(IMG_DIR, "brick_wall.png"),
    "line": os.path.join(IMG_DIR, "line.png"),
    "gate": os.path.join(IMG_DIR, "gate.png"),
    "circular": os.path.join(IMG_DIR, "circular.png"),
    "icon": os.path.join(IMG_DIR, "ic.png"),
    "one": os.path.join(IMG_DIR, "one.png"),
    "liverpool": os.path.join(IMG_DIR, "liverpool3.png"),
    "direction": os.path.join(IMG_DIR, "direction2.png"),
}

# ===== Ghostscript 配置 =====
GS_DIR = "gs10.01.1-32bit"
GS_BINARY = os.path.join(GS_DIR, "bin", "gswin32.exe")
GS_DEVICE = "jpeg"
GS_RESOLUTION = 600

# ===== 颜色配置 =====
COLOR_WATERMARK = "#e4e4dc"
COLOR_LINE = "#000000"
COLOR_SELECTION_DASH = (3, 5)

# ===== 赛事信息字段 =====
EVENT_INFO_FIELDS = [
    "比赛名称",
    "级别赛制",
    "比赛日期",
    "路线查看时间",
    "开赛时间",
    "判罚表",
    "障碍高度",
    "行进速度",
    "路线长度",
    "允许时间",
    "限制时间",
    "障碍数量",
    "跳跃数量",
    "附加赛",
    "路线设计师",
]

# ===== 确保目录存在 =====
for _dir in [TEMP_DIR, DOWNLOAD_DIR]:
    if not os.path.exists(_dir):
        os.mkdir(_dir)
