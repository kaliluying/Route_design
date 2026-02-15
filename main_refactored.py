"""
重构后的应用入口点
展示模块化架构
"""

import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.dirname(__file__))

import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog, Entry
import math
import time
import subprocess
import platform
from functools import partial
from src.core.logger import get_logger, log_exception, error, warning
# 移除旧的 logging 导入，使用统一的 logger
# import logging  # 已注释，使用 src.core.logger

from PIL import Image, ImageTk, EpsImagePlugin

from src.ui.main_window import get_main_window
from src.state.app_state import get_app_state
from src.models.edit_panel import get_edit_panel
from src.core.image_processor import get_image_processor, _get_img_path
from src.ui.menu_handler import create_menu
from src.ui.save_handler import create_save_functions
from src.ui.measurement_handler import create_measurement_handler
from src.ui.obstacle_handler import create_obstacle_handler
from src.core.tool_functions import create_obstacle_tools
from src.constants import (
    DEFAULT_BAR_LENGTH,
    IS_WINDOWS,
    IMAGE_PATHS,
)


# 配置日志（使用统一日志模块）
logger = get_logger()
logger.info("应用程序启动")

# ===== 全局变量 =====
WIDTH = 900
HEIGHT = 600
choice_tup = []
par_index = 0
state_f = False  # 水印状态
create_grid = False
grid_start = False
aux_stare = True
remove_px = {}
lastDraw = None
end = []
index_txt = 0
index_img = 0
px = 0  # 测量长度
click_num = 1  # 点击次数
temp_txt = ""  # 比赛名称
fg_path = "img/fg.png"  # 背景图路径
fg_img = None  # 背景图对象
watermark = None  # 水印对象
h1 = None  # 长文本
h2 = None  # 宽文本
watermark_id = None  # 水印ID


# ===== 核心功能函数 =====

def found(win, canvas, var_l_w, var_l_h):
    """生成路线图"""
    global WIDTH, HEIGHT, fg_img, watermark_id, h1, h2, px

    w = var_l_w.get()
    h = var_l_h.get()

    try:
        WIDTH = int(float(w) * 10)
        HEIGHT = int(float(h) * 10)
    except ValueError:
        messagebox.showerror("错误", "请输入有效的数字")
        return

    # 调整画布尺寸
    canvas.config(width=WIDTH + 30, height=HEIGHT + 70)
    canvas.coords("实际画布", 15, 50, WIDTH + 15, HEIGHT + 50)

    # 更新长/宽显示
    wid = WIDTH / 10
    hei = HEIGHT / 10
    canvas.itemconfig("长", text=f"长：{wid}m")
    canvas.itemconfig("宽", text=f"宽：{hei}m")
    canvas.coords("长", WIDTH - 40, 60)
    canvas.coords("宽", WIDTH - 40, 80)
    canvas.coords("实时路线", WIDTH - 40, 30)

    # 更新鼠标坐标位置
    canvas.coords("鼠标x", WIDTH - 10, HEIGHT + 60)
    canvas.coords("鼠标y", WIDTH - 10, HEIGHT + 70)

    # 删除旧背景
    canvas.delete("bg")

    # 加载新背景
    try:
        img = Image.open(fg_path)
        img = img.resize((WIDTH, HEIGHT))
        fg_img = ImageTk.PhotoImage(img)
        canvas.create_image(15, 50, image=fg_img, anchor="nw", tags=("不框选", "bg"))
    except FileNotFoundError:
        pass  # 没有背景图时不报错

    # 水印
    global watermark, state_f
    canvas.delete("watermark")
    if state_f:
        font_size = int(WIDTH * 0.12) if WIDTH > 0 else 100
        watermark = canvas.create_text(
            WIDTH / 2,
            (HEIGHT + 20) / 2,
            text="山东体育学院",
            font=("行楷", font_size, "bold", "italic"),
            fill="#e4e4dc",
            tags=("watermark", "不框选"),
        )
        canvas.lower("watermark")

    # 重置测量
    px = 0
    canvas.itemconfig("实时路线", text="%.2fm" % px)


