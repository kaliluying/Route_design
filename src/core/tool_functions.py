"""
工具函数模块
将 main.py 中的工具函数分离到这里
"""
import tkinter as tk
import tkinter.simpledialog
from tkinter import messagebox

# 使用统一的日志模块
from src.core.logger import get_logger


def create_tool_functions(win, what, no_what, set_color, canvas,
                          px, set_px, click_num, set_click_num,
                          stack, remove_px, end, route_click,
                          font_size, remove_size, size,
                          sys_name, but_0, but_1, but_3):
    """
    创建工具函数
    :return: 包含所有工具函数的字典
    """
    # 拖动
    def drag():
        what.set(0)
        set_color()
        no_what.set(0)

    # 铅笔
    def pen():
        global click_num
        what.set(1)
        set_color()
        no_what.set(1)
        click_num = 1

    # 橡皮擦
    def remove():
        what.set(2)
        set_color()
        no_what.set(2)

    # 旋转
    def rotate():
        what.set(3)
        set_color()
        no_what.set(3)

    # 画弧
    def arc():
        what.set(4)
        set_color()
        no_what.set(4)

    # 清屏
    def clear():
        global px, click_num
        canvas.delete("line")
        canvas.delete("rubber")
        px = 0
        canvas.itemconfig('实时路线', text="%.2fm" % px)
        click_num = 1
        to_be_deleted = []
        for i in range(len(stack)):
            if stack[i][0] == '长度测量':
                to_be_deleted.append(i)
        for idx in reversed(to_be_deleted):
            stack.pop(idx)

    # 撤销
    def back():
        global end, remove_px, px
        temp = 0
        temp_dict = {}
        iteration = remove_px.keys()
        for i in range(end[-2] + 1, end[-1] + 1):
            if next(iter(remove_px)) > i:
                continue
            canvas.delete(i)
        for i in iteration:
            if i > end[-2]:
                temp += remove_px[i]
                temp_dict[i] = remove_px[i]
        for i in temp_dict.keys():
            if i in remove_px:
                del remove_px[i]
        end.pop()
        px -= temp
        canvas.itemconfig('实时路线', text="%.2fm" % px)

    # 通用字号
    def currency_font():
        global font_size, remove_size, size
        size = tkinter.simpledialog.askinteger('输入字号', prompt='', initialvalue=size)
        font_size = remove_size = size

    # 铅笔字号
    def currency_pen():
        global font_size
        font_size = tkinter.simpledialog.askinteger('输入字号', prompt='', initialvalue=font_size)

    # 橡皮擦字号
    def currency_remove():
        global remove_size
        remove_size = tkinter.simpledialog.askinteger('输入字号', prompt='', initialvalue=remove_size)

    return {
        'drag': drag,
        'pen': pen,
        'remove': remove,
        'rotate': rotate,
        'arc': arc,
        'clear': clear,
        'back': back,
        'currency_font': currency_font,
        'currency_pen': currency_pen,
        'currency_remove': currency_remove,
    }


def create_canvas_tools(win, canvas, X, Y, what, no_what, but_0, but_1, but_3,
                        sys_name, frame_mea_com_rig, frame_command_left, frame_command_right,
                        width):
    """创建画布工具按钮"""
    # 工作模块按钮
    but_0 = tk.Button(frame_command_left, text='拖动', command=None, fg='red', width=width, height=1)
    but_0.pack()
    but_3 = tk.Button(frame_command_left, text='旋转', command=None, width=width, height=1)
    but_3.pack()

    # 测量模块按钮
    tk.Button(frame_mea_com_rig, text='清屏', command=None, width=width, height=1).pack()

    # 功能按钮
    tk.Button(frame_command_right, text='置底', command=None, width=width, height=1).pack()
    tk.Button(frame_command_right, text='删除', command=None, width=width, height=1).pack()

    return but_0, but_3


def create_aux_tools(frame_aux_com_lef, frame_aux_com_rig, width, grid_func, info_func):
    """创建辅助工具按钮"""
    tk.Button(frame_aux_com_lef, text='网格辅助线', command=grid_func, width=width, height=1).pack()
    aux_info = tk.Button(frame_aux_com_rig, text='隐藏辅助信息', command=info_func, width=width, height=1)
    aux_info.pack()
    return aux_info


def create_obstacle_tools(frame_temp_1, frame_temp_2, frame_temp_3, frame_temp_4,
                          frame_temp_5, frame_temp_6, frame_temp_7, gate_func, compass_func,
                          water_barrier_func, brick_wall_func, line_func, force_func,
                          live_func, monorail_func, oxer_func, tirail_func,
                          combination_ab_func, combination_abc_func, custom_func, fg_func):
    """创建障碍物按钮"""
    # 第一行
    tk.Button(frame_temp_1, text='进出口', command=gate_func).pack()
    tk.Button(frame_temp_1, text='指北针', command=compass_func).pack()

    # 第二行
    tk.Button(frame_temp_2, text='水障', command=water_barrier_func).pack()
    tk.Button(frame_temp_2, text='砖墙', command=brick_wall_func).pack()

    # 第三行
    tk.Button(frame_temp_3, text='起/终点线', command=line_func).pack()
    tk.Button(frame_temp_3, text='强制通过点', command=force_func).pack()

    # 第四行
    tk.Button(frame_temp_4, text='利物浦', command=live_func).pack()
    tk.Button(frame_temp_4, text='单横木', command=monorail_func).pack()

    # 第五行
    tk.Button(frame_temp_5, text='双横木', command=oxer_func).pack()
    tk.Button(frame_temp_5, text='三横木', command=tirail_func).pack()

    # 第六行
    tk.Button(frame_temp_6, text='AB组合障碍', command=combination_ab_func).pack()
    tk.Button(frame_temp_6, text='ABC组合障碍', command=combination_abc_func).pack()

    # 第七行
    tk.Button(frame_temp_7, text='自定义障碍', command=custom_func).pack()
    tk.Button(frame_temp_7, text='导入背景图', command=fg_func).pack()
