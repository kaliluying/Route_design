import os
import math
# import tkinter as ttk
import platform
import logging
import traceback
from tkinter import Checkbutton
from tkinter import messagebox
from functools import partial
from PIL import Image, ImageTk, ImageOps, ImageGrab, EpsImagePlugin

from Middleware import *
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

# 创建窗口
# win = ttk.Tk()
win = ttk.Window(
    title="路线设计",
    iconphoto='img/ic.png'
)

# 程序最大化
W = win.winfo_screenwidth()
H = win.winfo_screenheight()
win.geometry(f"{W}x{H}")
win.state("zoomed")
# win.iconphoto(False, ttk.PhotoImage(file='img/ic.png'))

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
    filename='logging.log',
)


# 设置异常处理函数
def log_error(exctype, value, tb):
    # 打印错误日志
    error_msg = ''.join(traceback.format_exception(exctype, value, tb))
    print(error_msg)
    logging.error("预料之外的错误: %s", error_msg, exc_info=True)


win.report_callback_exception = log_error

# 当前系统
sys_name = platform.system()

# 全局变量
WIDTH = 900
HEIGHT = 600
if sys_name == 'Darwin':
    FONT = ("微软雅黑", 15)
elif sys_name == 'Windows':
    FONT = ("微软雅黑", 12)
X = ttk.IntVar(value=0)
Y = ttk.IntVar(value=0)
what = ttk.IntVar(value=0)
no_what = ttk.IntVar(value=0)

canvas = ttk.Canvas(win, width=WIDTH + 30, height=HEIGHT + 80, highlightthickness=0)
canvas.place(x=175, y=100)

# img = Image.open('./img/bg1.png')
# img = img.resize((900, 600))
# img_obj = ImageTk.PhotoImage(img)
# canvas.create_image(15, 50, image=img_obj, anchor='nw', tags=('不框选', 'bg'))

#
# def d():
#     canvas.delete('bg')
#
#
# ttk.Button(win, text='del', command=d).place(x=0, y=0)

fg_img = None
fg_path = None

# 初始点
start_x = ttk.IntVar(value=0)
start_y = ttk.IntVar(value=0)
# 终止点
end_x = ttk.IntVar(value=0)
end_y = ttk.IntVar(value=0)
# 路线测量每一次点击的位置
route_click = []
# 点击次数
click_num = 1

# 网格状态
grid_start = 0
# 网格是否创建
create_grid = False

# 比赛名
temp_txt = None

# 多选框坐标
choice_tup = []

# 辅助信息状态
aux_stare = True

# 撤销栈
stack = []

# 撤销移动的还原点
move_x = ttk.IntVar(value=0)
move_y = ttk.IntVar(value=0)

# 多选框框中的状态
choice_start = False

# 记录长度测量时每一次点击的值
click = []

# 记录每次旋转的角度
rotate_ = [0]

lastDraw = 0
end = [0]
size = 1
font_size = 1
remove_size = 1
state_f = 1
px = 0
remove_px = {}

index = 0
index_txt = 0
index_img = 0

par_index = 1


# 拓展方法
def adjust_image_size(image_path):
    image = Image.open(image_path)
    w, h = image.size
    h = int(get_len() * 10)
    image = image.resize((w, h))
    if not os.path.exists('./temp_img'):
        os.mkdir('./temp_img')
    file_name = os.path.basename(image_path)
    name = file_name.replace('.', '-adj.')
    file_path = "./temp_img/" + name
    image.save(file_path)

    return file_path


# 装饰器
def load_image(func):
    def wrapper(*args, **kwargs):
        image = func(*args, **kwargs)
        adjusted_image = adjust_image_size(image)
        return adjusted_image

    return wrapper


@load_image
def get_one_path():
    """
    获取单横木
    :return:
    """
    return 'img/one.png'


@load_image
def get_live_path():
    """
    获取利物浦
    :return:
    """
    return "img/liverpool3.png"


@load_image
def get_oxer_path():
    """
    获取双横木
    :return:
    """
    return "img/oxer.png"


# 强制通过点
force_image = "img/force.png"
force_obj = ImageTk.PhotoImage(Image.open(force_image))
# 指北针
compass_image = "img/compass.png"
# 水障
water_barrier_iamge = "img/water_barrier.png"
# 砖墙
brick_wall_image = "img/brick_wall.png"
# 起/终点线
line_image = "img/line.png"
# 进出口
gate_image = "img/gate.png"
# icon
icon_path = "img/ic.png"
icon_obj = ImageTk.PhotoImage(Image.open(icon_path))
# 20米圆
circular_image = "img/circular.png"

# 左侧功能栏
frame_function = ttk.Frame(win, name='左侧功能栏', )
frame_function.place(x=5, y=150)

# 工作模块容器
frame_job = ttk.Frame(frame_function, name='工作模块')
# # 辅助模块容器
# frame_aux = ttk.Frame(frame_function, name='辅助模块')
# # 测量模块容器
# frame_mea = ttk.Frame(frame_function, name='测量模块')