def _create_ui_buttons(
    win, canvas, app_state, main_window, tool_funcs, obstacle_funcs, width, sys_name
):
    """创建所有UI按钮"""
    # 获取frames
    frame_command_left = main_window.get_frame("frame_command_left")
    frame_command_right = main_window.get_frame("frame_command_right")
    frame_mea_com_rig = main_window.get_frame("frame_mea_com_rig")
    frame_mea_com_lef = main_window.get_frame("frame_mea_com_lef")
    frame_aux_com_lef = main_window.get_frame("frame_aux_com_lef")
    frame_aux_com_rig = main_window.get_frame("frame_aux_com_rig")
    frame_aux_tit = main_window.get_frame("frame_aux_tit")
    frame_aux_inp = main_window.get_frame("frame_aux_inp")
    frame_aux_tit2 = main_window.get_frame("frame_aux_tit2")
    frame_aux_inp2 = main_window.get_frame("frame_aux_inp2")
    frame_aux_but = main_window.get_frame("frame_aux_but")
    frame_temp_8 = main_window.get_frame("frame_temp_8")
    frame_temp_9 = main_window.get_frame("frame_temp_9")

    # 按钮宽度
    btn_width = 10 if sys_name == "Windows" else 5
    font = ("微软雅黑", 15 if sys_name == "Darwin" else 12)

    # ===== 工作模块按钮 =====
    but_0 = tk.Button(
        frame_command_left,
        text="拖动",
        command=tool_funcs["drag"],
        fg="red",
        width=btn_width,
        height=1,
    )
    but_0.pack()
    but_3 = tk.Button(
        frame_command_left,
        text="旋转",
        command=tool_funcs["rotate"],
        width=btn_width,
        height=1,
    )
    but_3.pack()

    # ===== 测量模块按钮 =====
    tk.Button(
        frame_mea_com_rig,
        text="清屏",
        command=tool_funcs["clear"],
        width=btn_width,
        height=1,
    ).pack()

    # ===== 功能按钮 =====
    tk.Button(
        frame_command_right,
        text="置底",
        command=lambda: None,
        width=btn_width,
        height=1,
    ).pack()
    tk.Button(
        frame_command_right,
        text="删除",
        command=lambda: None,
        width=btn_width,
        height=1,
    ).pack()

    # ===== 辅助模块按钮 =====
    tk.Button(
        frame_aux_com_lef,
        text="网格辅助线",
        command=lambda: None,
        width=btn_width,
        height=1,
    ).pack()
    aux_info = tk.Button(
        frame_aux_com_rig,
        text="隐藏辅助信息",
        command=lambda: None,
        width=btn_width,
        height=1,
    )
    aux_info.pack()

    # ===== 障碍参数 =====
    tk.Label(frame_aux_tit, text="障碍备注：", font=font).pack(pady=5)
    var_parameter = tk.StringVar()
    e_parameter = Entry(frame_aux_inp, textvariable=var_parameter, width=8)
    e_parameter.pack(pady=5)

    tk.Button(frame_aux_tit, text="确认", command=lambda: obstacle_funcs["parameter"](e_parameter)).pack()
    par_state = tk.Button(frame_aux_inp, text="隐藏", command=lambda: obstacle_funcs["hidden"](par_state))
    par_state.pack()

    # ===== 圆 =====
    tk.Label(frame_aux_tit2, text="圆(m)：", font=font).pack()
    var_cir = tk.StringVar()
    e_cir = Entry(frame_aux_inp2, textvariable=var_cir, width=3)
    e_cir.pack()

    tk.Button(frame_aux_but, text="确认", command=lambda: obstacle_funcs["circular"](var_cir)).pack()

    # ===== 测量模块 =====
    but_1 = tk.Button(
        frame_mea_com_lef,
        text="长度测量",
        command=tool_funcs["pen"],
        width=btn_width,
        height=1,
    )
    but_1.pack()

    # ===== 障碍号 =====
    tk.Label(frame_temp_9, text="障碍号：", font=font).pack(side="left")
    var_id = tk.StringVar()
    e_id = Entry(frame_temp_9, textvariable=var_id, width=4)
    e_id.pack(side="left")

    tk.Button(frame_temp_8, text="确认", command=lambda: obstacle_funcs["insert"](e_id)).pack(padx=1)

    # ===== 窗口上的全局控件 =====
    tk.Label(win, text="全局障碍长度(m):", font=font).place(x=200, y=10)
    var_len = tk.StringVar(value="4")
    len_entry = Entry(win, textvariable=var_len, width=4)
    len_entry.place(x=330, y=10)

    tk.Button(win, text="确认", command=lambda: None).place(x=300, y=40)

    tk.Button(win, text="清除水印", command=tool_funcs["remove_f"]).place(x=180, y=40)

    # ===== 路线图长度 =====
    tk.Label(win, text="长度(m):", font=font).place(x=10, y=10)
    var_l_w = tk.StringVar(value="90")
    var_l_h = tk.StringVar(value="60")
    var_l_w_inp = Entry(win, textvariable=var_l_w, width=5)
    var_l_w_inp.place(x=80, y=10)

    tk.Label(win, text="宽度(m):", font=font).place(x=10, y=40)
    var_l_h_inp = Entry(win, textvariable=var_l_h, width=5)
    var_l_h_inp.place(x=80, y=40)

    # 绑定确认按钮到 found 函数
    tk.Button(win, text="确认", command=lambda: found(win, canvas, var_l_w, var_l_h)).place(x=50, y=70)

    # 导出路线图变量供全局使用
    globals()["var_l_w"] = var_l_w
    globals()["var_l_h"] = var_l_h
    globals()["var_l_w_inp"] = var_l_w_inp
    globals()["var_l_h_inp"] = var_l_h_inp

    # 创建按钮颜色切换函数引用（供外部使用）
    globals()["but_0"] = but_0
    globals()["but_1"] = but_1
    globals()["but_3"] = but_3

    # ===== 障碍物按钮 =====

    # 使用本地定义的障碍物创建函数（无需额外参数）
    create_obstacle_tools(
        main_window.get_frame("frame_temp_1"),
        main_window.get_frame("frame_temp_2"),
        main_window.get_frame("frame_temp_3"),
        main_window.get_frame("frame_temp_4"),
        main_window.get_frame("frame_temp_5"),
        main_window.get_frame("frame_temp_6"),
        main_window.get_frame("frame_temp_7"),
        gate,      # 使用本地函数
        compass,  # 使用本地函数
        water_barrier,  # 使用本地函数
        brick_wall,     # 使用本地函数
        line,          # 使用本地函数
        force,         # 使用本地函数
        live,          # 使用本地函数
        monorail,      # 使用本地函数
        oxer,          # 使用本地函数
        tirail,        # 使用本地函数
        combination_ab,    # 使用本地函数
        combination_abc,   # 使用本地函数
        lambda: None,  # 自定义障碍（未实现）
        lambda: None,  # 导入背景图（未实现）
    )


