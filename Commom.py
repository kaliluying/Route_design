import math
import tkinter as tk
from tkinter import Checkbutton
from tkinter import messagebox
from functools import partial
from PIL import Image, ImageTk, ImageOps, ImageGrab, EpsImagePlugin
from Middleware import *

# 创建窗口
win = tk.Tk()
win.title("路线设计")

# 程序最大化
W = win.winfo_screenwidth()
H = win.winfo_screenheight()
win.geometry(f"{W}x{H}")
win.state("zoomed")
win.iconphoto(False, tk.PhotoImage(file='img/ic.png'))

# 全局变量
WIDTH = 900
HEIGHT = 600
FONT = ("微软雅黑", 15)
X = tk.IntVar(value=0)
Y = tk.IntVar(value=0)
what = tk.IntVar(value=0)
no_what = tk.IntVar(value=0)

# 初始点
start_x = tk.IntVar(value=0)
start_y = tk.IntVar(value=0)
# 终止点
end_x = tk.IntVar(value=0)
end_y = tk.IntVar(value=0)
# 点击次数
click_num = 1

# 网格状态
grid_start = 0
# 网格是否创建
create_grid = False

# 比赛名
temp_txt = None

# 多选选中id
choice_tup = []

# 辅助信息状态
aux_stare = True

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
    h = int(get_len()) * 10
    image = image.resize((w, h))
    path = image_path.replace('.', '-adj.')
    image.save(path)

    return path


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
    return "img/liverpool.png"


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
frame_function = tk.Frame(win, name='左侧功能栏')
frame_function.place(x=5, y=150)

# 工作模块容器
frame_job = tk.Frame(frame_function, relief='ridge', bd=2, name='工作模块')
# 辅助模块容器
frame_aux = tk.Frame(frame_function, relief='ridge', bd=2, name='辅助模块')
# 测量模块容器
frame_mea = tk.Frame(frame_function, relief='ridge', bd=2, name='测量模块')

frame_job.pack()
frame_aux.pack()
frame_mea.pack()

# 功能容器
frame_command = tk.Frame(frame_job, name='功能容器')
frame_command.pack()
frame_command_left = tk.Frame(frame_command)
frame_command_right = tk.Frame(frame_command)
frame_command_left.pack(side="left")
frame_command_right.pack(side="right")

# 旋转、备注编辑主容器
frame_edit = tk.Frame(frame_job, name='旋转、备注')
frame_edit.pack()

# 旋转容器
frame_x = tk.Frame(frame_edit, name='旋转')
frame_x.pack()
frame_focus_x_ladel = tk.Frame(frame_x)
frame_focus_x_ent = tk.Frame(frame_x)
frame_focus_x_but = tk.Frame(frame_x)
frame_focus_x_but.pack(side='bottom')
frame_focus_x_ladel.pack(side='left')
frame_focus_x_ent.pack(side='right')

# 备注容器
frame_z = tk.Frame(frame_edit, name='备注')
frame_z.pack()
frame_focus_z_ladel = tk.Frame(frame_z)
frame_focus_z_ent = tk.Frame(frame_z)
frame_focus_z_but = tk.Frame(frame_z)
frame_focus_z_but.pack(side='bottom')
frame_focus_z_ladel.pack(side='left')
frame_focus_z_ent.pack(side='right')

# 辅助功能容器
frame_aux_com = tk.Frame(frame_aux, name='辅助功能容器')
frame_aux_com.pack()
frame_aux_com_lef = tk.Frame(frame_aux_com)
frame_aux_com_rig = tk.Frame(frame_aux_com)
frame_aux_com_lef.pack(side='left')
frame_aux_com_rig.pack(side='right')

# 辅助信息容器
frame_aux_info = tk.Frame(frame_aux, name='辅助信息容器')
frame_aux_info.pack()
frame_aux_tit = tk.Frame(frame_aux_info)
frame_aux_inp = tk.Frame(frame_aux_info)
frame_aux_tit.pack(side='left')
frame_aux_inp.pack(side='right')

# 测量功能容器
frame_mea_com = tk.Frame(frame_mea, name='测量功能容器')
frame_mea_com.pack()
frame_mea_com_lef = tk.Frame(frame_mea_com)
frame_mea_com_rig = tk.Frame(frame_mea_com)
frame_mea_com_lef.pack(side='left')
frame_mea_com_rig.pack(side='right')

# 障碍按键容器
frame_create = tk.Frame(win, name='按键')
frame_create.place(x=200, y=5)
frame_temp_1 = tk.Frame(frame_create)
frame_temp_2 = tk.Frame(frame_create)
frame_temp_3 = tk.Frame(frame_create)
frame_temp_4 = tk.Frame(frame_create)
frame_temp_5 = tk.Frame(frame_create)
frame_temp_6 = tk.Frame(frame_create)
frame_temp_7 = tk.Frame(frame_create)

frame_temp_1.pack(side="left")
frame_temp_2.pack(side="left")
frame_temp_3.pack(side="left")
frame_temp_4.pack(side="left")
frame_temp_5.pack(side="left")
frame_temp_6.pack(side="left")
frame_temp_7.pack(side="left")

from focus import Focus

focus = Focus(frame_job)
