"""
应用状态管理单例类
提供统一的全局状态管理，替代分散的全局变量

注意：tk.IntVar 需要在主窗口创建后才能初始化
"""

import tkinter as tk
from typing import Optional, Dict, List, Any, Tuple


class AppState:
    """应用全局状态单例"""

    _instance = None
    _root_window: Optional[tk.Tk] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
            cls._instance._tk_vars_initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._init_state()

    @classmethod
    def set_root_window(cls, root: tk.Tk):
        """设置根窗口（必须在主窗口创建后调用）"""
        cls._root_window = root
        if cls._instance and not cls._instance._tk_vars_initialized:
            cls._instance._init_tk_variables()

    def _init_state(self):
        """初始化非 tk 变量状态"""
        # ===== 窗口/系统状态 =====
        self.sys_name = "Windows"  # 默认 Windows
        self.FONT = ("微软雅黑", 12)

        # ===== 画布相关状态 =====
        self.WIDTH = 900
        self.HEIGHT = 600
        self.canvas_width = self.WIDTH + 30
        self.canvas_height = self.HEIGHT + 80

        # ===== 障碍物相关 =====
        self.bar_len = 4.0  # 障碍物全局长度（米）
        self.index = 0
        self.index_txt = 0
        self.index_img = 0
        self.par_index = 1  # 障碍参数显示状态

        # ===== 鼠标/坐标状态 =====
        self.mouse_x = 0
        self.mouse_y = 0

        # ===== 工具状态 =====
        self.font_size = 1
        self.remove_size = 1
        self.size = 1

        # ===== 测量状态 =====
        self.px = 0.0  # 总路线长度（米）
        self.click_num = 1  # 点击次数
        self.remove_px = {}  # 线段长度记录 {id: 长度}
        self.route_clicks = []  # 路线测量点击位置
        self.route_click = []  # 兼容旧代码
        self.click_history = []  # 点击历史
        self.lastDraw = 0  # 最后绘制的线段ID
        self.end = [0]  # 线段ID列表

        # ===== 网格状态 =====
        self.grid_start = 0
        self.create_grid = False

        # ===== 辅助信息状态 =====
        self.aux_state = True
        self.aux_stare = True  # 兼容旧代码
        self.state_f = 1  # 水印状态

        # ===== 水印/前景图像 =====
        self.watermark = None  # 水印 canvas 对象
        self.fg_img = None  # 前景图像
        self.fg_path = ""  # 前景图像路径

        # ===== 比赛信息 =====
        self.info_var = []  # 比赛信息变量列表
        self.pro_var = []  # 比赛信息值列表
        self.temp_txt = None

        # ===== 画布文本对象 =====
        self.h1 = None  # 画布长文本对象
        self.h2 = None  # 画布宽文本对象

        # ===== 选择状态 =====
        self.current_frame_stare = True  # 多选框状态（兼容旧代码）

        # ===== 选择状态 =====
        self.choice_tuple = []  # 多选框坐标
        self.choice_tup = []  # 兼容旧代码
        self.choice_start = False

        # ===== 撤销栈 =====
        self.stack = []

        # ===== 旋转历史 =====
        self.rotate_ = [0]

        # ===== 比赛信息 =====
        self.temp_txt = None

        # ===== 图像路径 =====
        self.force_image = "img/force.png"
        self.compass_image = "img/compass.png"
        self.water_barrier_image = "img/water_barrier.png"
        self.brick_wall_image = "img/brick_wall.png"
        self.line_image = "img/line.png"
        self.gate_image = "img/gate.png"
        self.icon_path = "img/ic.png"
        self.circular_image = "img/circular.png"

        # ===== tk 变量（延迟初始化）=====
        self._tk_vars: Dict[str, tk.Variable] = {}

    def _init_tk_variables(self):
        """初始化 tk 变量（需要主窗口）"""
        if self._tk_vars_initialized:
            return
        if AppState._root_window is None:
            return

        self._tk_vars = {
            "X": tk.IntVar(AppState._root_window, value=0, name="state_X"),
            "Y": tk.IntVar(AppState._root_window, value=0, name="state_Y"),
            "move_x": tk.IntVar(AppState._root_window, value=0, name="state_move_x"),
            "move_y": tk.IntVar(AppState._root_window, value=0, name="state_move_y"),
            "start_x": tk.IntVar(AppState._root_window, value=0, name="state_start_x"),
            "start_y": tk.IntVar(AppState._root_window, value=0, name="state_start_y"),
            "end_x": tk.IntVar(AppState._root_window, value=0, name="state_end_x"),
            "end_y": tk.IntVar(AppState._root_window, value=0, name="state_end_y"),
            "what": tk.IntVar(AppState._root_window, value=0, name="state_what"),
            "no_what": tk.IntVar(AppState._root_window, value=0, name="state_no_what"),
        }
        self._tk_vars_initialized = True

    # ===== 属性访问器 =====

    @property
    def X(self) -> tk.IntVar:
        if "X" not in self._tk_vars:
            self._init_tk_variables()
        return self._tk_vars["X"]

    @property
    def Y(self) -> tk.IntVar:
        if "Y" not in self._tk_vars:
            self._init_tk_variables()
        return self._tk_vars["Y"]

    @property
    def move_x(self) -> tk.IntVar:
        if "move_x" not in self._tk_vars:
            self._init_tk_variables()
        return self._tk_vars["move_x"]

    @property
    def move_y(self) -> tk.IntVar:
        if "move_y" not in self._tk_vars:
            self._init_tk_variables()
        return self._tk_vars["move_y"]

    @property
    def start_x(self) -> tk.IntVar:
        if "start_x" not in self._tk_vars:
            self._init_tk_variables()
        return self._tk_vars["start_x"]

    @property
    def start_y(self) -> tk.IntVar:
        if "start_y" not in self._tk_vars:
            self._init_tk_variables()
        return self._tk_vars["start_y"]

    @property
    def end_x(self) -> tk.IntVar:
        if "end_x" not in self._tk_vars:
            self._init_tk_variables()
        return self._tk_vars["end_x"]

    @property
    def end_y(self) -> tk.IntVar:
        if "end_y" not in self._tk_vars:
            self._init_tk_variables()
        return self._tk_vars["end_y"]

    @property
    def what(self) -> tk.IntVar:
        if "what" not in self._tk_vars:
            self._init_tk_variables()
        return self._tk_vars["what"]

    @property
    def no_what(self) -> tk.IntVar:
        if "no_what" not in self._tk_vars:
            self._init_tk_variables()
        return self._tk_vars["no_what"]

    # ===== 便捷属性 =====

    @property
    def scale_factor(self) -> float:
        """比例因子：像素/米"""
        return 10.0

    def meters_to_pixels(self, meters: float) -> int:
        return int(meters * self.scale_factor)

    def pixels_to_meters(self, pixels: int) -> float:
        return pixels / self.scale_factor

    # ===== 状态重置方法 =====

    def reset_click_state(self):
        """重置点击状态（测量用）"""
        self.click_num = 1
        self.route_clicks = []

    def reset_selection(self):
        """重置选择状态"""
        self.current_tag = None
        self.choice_start = False
        self.choice_tuple = []

    def clear_measurement(self):
        """清除测量数据"""
        self.px = 0.0
        self.click_num = 1
        self.remove_px = {}
        self.route_clicks = []

    def set_tool(self, tool_id: int):
        """设置当前工具"""
        self.no_what.set(self.what.get())
        self.what.set(tool_id)

    def increment_index_img(self) -> int:
        """递增并返回 index_img"""
        self.index_img += 1
        return self.index_img

    def increment_index_txt(self) -> int:
        """递增并返回 index_txt"""
        self.index_txt += 1
        return self.index_txt

    def update_canvas_size(self, width: int, height: int):
        """更新画布尺寸"""
        self.WIDTH = width
        self.HEIGHT = height
        self.canvas_width = width + 30
        self.canvas_height = height + 80

    def set_system(self, sys_name: str):
        """设置系统名称并更新字体"""
        self.sys_name = sys_name
        if sys_name == "Darwin":
            self.FONT = ("微软雅黑", 15)
        elif sys_name == "Windows":
            self.FONT = ("微软雅黑", 12)

    # ===== 撤销操作 =====

    def push_undo(self, action: Tuple):
        """添加撤销操作"""
        self.stack.append(action)

    def pop_undo(self):
        """弹出撤销操作"""
        if self.stack:
            return self.stack.pop()
        return None

    def get_undo_stack(self) -> List:
        """获取撤销栈"""
        return self.stack


def get_app_state() -> AppState:
    """获取 AppState 单例"""
    return AppState()