def main():
    """应用主入口"""
    # 初始化系统
    sys_name = platform.system()
    app_state = get_app_state()
    app_state.set_system(sys_name)

    # 获取主窗口
    main_window = get_main_window()
    win = main_window.window
    canvas = main_window.canvas

    # 设置根窗口引用（用于 tk 变量初始化）
    from src.state.app_state import AppState

    AppState.set_root_window(win)

    # 获取图像处理器
    image_processor = get_image_processor()

    # 获取编辑面板
    edit_panel = get_edit_panel(win)

    # 导出全局变量（向后兼容）
    _export_globals(win, canvas, main_window, app_state, edit_panel, sys_name)

    # 创建工具函数
    tool_funcs = _create_tool_functions(win, canvas, app_state, sys_name)
    globals().update(tool_funcs)

    # 创建障碍物创建函数（传入事件处理函数）
    obstacle_funcs = _create_obstacle_functions(
        canvas, app_state, image_processor,
        handlers={
            "mousedown_handler": tool_funcs["mousedown_handler"],
            "drag_handler": tool_funcs["drag_handler"],
            "mouseup_handler": tool_funcs["mouseup_handler"],
        }
    )
    globals().update(obstacle_funcs)

    # 创建菜单
    create_menu(
        win,
        app_state.what,
        tool_funcs["drag"],
        tool_funcs["rotate"],
        tool_funcs["pen"],
        tool_funcs["clear"],
        tool_funcs["remove_f"],
        tool_funcs["open_file"],
        tool_funcs["save_1"],
        tool_funcs["del_fg"],
        tool_funcs["currency_pen"],
        tool_funcs["about"],
        tool_funcs["open_web"],
    )

    # 创建UI按钮
    width = 10 if sys_name == "Windows" else 5
    _create_ui_buttons(
        win, canvas, app_state, main_window, tool_funcs, obstacle_funcs, width, sys_name
    )

    # 初始化赛事信息面板
    edit()

    # 添加赛事信息确认和修改按钮
    font = ("微软雅黑", 12)
    but1 = tk.Button(win, text="确认", command=dle, font=font)
    but1.place(x=1200 + 160, y=700)
    but2 = tk.Button(win, text="修改", command=edit, font=font)
    but2.place(x=1200 + 260, y=700)

    # 绑定快捷键
    _bind_shortcuts(win, app_state, canvas, sys_name)

    # 绑定鼠标移动事件（更新坐标显示）
    def on_mouse_move(event):
        x = event.x / 10 - 1.5
        y = event.y / 10 - 5
        canvas.itemconfig("鼠标x", text=f"x:{x:.2f}")
        canvas.itemconfig("鼠标y", text=f"y:{y:.2f}")

    canvas.bind("<Motion>", on_mouse_move)

    # 运行主循环
    win.mainloop()