frame_job.pack()

frame_aux_mea = ttk.Frame(win, name='辅助模块')
frame_aux_mea.place(x=5, y=530)
# 辅助模块容器
frame_aux = ttk.Frame(frame_aux_mea, name='辅助模块')
# 测量模块容器
frame_mea = ttk.Frame(frame_aux_mea, name='测量模块')
frame_aux.pack()
frame_mea.pack()

# 功能容器
frame_command = ttk.Frame(frame_job, name='功能容器')
frame_command.pack()
frame_command_left = ttk.Frame(frame_command)
frame_command_right = ttk.Frame(frame_command)
ttk.Label(frame_command, text='操作模块').pack()
frame_command_left.pack(side="left")
frame_command_right.pack(side="right")

# 旋转、备注编辑主容器
frame_edit = ttk.Frame(frame_job, name='旋转、备注', bootstyle="info")
frame_edit.pack()

# 旋转容器
frame_x = ttk.Frame(frame_edit, name='旋转')
frame_x.pack()
frame_focus_x_ladel = ttk.Frame(frame_x)
frame_focus_x_ent = ttk.Frame(frame_x)
frame_focus_x_but = ttk.Frame(frame_x)
frame_focus_x_but.pack(side='bottom')
frame_focus_x_ladel.pack(side='left')
frame_focus_x_ent.pack(side='right')

# 备注容器
frame_z = ttk.Frame(frame_edit, name='备注')
frame_z.pack()
frame_focus_z_ladel = ttk.Frame(frame_z)
frame_focus_z_ent = ttk.Frame(frame_z)
frame_focus_z_but = ttk.Frame(frame_z)
frame_focus_z_but.pack(side='bottom')
frame_focus_z_ladel.pack(side='left')
frame_focus_z_ent.pack(side='right')

# 辅助功能容器
frame_aux_com = ttk.Frame(frame_aux, name='辅助功能容器')
# frame_aux_com = ttk.Frame(frame_aux, name='辅助功能容器')
frame_aux_com.pack()
ttk.Label(frame_aux_com, text='辅助模块').pack()
frame_aux_com_lef = ttk.Frame(frame_aux_com)
frame_aux_com_rig = ttk.Frame(frame_aux_com)
frame_aux_com_lef.pack(side='left')
frame_aux_com_rig.pack(side='right')

# 辅助信息容器
frame_aux_info = ttk.Frame(frame_aux, name='辅助信息容器')
frame_aux_info.pack()

frame_aux_info_1 = ttk.Frame(frame_aux_info)
frame_aux_info_2 = ttk.Frame(frame_aux_info)
frame_aux_tit = ttk.Frame(frame_aux_info_1)
frame_aux_inp = ttk.Frame(frame_aux_info_1)
frame_aux_tit2 = ttk.Frame(frame_aux_info)
frame_aux_inp2 = ttk.Frame(frame_aux_info)
frame_aux_but = ttk.Frame(frame_aux_info)

frame_aux_info_1.pack()
frame_aux_info_2.pack()

frame_aux_tit.pack(side='left')
frame_aux_inp.pack(side='right')

frame_aux_tit2.pack(side='left')
frame_aux_inp2.pack(side='left')
frame_aux_but.pack(side='bottom')

# 测量功能容器
frame_mea_com = ttk.Frame(frame_mea, name='测量功能容器')
# frame_mea_com = ttk.Frame(frame_mea, name='测量功能容器')
frame_mea_com.pack()
frame_mea_com_lef = ttk.Frame(frame_mea_com)
frame_mea_com_rig = ttk.Frame(frame_mea_com)
frame_mea_com_lef.pack(side='left')
frame_mea_com_rig.pack(side='right')

# 障碍按键容器
frame_create = ttk.Frame(win, name='按键')
frame_create.place(x=400, y=5)
# ttk.Label(frame_create, text='生产模块').pack()
frame_temp_1 = ttk.Frame(frame_create)
frame_temp_2 = ttk.Frame(frame_create)
frame_temp_3 = ttk.Frame(frame_create)
frame_temp_4 = ttk.Frame(frame_create)
frame_temp_5 = ttk.Frame(frame_create)
frame_temp_6 = ttk.Frame(frame_create)
frame_temp_7 = ttk.Frame(frame_create)
frame_temp_8 = ttk.Frame(frame_create)
frame_temp_9 = ttk.Frame(frame_create)

frame_temp_1.pack(side="left")
frame_temp_2.pack(side="left")
frame_temp_3.pack(side="left")
frame_temp_4.pack(side="left")
frame_temp_5.pack(side="left")
frame_temp_6.pack(side="left")
frame_temp_7.pack(side="left")
frame_temp_8.pack(side="bottom")
frame_temp_9.pack(side="top")

from focus import Focus

focus = Focus(frame_job)
