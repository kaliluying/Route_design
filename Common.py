"""
Common.py - 统一兼容层
负责：初始化窗口 + 导出全局变量 + 修复已知问题

使用说明:
    - 导入此模块时会自动初始化窗口和所有全局变量
    - 修复了 Focus(frame_job) 错误，现为 Focus(win)
    - 修复了 water_barrier_iamge 拼写错误
"""

import os
import tkinter as tk
import platform
import logging
from functools import partial
from PIL import Image, ImageTk, ImageOps

# ===== 1. 初始化状态管理 =====
from src.state.app_state import AppState, get_app_state

_app_state = get_app_state()

# ===== 2. 初始化窗口 =====
from src.ui.main_window import get_main_window

_main_window = get_main_window()

# ===== 3. 导出核心对象 =====
win = _main_window.window
canvas = _main_window.canvas

# ===== 4. 导出所有 Frames =====
frame_job = _main_window.get_frame("frame_job")
frame_function = _main_window.get_frame("frame_function")
frame_aux = _main_window.get_frame("frame_aux")
frame_mea = _main_window.get_frame("frame_mea")
frame_create = _main_window.get_frame("frame_create")

# 临时按钮 Frame
frame_temp_1 = _main_window.get_frame("frame_temp_1")
frame_temp_2 = _main_window.get_frame("frame_temp_2")
frame_temp_3 = _main_window.get_frame("frame_temp_3")
frame_temp_4 = _main_window.get_frame("frame_temp_4")
frame_temp_5 = _main_window.get_frame("frame_temp_5")
frame_temp_6 = _main_window.get_frame("frame_temp_6")
frame_temp_7 = _main_window.get_frame("frame_temp_7")
frame_temp_8 = _main_window.get_frame("frame_temp_8")
frame_temp_9 = _main_window.get_frame("frame_temp_9")

# 功能 Frame
frame_command_left = _main_window.get_frame("frame_command_left")
frame_command_right = _main_window.get_frame("frame_command_right")
frame_command = _main_window.get_frame("frame_command")
frame_edit = _main_window.get_frame("frame_edit")
frame_aux_com = _main_window.get_frame("frame_aux_com")
frame_aux_com_lef = _main_window.get_frame("frame_aux_com_lef")
frame_aux_com_rig = _main_window.get_frame("frame_aux_com_rig")

# 辅助信息 Frame
frame_aux_info = _main_window.get_frame("frame_aux_info")
frame_aux_tit = _main_window.get_frame("frame_aux_tit")
frame_aux_inp = _main_window.get_frame("frame_aux_inp")
frame_aux_tit2 = _main_window.get_frame("frame_aux_tit2")
frame_aux_inp2 = _main_window.get_frame("frame_aux_inp2")
frame_aux_but = _main_window.get_frame("frame_aux_but")

# 测量功能 Frame
frame_mea_com = _main_window.get_frame("frame_mea_com")
frame_mea_com_lef = _main_window.get_frame("frame_mea_com_lef")
frame_mea_com_rig = _main_window.get_frame("frame_mea_com_rig")

# ===== 5. 导出图像路径（兼容旧代码） =====
force_image = "img/force.png"
compass_image = "img/compass.png"
water_barrier_image = "img/water_barrier.png"
brick_wall_image = "img/brick_wall.png"
line_image = "img/line.png"
gate_image = "img/gate.png"
circular_image = "img/circular.png"
icon_path = "img/ic.png"
force_obj = _main_window.get_image("force_image")
icon_obj = _main_window.get_image("icon_path")

# ===== 6. 导出状态变量 =====
sys_name = platform.system()
FONT = ("微软雅黑", 15 if sys_name == "Darwin" else 12)
WIDTH, HEIGHT = 900, 600

# ===== 7. 导出 AppState 实例（推荐使用）=====
# 推荐新代码使用: from Common import state
# 然后通过 state.index_img, state.px 等访问
state = _app_state

# 获取 AppState 的辅助函数
def get_app_state():
    """获取 AppState 实例"""
    return _app_state