def _export_globals(win, canvas, main_window, app_state, edit_panel, sys_name):
    """导出全局变量（向后兼容）"""
    # 窗口和画布
    globals()["win"] = win
    globals()["canvas"] = canvas

    # 状态
    globals()["app_state"] = app_state
    globals()["edit_panel"] = edit_panel
    globals()["sys_name"] = sys_name

    # Frames
    for name in [
        "frame_job",
        "frame_function",
        "frame_aux",
        "frame_mea",
        "frame_create",
        "frame_command_left",
        "frame_command_right",
        "frame_command",
        "frame_temp_1",
        "frame_temp_2",
        "frame_temp_3",
        "frame_temp_4",
        "frame_temp_5",
        "frame_temp_6",
        "frame_temp_7",
        "frame_temp_8",
        "frame_temp_9",
        "frame_aux_com",
        "frame_aux_com_lef",
        "frame_aux_com_rig",
        "frame_aux_tit",
        "frame_aux_inp",
        "frame_aux_tit2",
        "frame_aux_inp2",
        "frame_aux_but",
        "frame_mea_com",
        "frame_mea_com_lef",
        "frame_mea_com_rig",
        "frame_info",
        "frame_tit",
        "frame_inp",
        "frame_por",
    ]:
        frame = main_window.get_frame(name)
        if frame:
            globals()[name] = frame

    # 赛事信息标签列表
    globals()["info"] = [
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

    # 图像路径
    globals()["force_image"] = IMAGE_PATHS.get("force", "img/force.png")
    globals()["compass_image"] = IMAGE_PATHS.get("compass", "img/compass.png")
    globals()["water_barrier_image"] = IMAGE_PATHS.get(
        "water_barrier", "img/water_barrier.png"
    )
    globals()["brick_wall_image"] = IMAGE_PATHS.get("brick_wall", "img/brick_wall.png")
    globals()["line_image"] = IMAGE_PATHS.get("line", "img/line.png")
    globals()["gate_image"] = IMAGE_PATHS.get("gate", "img/gate.png")
    globals()["circular_image"] = IMAGE_PATHS.get("circular", "img/circular.png")
    globals()["icon_path"] = IMAGE_PATHS.get("icon", "img/ic.png")

    # 状态变量
    globals()["sys_name"] = sys_name
    globals()["FONT"] = ("微软雅黑", 15 if sys_name == "Darwin" else 12)
    globals()["WIDTH"] = 900
    globals()["HEIGHT"] = 600


def _create_tool_functions(win, canvas, app_state, sys_name):
    """创建工具函数"""

    # 选中对象存储
    _selected_objects = {}  # tag -> (obj, startx, starty)
    choice_tup = []
    _start_x = 0
    _start_y = 0

    def mousedown_handler(tag, event):
        """鼠标按下处理"""
        global _start_x, _start_y
        _start_x = event.x
        _start_y = event.y

        from src.models.canvas_objects import CanvasObject
        # 找到对应的 CanvasObject 实例
        obj = CanvasObject.get_instance_by_tag(tag)
        if obj:
            _selected_objects[tag] = [obj, event.x, event.y]
            obj.mousedown(
                tag, [event.x, event.y],
                lambda x: None, lambda x: None,
                app_state.what, choice_tup
            )
            canvas.lift(tag)

        # 清除旧的选择框
        canvas.delete("choice")

    def drag_handler(img_id, event):
        """鼠标拖动处理"""
        global px, lastDraw, remove_px

        # 橡皮擦模式
        if app_state.what.get() == 2:
            te = canvas.find_overlapping(
                event.x - 10, event.y - 10, event.x + 10, event.y + 10
            )
            for i in te:
                if str(i).isdigit():
                    canvas.delete(i)
            return

        # 铅笔模式（测量）
        if app_state.what.get() == 1:
            global lastDraw
            if click_num == 1:
                lastDraw = canvas.create_line(
                    _start_x, _start_y, event.x, event.y,
                    fill="#000000", width=app_state.font_size,
                    tags=("line", "不框选"), smooth=True
                )
                x1, y1, x2, y2 = canvas.coords(lastDraw)
                px += (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) / 10
                temp_px = (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) / 10
                remove_px[lastDraw] = temp_px
                canvas.itemconfig("实时路线", text="%.2fm" % px)
            return

        # 拖动模式
        for tag, (obj, startx, starty) in list(_selected_objects.items()):
            if app_state.what.get() == 0 and not choice_tup:
                dx = event.x - startx
                dy = event.y - starty
                canvas.move(tag, dx, dy)
                if obj.line_tag:
                    canvas.move(obj.line_tag, dx, dy)
                obj.current_x += dx
                obj.current_y += dy
                _selected_objects[tag] = [obj, event.x, event.y]

    def mouseup_handler(event):
        """鼠标释放处理"""
        global px, lastDraw, end, choice_tup

        for tag, (obj, startx, starty) in list(_selected_objects.items()):
            dx = event.x - startx
            dy = event.y - starty
            if dx != 0 or dy != 0:
                app_state.stack.append(("移动", (obj.id,), (dx, dy)))
        _selected_objects.clear()

        # 铅笔模式结束
        if app_state.what.get() == 1:
            click_num = 2
            app_state.click_num = 2
            end.append(canvas.find_withtag("line")[-1] if canvas.find_withtag("line") else 0)

    def drag():
        app_state.what.set(0)
        app_state.no_what.set(0)

    def pen():
        app_state.what.set(1)
        app_state.no_what.set(1)
        app_state.click_num = 1

    def rotate():
        app_state.what.set(3)
        app_state.no_what.set(3)

    def remove():
        """橡皮擦工具"""
        app_state.what.set(2)
        app_state.no_what.set(2)

    def clear():
        canvas.delete("line")
        canvas.delete("rubber")
        app_state.px = 0
        canvas.itemconfig("实时路线", text="%.2fm" % app_state.px)
        app_state.click_num = 1

    def remove_f():
        canvas.delete("watermark")

    def open_file():
        if not os.path.exists("./ms_download"):
            os.mkdir("./ms_download")
        path = os.getcwd() + "/ms_download"
        if sys_name == "Windows":
            subprocess.Popen(["explorer", path])
        else:
            subprocess.call(["open", path])

    def save_1():
        _save_image(win, canvas, True, sys_name)

    def del_fg():
        canvas.delete("bg")

    def currency_pen():
        app_state.font_size = simpledialog.askinteger(
            "输入字号", prompt="", initialvalue=app_state.font_size
        )

    def about():
        app = tk.Toplevel(win)
        app.title("关于软件")
        app.geometry("300x200")
        app_frame = tk.Frame(app)
        app_frame.pack()
        tk.Label(app_frame, text="路线设计", font=("宋体", 15, "bold")).pack()
        tk.Label(app_frame, text="版本 1.0").pack()
        tk.Label(app_frame, text="Copyright © 2022 山东体育学院").pack()

    def open_web():
        import webbrowser

        webbrowser.open("https://gitee.com/gmlwb/ms/blob/master/README.md")

    return {
        "drag": drag,
        "pen": pen,
        "rotate": rotate,
        "remove": remove,
        "clear": clear,
        "remove_f": remove_f,
        "open_file": open_file,
        "save_1": save_1,
        "del_fg": del_fg,
        "currency_pen": currency_pen,
        "about": about,
        "open_web": open_web,
        "mousedown_handler": mousedown_handler,
        "drag_handler": drag_handler,
        "mouseup_handler": mouseup_handler,
    }


def _create_obstacle_functions(canvas, app_state, image_processor, handlers=None):
    """创建障碍物创建函数"""
    # 获取事件处理函数
    mousedown_handler = handlers.get("mousedown_handler") if handlers else lambda t, e: None
    drag_handler = handlers.get("drag_handler") if handlers else lambda t, e: None
    mouseup_handler = handlers.get("mouseup_handler") if handlers else lambda e: None

    # 从全局获取图像路径
    force_image = IMAGE_PATHS.get("force", "img/force.png")
    compass_image = IMAGE_PATHS.get("compass", "img/compass.png")
    water_barrier_image = IMAGE_PATHS.get("water_barrier", "img/water_barrier.png")
    brick_wall_image = IMAGE_PATHS.get("brick_wall", "img/brick_wall.png")
    line_image = IMAGE_PATHS.get("line", "img/line.png")
    gate_image = IMAGE_PATHS.get("gate", "img/gate.png")
    circular_image = IMAGE_PATHS.get("circular", "img/circular.png")

    def monorail():
        app_state.index_img += 1
        image_path = image_processor.expand(image_processor.get_one_path())
        image_path = image_processor.start_direction(image_path)
        from src.models.canvas_objects import CreateImg

        CreateImg(canvas, app_state.index_img, image_path, obstacle="monorail").create(
            mousedown_handler,
            drag_handler,
            mouseup_handler,
            lambda x: None,
            app_state.stack,
        )

    def oxer():
        app_state.index_img += 1
        image_path = image_processor.merge(10)
        image_path = image_processor.start_direction(image_path)
        from src.models.canvas_objects import CreateImg

        CreateImg(canvas, app_state.index_img, image_path, obstacle="oxer").create(
            mousedown_handler,
            drag_handler,
            mouseup_handler,
            lambda x: None,
            app_state.stack,
        )

    def live():
        app_state.index_img += 1
        image_path = image_processor.live_one_tool()
        from src.models.canvas_objects import CreateImg

        CreateImg(canvas, app_state.index_img, image_path, obstacle="live").create(
            mousedown_handler,
            drag_handler,
            mouseup_handler,
            lambda x: None,
            app_state.stack,
        )

    def force():
        app_state.index_img += 1
        from src.models.canvas_objects import CreateImg

        CreateImg(canvas, app_state.index_img, force_image).create(
            mousedown_handler,
            drag_handler,
            mouseup_handler,
            lambda x: None,
            app_state.stack,
        )

    def compass():
        app_state.index_img += 1
        image_path = image_processor.expand(compass_image)
        from src.models.canvas_objects import CreateImg

        CreateImg(canvas, app_state.index_img, image_path).create(
            mousedown_handler,
            drag_handler,
            mouseup_handler,
            lambda x: None,
            app_state.stack,
        )

    def water_barrier():
        app_state.index_img += 1
        image_path = image_processor.expand(water_barrier_image)
        image_path = image_processor.start_direction(image_path)
        from src.models.canvas_objects import CreateImg

        CreateImg(canvas, app_state.index_img, image_path, obstacle="water").create(
            mousedown_handler,
            drag_handler,
            mouseup_handler,
            lambda x: None,
            app_state.stack,
        )

    def brick_wall():
        app_state.index_img += 1
        image_path = image_processor.expand(brick_wall_image)
        from src.models.canvas_objects import CreateImg

        CreateImg(canvas, app_state.index_img, image_path).create(
            mousedown_handler,
            drag_handler,
            mouseup_handler,
            lambda x: None,
            app_state.stack,
        )

    def line():
        app_state.index_img += 1
        image_path = image_processor.expand(line_image)
        image_path = image_processor.start_direction(image_path)
        from src.models.canvas_objects import CreateImg

        CreateImg(canvas, app_state.index_img, image_path).create(
            mousedown_handler,
            drag_handler,
            mouseup_handler,
            lambda x: None,
            app_state.stack,
        )

    def gate():
        app_state.index_img += 1
        image_path = image_processor.expand(gate_image)
        from src.models.canvas_objects import CreateImg

        CreateImg(canvas, app_state.index_img, image_path).create(
            mousedown_handler,
            drag_handler,
            mouseup_handler,
            lambda x: None,
            app_state.stack,
        )

    def circular(var_cir=None):
        """创建圆"""
        app_state.index_img += 1
        cir_value = var_cir.get() if var_cir else "1"
        cir = int(cir_value) * 10
        img = Image.open(circular_image)
        img = img.resize((cir, cir))
        cir_path = _get_img_path("cir.png")
        img.save(cir_path)
        from src.models.canvas_objects import CreateImg

        CreateImg(canvas, app_state.index_img, cir_path).create(
            mousedown_handler,
            drag_handler,
            mouseup_handler,
            lambda x: None,
            app_state.stack,
        )

    def combination_ab():
        app_state.index_img += 1
        image_path = image_processor.merge_ab(state=1, m1=30)
        from src.models.canvas_objects import CreateImg

        CreateImg(
            canvas, app_state.index_img, image_path, obstacle="combination_ab"
        ).create(
            mousedown_handler,
            drag_handler,
            mouseup_handler,
            lambda x: None,
            app_state.stack,
        )

    def combination_abc():
        app_state.index_img += 1
        image_path = image_processor.merge_ab(state=1, m1=30, m2=30)
        from src.models.canvas_objects import CreateImg

        CreateImg(
            canvas, app_state.index_img, image_path, obstacle="combination_abc"
        ).create(
            mousedown_handler,
            drag_handler,
            mouseup_handler,
            lambda x: None,
            app_state.stack,
        )

    def tirail():
        app_state.index_img += 1
        image_path = image_processor.merge(10, 10)
        from src.models.canvas_objects import CreateImg

        CreateImg(canvas, app_state.index_img, image_path, obstacle="tirail").create(
            mousedown_handler,
            drag_handler,
            mouseup_handler,
            lambda x: None,
            app_state.stack,
        )

    # ===== 障碍号和参数功能 =====
    def insert(e_id):
        """障碍号确认"""
        global index_txt
        var = var_id.get()
        if var:
            from src.models.canvas_objects import CreateTxt
            index_txt += 1
            CreateTxt(canvas, index_txt).create(var)
            e_id.delete(0, "end")
            drag()

    def parameter(e_parameter):
        """障碍参数确认"""
        global index_txt
        var = var_parameter.get()
        if var:
            from src.models.canvas_objects import CreateParameter
            index_txt += 1
            CreateParameter(canvas, index_txt).create(var)
            e_parameter.delete(0, "end")
            drag()

    def hidden(par_state):
        """隐藏障碍参数"""
        global par_index
        if par_index:
            canvas.itemconfig("parameter", state="hidden")
            par_state.config(text="显示")
            par_index = 0
        else:
            canvas.itemconfig("parameter", state="normal")
            par_state.config(text="隐藏")
            par_index = 1

    return {
        "monorail": monorail,
        "oxer": oxer,
        "live": live,
        "force": force,
        "compass": compass,
        "water_barrier": water_barrier,
        "brick_wall": brick_wall,
        "line": line,
        "gate": gate,
        "circular": circular,
        "combination_ab": combination_ab,
        "combination_abc": combination_abc,
        "tirail": tirail,
        "insert": insert,
        "parameter": parameter,
        "hidden": hidden,
    }


# ===== 赛事信息相关全局变量 =====
info_var = []
pro_var = []
temp_txt = ""


def allow(info_vars, pro_value):
    """计算最佳时间"""
    try:
        s = info_vars[7].get()
        l = info_vars[8].get()
        if s.isdigit():
            s = float(s)
        else:
            s = float(s.split("/")[0][:-1])
        if l.isdigit():
            l = float(l)
        else:
            l = float(l.split("m")[0])
        t = s / l * 60
        pro_value.set("%.2fs" % t)
        return True
    except Exception as e:
        print(f"赛事信息出错：{e}")
        logger.warning(f"赛事信息计算出错: {e}", exc_info=True)
        return False


def dle():
    """赛事信息确认"""
    global temp_txt
    try:
        temp = {}
        for i in frame_tit.winfo_children():
            i.destroy()
        for i in frame_inp.winfo_children():
            i.destroy()
        for i in frame_por.winfo_children():
            i.destroy()
        for i in range(len(info_var)):
            if info_var[i].get():
                temp[info[i]] = info_var[i]

        for key, value in temp.items():
            if key == "比赛名称":
                temp_txt = value.get()
                canvas.itemconfig("比赛名称", text=temp_txt)
                continue
            font = 21 if sys_name == "Darwin" else 15
            tk.Label(frame_tit, text=key + ": ", font=("微软雅黑", font)).pack(
                padx=1, pady=4
            )
            tk.Label(frame_inp, text=value.get(), font=("微软雅黑", font)).pack(
                padx=1, pady=4
            )
            tk.Label(frame_por, text="").pack(padx=1, pady=7)

    except Exception as e:
        print(f"Error: {e}")
        messagebox.showerror("Error", "出错了")
        logger.warning(f"赛事信息确认出错: {e}", exc_info=True)


def edit():
    """修改赛事信息"""
    global info_var, pro_var
    temp_ = {}
    for i in range(len(info_var)):
        temp_[info[i]] = info_var[i].get()

    info_var = []
    pro_var = []
    for i in frame_tit.winfo_children():
        i.destroy()
    for i in frame_inp.winfo_children():
        i.destroy()
    for i in frame_por.winfo_children():
        i.destroy()
    for i in info:
        font = 20 if sys_name == "Darwin" else 13
        tk.Label(frame_tit, text=i + ":", font=("微软雅黑", font)).pack(padx=1, pady=3)
        var = tk.StringVar()
        pro_value = tk.StringVar()
        if temp_:
            var.set(temp_[i])
        info_var.append(var)
        pro_var.append(pro_value)
        y = 4 if sys_name == "Darwin" else 7
        if i == "允许时间":
            Entry(
                frame_inp,
                textvariable=var,
                width=15,
                validate="focusin",
                validatecommand=partial(allow, info_var, pro_value),
            ).pack(padx=1, pady=y)
            tk.Label(frame_por, textvariable=pro_value).pack(padx=1, pady=7)
            continue
        Entry(frame_inp, textvariable=var, width=15).pack(padx=1, pady=y)
        tk.Label(frame_por, textvariable=pro_value).pack(padx=1, pady=7)


def _save_image(win, canvas, include_info, sys_name):
    """保存图像"""
    current_time = time.strftime("%Y%m%d-%H%M%S")
    txt = "路线设计_" + current_time
    if not os.path.exists("./ms_download"):
        os.mkdir("./ms_download")
    path = filedialog.asksaveasfilename(
        title="保存为图片",
        filetypes=[("PNG", ".png")],
        initialdir=os.getcwd() + "/ms_download",
        initialfile=txt,
    )
    if path:
        path = path.split(".")[0]
        eps_path = path + ".eps"
        png_path = path + ".png"
        canvas.postscript(file=eps_path, colormode="color", font=("微软雅黑", 15))

        if sys_name == "Windows":
            EpsImagePlugin.gs_windows_binary = (
                os.getcwd() + r"\gs10.01.1-32bit\bin\gswin32.exe"
            )
            startupinfo = subprocess.STARTUPINFO()
            startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
            cmd = (
                f"{EpsImagePlugin.gs_windows_binary} -dSAFER -dBATCH -dNOPAUSE -sDEVICE=jpeg -r600 "
                f"-dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dEPSCrop -sOutputFile={png_path} {eps_path} "
            )
            subprocess.call(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW,
                startupinfo=startupinfo,
            )
        else:
            img = Image.open(eps_path)
            img.save(png_path)

        os.remove(eps_path)
        messagebox.showinfo("成功", f"保存成功,\n路径:{png_path}")


def _bind_shortcuts(win, app_state, canvas, sys_name):
    """绑定快捷键"""

    def undo(event):
        if event.widget == win and app_state.stack:
            item = app_state.stack.pop()
            if item[0] == "删除":
                for i in item[1]:
                    canvas.itemconfig(i, state="normal")
            elif item[0] == "长度测量":
                ids, temp_px = item[1]
                for i in ids:
                    canvas.delete(i)
                app_state.px -= temp_px
                canvas.itemconfig("实时路线", text="%.2fm" % app_state.px)

    def delete(event):
        if "ent" not in str(event.widget):
            items = canvas.find_withtag("choice_start")[:-1]
            if items:
                canvas.itemconfig("choice_start", state="hidden")
                app_state.stack.append(("删除", items))
            else:
                canvas.delete("choice")

    win.bind("<Command-KeyPress-z>", undo)
    win.bind("<Control-KeyPress-z>", undo)
    win.bind("<BackSpace>", delete)


if __name__ == "__main__":
    main()
