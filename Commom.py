import tkinter as tk
from tkinter import Checkbutton
from tkinter import messagebox
from functools import partial
from PIL import Image, ImageTk, ImageOps, ImageGrab

# 创建窗口
win = tk.Tk()
win.title("路线设计")

# 程序最大化
w = win.winfo_screenwidth()
h = win.winfo_screenheight()
win.geometry(f"{w}x{h}")
win.state("zoomed")
win.iconphoto(False, tk.PhotoImage(file='img/ic.png'))

# 全局变量
WIDTH = 900
HEIGHT = 600
FONT = ("微软雅黑", 18)
X = tk.IntVar(value=0)
Y = tk.IntVar(value=0)
what = tk.IntVar(value=0)
lastDraw = 0
end = [0]
size = 1
font_size = 1
remove_size = 1
state_f = 1
px = 0
remove_px = {}
from focus import Focus

focus = Focus(win)
index = 0
index_txt = 0
index_img = 0
temp_txt = None

# 单横木
one_path = 'img/one.png'
# 利物浦
live_image = "img/liverpool.png"
# 双横木
oxer_image = "img/oxer.png"
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