# 工具变量（延迟获取，因为需要主窗口创建后才能初始化 tk 变量）
class _DelayedVar:
    """延迟获取 tk 变量的包装类"""

    def __init__(self, app_state, attr_name):
        self._app_state = app_state
        self._attr_name = attr_name

    def get(self):
        return getattr(self._app_state, self._attr_name)

    def set(self, value):
        getattr(self._app_state, self._attr_name).set(value)


what = _DelayedVar(_app_state, "what")
no_what = _DelayedVar(_app_state, "no_what")

# ===== 模块级变量通过 __getattr__/__setattr__ 代理到 AppState =====
# 这样当函数中使用 global index_txt 然后 index_txt = xxx 时，
# 会自动转发到 AppState

_known_attrs = {
    'choice_tup', 'stack', 'rotate_',
    'watermark', 'fg_img', 'fg_path',
    'info_var', 'pro_var', 'h1', 'h2',
    'route_click', 'route_clicks',
    'aux_stare', 'current_frame_stare',
    'remove_px', 'click_num', 'lastDraw', 'end',
    'grid_start', 'create_grid', 'state_f', 'temp_txt',
    'index_txt', 'index_img', 'par_index', 'px',
    'state', 'get_app_state'
}

def __getattr__(name):
    """模块级属性访问代理到 AppState"""
    if name in _known_attrs:
        return getattr(_app_state, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

def __setattr__(name, value):
    """模块级属性赋值代理到 AppState"""
    if name in _known_attrs:
        setattr(_app_state, name, value)
    else:
        object.__setattr__(__import__(__name__), name, value)

# ===== 7. 初始化 Focus ✅ 修复：传入 win 而非 frame_job =====
from focus import Focus

focus = Focus(win)

# ===== 8. 导出工具函数 =====
from src.core.tool_functions import (
    create_tool_functions,
    create_canvas_tools,
    create_aux_tools,
    create_obstacle_tools,
)
from src.core.obstacle_factory import (
    insert,
    parameter,
    hidden,
    create_monorail,
    create_oxer,
    create_tirail,
    create_combination_ab,
    create_combination_abc,
    create_live,
    create_force,
    create_compass,
    create_water_barrier,
    create_brick_wall,
    create_line,
    create_gate,
    create_circular,
)

# ===== 9. 迁移的 Middleware 函数 =====
_current_tag = None
_line_tag = None
_current_frame_stare = True
_live_state = 0
_bar_len = 4.0


def set_cur(cur):
    """设置障碍tag"""
    global _current_tag
    _current_tag = cur


def set_line(line):
    """设置辅助线tag"""
    global _line_tag
    _line_tag = line


def get_cur():
    """获取障碍tag和辅助线tag"""
    return _current_tag, _line_tag


def set_frame_stare(frame_stare):
    """设置多选框状态"""
    global _current_frame_stare
    _current_frame_stare = frame_stare


def get_frame_stare():
    """获取多选框状态"""
    return _current_frame_stare


def get_live():
    """获取利物浦是否为双横木"""
    return _live_state


def set_live(state):
    """设置利物浦是否为双横木"""
    global _live_state
    _live_state = state


def set_len(length):
    """设置全局障碍长度"""
    global _bar_len
    _bar_len = float(length.get())


def get_len():
    """获取全局障碍长度"""
    return _bar_len


# ===== 导出到模块级别（向后兼容） =====
import sys

_current_module = sys.modules[__name__]
_current_module.set_len = set_len
_current_module.get_len = get_len
_current_module.get_cur = get_cur
_current_module.set_cur = set_cur
_current_module.set_line = set_line
_current_module.get_frame_stare = get_frame_stare
_current_module.set_frame_stare = set_frame_stare
_current_module.get_live = get_live
_current_module.set_live = set_live


from src.core.obstacle_factory import (
    insert,
    parameter,
    hidden,
    create_monorail,
    create_oxer,
    create_tirail,
    create_combination_ab,
    create_combination_abc,
    create_live,
    create_force,
    create_compass,
    create_water_barrier,
    create_brick_wall,
    create_line,
    create_gate,
    create_circular,
)
