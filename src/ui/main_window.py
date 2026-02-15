"""
主窗口模块
封装主窗口的创建、布局和属性
"""

import tkinter as tk
from typing import Optional, Dict, Any
from PIL import ImageTk


class MainWindow:
    """主窗口类"""

    _instance: Optional["MainWindow"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._win: Optional[tk.Tk] = None
        self._canvas: Optional[tk.Canvas] = None
        self._frames: Dict[str, tk.Frame] = {}
        self._images: Dict[str, Any] = {}

    def initialize(self, title: str = "路线设计") -> "MainWindow":
        """初始化窗口"""
        self._create_window(title)
        self._create_canvas()
        self._create_frames()
        self._load_images()
        return self

    def _create_window(self, title: str):
        """创建主窗口"""
        self._win = tk.Tk()
        self._win.title(title)

        # 最大化
        W = self._win.winfo_screenwidth()
        H = self._win.winfo_screenheight()
        self._win.geometry(f"{W}x{H}")
        self._win.state("zoomed")

        # 设置图标
        try:
            self._win.iconphoto(False, tk.PhotoImage(file="img/ic.png"))
        except Exception:
            pass

    def _create_canvas(self):
        """创建画布"""
        self._canvas = tk.Canvas(
            self._win, width=900 + 30, height=600 + 80, highlightthickness=0
        )
        self._canvas.place(x=175, y=100)

        # 初始化画布元素
        self._init_canvas_elements()

    def _init_canvas_elements(self):
        """初始化画布元素（场地矩形、辅助信息等）"""
        canvas = self._canvas
        WIDTH = 900
        HEIGHT = 600

        # 实际场地矩形
        canvas.create_rectangle(
            15, 50, WIDTH + 15, HEIGHT + 50, state="disabled", tags=("不框选", "实际画布")
        )

        # 右上角显示路线长宽
        w = WIDTH / 10
        h = HEIGHT / 10
        canvas.create_text(
            WIDTH - 40, 60, text=f"长：{w}m", tags=("辅助信息", "不框选", "长")
        )
        canvas.create_text(
            WIDTH - 40, 80, text=f"宽：{h}m", tags=("辅助信息", "不框选", "宽")
        )

        # 左上角显示 5m 的距离标记
        canvas.create_text(45, 60, text="5m", tags=("辅助信息", "不框选"))
        canvas.create_line(20, 65, 20, 70, tags=("辅助信息", "不框选"))
        canvas.create_line(70, 65, 70, 70, tags=("辅助信息", "不框选"))
        canvas.create_line(20, 70, 70, 70, tags=("辅助信息", "不框选"))

        # 右上显示路线长度（实时）
        canvas.create_text(
            WIDTH - 40, 30, text="0.00m", tags=("实时路线", "不框选", "辅助信息")
        )

        # 右下角显示鼠标实时坐标
        canvas.create_text(
            WIDTH - 10, HEIGHT + 60, text="x:0.00", tags=("辅助信息", "不框选", "鼠标x")
        )
        canvas.create_text(
            WIDTH - 10, HEIGHT + 70, text="y:0.00", tags=("辅助信息", "不框选", "鼠标y")
        )

        # 比赛名称
        canvas.create_text(
            WIDTH / 2, 30, text="", tags=("比赛名称", "辅助信息", "不框选")
        )

    def _create_frames(self):
        """创建所有 UI 容器"""
        win = self._win
        canvas = self._canvas

        # ===== 左侧功能栏 =====
        self._frames["frame_function"] = tk.Frame(win, name="左侧功能栏")
        self._frames["frame_function"].place(x=5, y=150)

        # 工作模块容器
        self._frames["frame_job"] = tk.Frame(
            self._frames["frame_function"], relief="ridge", bd=2, name="工作模块"
        )

        # ===== 底部辅助/测量模块 =====
        self._frames["frame_aux_mea"] = tk.Frame(
            win, relief="ridge", bd=2, name="辅助模块"
        )
        self._frames["frame_aux_mea"].place(x=5, y=530)
        self._frames["frame_aux"] = tk.Frame(
            self._frames["frame_aux_mea"], name="辅助模块"
        )
        self._frames["frame_mea"] = tk.Frame(
            self._frames["frame_aux_mea"], name="测量模块"
        )

        # 打包
        self._frames["frame_job"].pack()
        self._frames["frame_aux"].pack()
        self._frames["frame_mea"].pack()

        # ===== 功能容器（操作模块）=====
        self._frames["frame_command"] = tk.Frame(
            self._frames["frame_job"], name="功能容器"
        )
        self._frames["frame_command"].pack()
        self._frames["frame_command_left"] = tk.Frame(self._frames["frame_command"])
        self._frames["frame_command_right"] = tk.Frame(self._frames["frame_command"])
        tk.Label(self._frames["frame_command"], text="操作模块").pack()
        self._frames["frame_command_left"].pack(side="left")
        self._frames["frame_command_right"].pack(side="right")

        # ===== 旋转、备注编辑容器 =====
        self._frames["frame_edit"] = tk.Frame(
            self._frames["frame_job"], name="旋转、备注"
        )
        self._frames["frame_edit"].pack()

        # 旋转容器
        self._frames["frame_x"] = tk.Frame(self._frames["frame_edit"], name="旋转")
        self._frames["frame_x"].pack()
        self._frames["frame_focus_x_ladel"] = tk.Frame(self._frames["frame_x"])
        self._frames["frame_focus_x_ent"] = tk.Frame(self._frames["frame_x"])
        self._frames["frame_focus_x_but"] = tk.Frame(self._frames["frame_x"])
        self._frames["frame_focus_x_but"].pack(side="bottom")
        self._frames["frame_focus_x_ladel"].pack(side="left")
        self._frames["frame_focus_x_ent"].pack(side="right")

        # 备注容器
        self._frames["frame_z"] = tk.Frame(self._frames["frame_edit"], name="备注")
        self._frames["frame_z"].pack()
        self._frames["frame_focus_z_ladel"] = tk.Frame(self._frames["frame_z"])
        self._frames["frame_focus_z_ent"] = tk.Frame(self._frames["frame_z"])
        self._frames["frame_focus_z_but"] = tk.Frame(self._frames["frame_z"])
        self._frames["frame_focus_z_but"].pack(side="bottom")
        self._frames["frame_focus_z_ladel"].pack(side="left")
        self._frames["frame_focus_z_ent"].pack(side="right")

        # ===== 辅助功能容器 =====
        self._frames["frame_aux_com"] = tk.Frame(
            self._frames["frame_aux"], name="辅助功能容器"
        )
        self._frames["frame_aux_com"].pack()
        tk.Label(self._frames["frame_aux_com"], text="辅助模块").pack()
        self._frames["frame_aux_com_lef"] = tk.Frame(self._frames["frame_aux_com"])
        self._frames["frame_aux_com_rig"] = tk.Frame(self._frames["frame_aux_com"])
        self._frames["frame_aux_com_lef"].pack(side="left")
        self._frames["frame_aux_com_rig"].pack(side="right")

        # ===== 辅助信息容器 =====
        self._frames["frame_aux_info"] = tk.Frame(
            self._frames["frame_aux"], name="辅助信息容器"
        )
        self._frames["frame_aux_info"].pack()

        self._frames["frame_aux_info_1"] = tk.Frame(self._frames["frame_aux_info"])
        self._frames["frame_aux_info_2"] = tk.Frame(self._frames["frame_aux_info"])
        self._frames["frame_aux_tit"] = tk.Frame(self._frames["frame_aux_info_1"])
        self._frames["frame_aux_inp"] = tk.Frame(self._frames["frame_aux_info_1"])
        self._frames["frame_aux_tit2"] = tk.Frame(self._frames["frame_aux_info"])
        self._frames["frame_aux_inp2"] = tk.Frame(self._frames["frame_aux_info"])
        self._frames["frame_aux_but"] = tk.Frame(self._frames["frame_aux_info"])

        self._frames["frame_aux_info_1"].pack()
        self._frames["frame_aux_info_2"].pack()
        self._frames["frame_aux_tit"].pack(side="left")
        self._frames["frame_aux_inp"].pack(side="right")
        self._frames["frame_aux_tit2"].pack(side="left")
        self._frames["frame_aux_inp2"].pack(side="left")
        self._frames["frame_aux_but"].pack(side="bottom")

        # ===== 测量功能容器 =====
        self._frames["frame_mea_com"] = tk.Frame(
            self._frames["frame_mea"], name="测量功能容器"
        )
        self._frames["frame_mea_com"].pack()
        self._frames["frame_mea_com_lef"] = tk.Frame(self._frames["frame_mea_com"])
        self._frames["frame_mea_com_rig"] = tk.Frame(self._frames["frame_mea_com"])
        self._frames["frame_mea_com_lef"].pack(side="left")
        self._frames["frame_mea_com_rig"].pack(side="right")

        # ===== 障碍按键容器（生产模块）=====
        self._frames["frame_create"] = tk.Frame(win, name="按键", relief="ridge", bd=2)
        self._frames["frame_create"].place(x=400, y=5)
        tk.Label(self._frames["frame_create"], text="生产模块").pack()

        # 创建9个障碍物按钮Frame
        for i in range(1, 10):
            self._frames[f"frame_temp_{i}"] = tk.Frame(self._frames["frame_create"])

        self._frames["frame_temp_1"].pack(side="left")
        self._frames["frame_temp_2"].pack(side="left")
        self._frames["frame_temp_3"].pack(side="left")
        self._frames["frame_temp_4"].pack(side="left")
        self._frames["frame_temp_5"].pack(side="left")
        self._frames["frame_temp_6"].pack(side="left")
        self._frames["frame_temp_7"].pack(side="left")
        self._frames["frame_temp_8"].pack(side="bottom")
        self._frames["frame_temp_9"].pack(side="top")

        # ===== 比赛信息面板 =====
        self._frames["frame_info"] = tk.Frame(win, name="比赛信息")
        self._frames["frame_tit"] = tk.Frame(self._frames["frame_info"])
        self._frames["frame_inp"] = tk.Frame(self._frames["frame_info"])
        self._frames["frame_por"] = tk.Frame(self._frames["frame_info"])

        # 赛事信息标签列表
        self._info_labels = [
            "比赛名称",
            "比赛日期",
            "比赛地点",
            "参赛级别",
            "路线裁判",
            "参赛骑手",
            "允许时间",
            "最佳时间",
            "障碍数量",
            "跳跃数量",
            "附加赛",
            "路线设计师",
        ]

        self._frames["frame_info"].place(x=1200, y=150)
        self._frames["frame_tit"].pack(side="left")
        self._frames["frame_por"].pack(side="right")
        self._frames["frame_inp"].pack(side="right")

    def _load_images(self):
        """加载图像对象"""
        image_paths = {
            "force_image": "img/force.png",
            "icon_path": "img/ic.png",
        }
        for name, path in image_paths.items():
            try:
                self._images[name] = ImageTk.PhotoImage(Image.open(path))
            except Exception:
                self._images[name] = None

    # ===== 属性访问器 =====

    @property
    def window(self) -> tk.Tk:
        return self._win

    @property
    def canvas(self) -> tk.Canvas:
        return self._canvas

    @property
    def win(self) -> tk.Tk:
        return self._win

    def get_frame(self, name: str) -> Optional[tk.Frame]:
        """获取指定名称的 Frame"""
        return self._frames.get(name)

    def get_image(self, name: str) -> Optional[Any]:
        """获取指定名称的图像"""
        return self._images.get(name)

    # ===== 便捷方法 =====

    def run(self):
        """运行主循环"""
        if self._win:
            self._win.mainloop()

    def destroy(self):
        """销毁窗口"""
        if self._win:
            self._win.destroy()
            self._win = None
            MainWindow._instance = None

    def export_globals_to_module(self, module_name: str):
        """导出全局变量到指定名称的模块（用于向后兼容）"""
        import sys

        target_module = sys.modules[module_name]

        # 导出窗口和画布
        setattr(target_module, "win", self._win)
        setattr(target_module, "canvas", self._canvas)

        # 导出常用 frames
        setattr(target_module, "frame_job", self._frames.get("frame_job"))
        setattr(target_module, "frame_function", self._frames.get("frame_function"))
        setattr(target_module, "frame_aux", self._frames.get("frame_aux"))
        setattr(target_module, "frame_mea", self._frames.get("frame_mea"))
        setattr(target_module, "frame_create", self._frames.get("frame_create"))
        setattr(
            target_module, "frame_command_left", self._frames.get("frame_command_left")
        )
        setattr(
            target_module,
            "frame_command_right",
            self._frames.get("frame_command_right"),
        )
        setattr(target_module, "frame_command", self._frames.get("frame_command"))

        # 导出临时 frames
        for i in range(1, 10):
            setattr(
                target_module, f"frame_temp_{i}", self._frames.get(f"frame_temp_{i}")
            )

        # 导出辅助 frames
        setattr(target_module, "frame_aux_com", self._frames.get("frame_aux_com"))
        setattr(
            target_module, "frame_aux_com_lef", self._frames.get("frame_aux_com_lef")
        )
        setattr(
            target_module, "frame_aux_com_rig", self._frames.get("frame_aux_com_rig")
        )
        setattr(target_module, "frame_aux_info", self._frames.get("frame_aux_info"))
        setattr(target_module, "frame_aux_tit", self._frames.get("frame_aux_tit"))
        setattr(target_module, "frame_aux_inp", self._frames.get("frame_aux_inp"))
        setattr(target_module, "frame_aux_tit2", self._frames.get("frame_aux_tit2"))
        setattr(target_module, "frame_aux_inp2", self._frames.get("frame_aux_inp2"))
        setattr(target_module, "frame_aux_but", self._frames.get("frame_aux_but"))
        setattr(target_module, "frame_mea_com", self._frames.get("frame_mea_com"))
        setattr(
            target_module, "frame_mea_com_lef", self._frames.get("frame_mea_com_lef")
        )
        setattr(
            target_module, "frame_mea_com_rig", self._frames.get("frame_mea_com_rig")
        )

        # 导出比赛信息 frames
        setattr(target_module, "frame_info", self._frames.get("frame_info"))
        setattr(target_module, "frame_tit", self._frames.get("frame_tit"))
        setattr(target_module, "frame_inp", self._frames.get("frame_inp"))
        setattr(target_module, "frame_por", self._frames.get("frame_por"))

        # 导出赛事信息标签列表
        setattr(target_module, "info", self._info_labels)

        # 导出图像路径（兼容旧代码）
        setattr(target_module, "force_image", "img/force.png")
        setattr(target_module, "compass_image", "img/compass.png")
        setattr(target_module, "water_barrier_image", "img/water_barrier.png")
        setattr(target_module, "brick_wall_image", "img/brick_wall.png")
        setattr(target_module, "line_image", "img/line.png")
        setattr(target_module, "gate_image", "img/gate.png")
        setattr(target_module, "circular_image", "img/circular.png")
        setattr(target_module, "icon_path", "img/ic.png")

        # 导出图像对象
        setattr(target_module, "force_obj", self._images.get("force_image"))
        setattr(target_module, "icon_obj", self._images.get("icon_path"))


# 便捷函数
def get_main_window(title: str = "路线设计") -> MainWindow:
    """获取主窗口单例，自动初始化"""
    if MainWindow._instance is None:
        MainWindow._instance = MainWindow()
        MainWindow._instance.initialize(title)
    return MainWindow._instance


def create_main_window(title: str = "路线设计") -> MainWindow:
    """创建并初始化主窗口（与 get_main_window 等价）"""
    return get_main_window(title)
