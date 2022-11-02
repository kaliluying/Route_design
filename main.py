import os
import re
import math
import webbrowser
import subprocess
import tkinter.simpledialog
from scale import CreateImg, CreateTxt
from Tools import *
from Commom import *


# 障碍号确认
def insert():
    global index_txt
    var = var_id.get()
    index_txt += 1
    CreateTxt(canvas, index_txt).create_txt(var)
    e_id.delete(0, 'end')


# 单横木
def monorail():
    global index_img
    image_path = expand(one_path)
    image_path = start_direction(image_path)
    index_img += 1
    CreateImg(canvas, index_img, image_path).create_img()


# 双横木
def oxer():
    global index_img
    image_path = expand(oxer_image)
    image_path = start_direction(image_path)
    index_img += 1
    CreateImg(canvas, index_img, image_path, obstacle='oxer').create_img()


# 三横木
def tirail():
    global index_img
    image_path = merge(10, 10)
    index_img += 1
    CreateImg(canvas, index_img, image_path, obstacle='tirail').create_img()


# AB组合障碍
def combination_ab():
    global index_img
    image_path = merge_ab(state=1, m1=30)
    index_img += 1
    CreateImg(canvas, index_img, image_path, obstacle="combination_ab").create_img()


# ABC组合障碍
def combination_abc():
    global index_img
    image_path = merge_ab(state=1, m1=30, m2=30)
    index_img += 1
    CreateImg(canvas, index_img, image_path, obstacle="combination_abc").create_img()


# 利物浦
def live():
    global index_img
    index_img += 1
    image_path = expand(live_image)
    image_path = start_direction(image_path)
    CreateImg(canvas, index_img, image_path).create_img()


# 强制通过点
def force():
    global index_img
    index_img += 1
    CreateImg(canvas, index_img, force_image).create_img()


# 指北针
def compass():
    global index_img
    index_img += 1
    image_path = expand(compass_image)
    CreateImg(canvas, index_img, image_path).create_img()


# 水障
def water_barrier():
    global index_img
    index_img += 1
    image_path = expand(water_barrier_iamge)
    image_path = start_direction(image_path)
    CreateImg(canvas, index_img, image_path).create_img()


# 砖墙
def brick_wall():
    global index_img
    index_img += 1
    image_path = expand(brick_wall_image)
    CreateImg(canvas, index_img, image_path).create_img()


# 起/终点线
def line():
    global index_img
    index_img += 1
    image_path = expand(line_image)
    image_path = start_direction(image_path)
    CreateImg(canvas, index_img, image_path).create_img()


# 进出口
def gate():
    global index_img
    index_img += 1
    image_path = expand(gate_image)
    CreateImg(canvas, index_img, image_path).create_img()


# 赛事标题确认
def title_ok(txt):
    global temp_txt
    temp_txt = txt
    china_list = re.findall(r"[\u4e00-\u9fa5]", txt)
    china = len(china_list) * 20
    letter = (len(txt) - len(china_list)) * 10
    t_x = (WIDTH // 2) - (china // 2 + letter // 2)
    if t_x < 0: messagebox.showinfo('INFO', "长度过长")
    title.configure(text=txt)
    title.place(x=t_x, y=120)


# 赛事信息确认
def dle():
    try:
        temp = {}
        for i in frame_tit.winfo_children():
            i.destroy()
        for i in frame_inp.winfo_children():
            i.destroy()
        for i in range(len(info_var)):
            if info_var[i].get():
                temp[info[i]] = info_var[i]

        for key, value in temp.items():
            if key == '比赛名称':
                title_ok(value.get())
                continue
            tk.Label(frame_tit, text=key + ': ', font=("微软雅黑", 21)).pack(padx=1, pady=4)
            tk.Label(frame_inp, text=value.get(), font=("微软雅黑", 21)).pack(padx=1, pady=4)

    except Exception as e:
        print("Error: " + str(e))
        messagebox.showerror("Error", "出错了")


# 修改赛事信息
def edit():
    temp_ = {}
    for i in range(len(info_var)):
        temp_[info[i]] = info_var[i].get()

    info_var.clear()
    for i in frame_tit.winfo_children():
        i.destroy()
    for i in frame_inp.winfo_children():
        i.destroy()
    for i in info:
        tk.Label(frame_tit, text=i + ":", font=("微软雅黑", 21)).pack(padx=1, pady=3)
        var = tk.StringVar()
        if temp_:
            var.set(temp_[i])
        info_var.append(var)
        temp = tk.Entry(frame_inp, textvariable=var)
        temp.pack(padx=1, pady=4)


# 生成路线图
def found():
    global WIDTH, HEIGHT, h1, h2, watermark
    w = var_l_w.get()
    h = var_l_h.get()
    if w.isdigit() and h.isdigit():
        WIDTH = int(w) * 10
        HEIGHT = int(h) * 10
        canvas.config(width=WIDTH, height=HEIGHT)
        canvas.pack()
        but1.place(x=WIDTH + 80, y=790)
        but2.place(x=WIDTH + 230, y=790)
        frame_info.place(x=WIDTH + 30, y=200)
        canvas.delete(h1, h2, watermark)
        wid = WIDTH / 10
        hei = HEIGHT / 10
        h1 = canvas.create_text(WIDTH - 40, 10, text=f"长：{wid}m")
        h2 = canvas.create_text(WIDTH - 40, 30, text=f"宽：{hei}m")
        if state_f:
            watermark = canvas.create_text(WIDTH / 2, HEIGHT / 2, text="山东体育学院",
                                           font=("行楷", int(WIDTH * 0.16), "bold", "italic"), fill="#e4e4dc",
                                           tags="watermark")
            canvas.lower("watermark")
        length.place(x=WIDTH - 30, y=140)

    else:
        messagebox.showerror('错误', '请输入正整数')
        if w.isdigit():
            var_l_h_inp.delete(0, 'end')
        if h.isdigit():
            var_l_w_inp.delete(0, 'end')


# 鼠标左键按下
def leftButtonDown(event):
    X.set(event.x)
    Y.set(event.y)


# 鼠标左键滚动事件
def leftButtonMove(event):
    global lastDraw, px, length, remove_px

    if what.get() == 1:
        lastDraw = canvas.create_line(X.get(), Y.get(), event.x, event.y,
                                      fill='#000000', width=font_size, tags="line")
        x = event.x - X.get()
        y = event.y - Y.get()
        if x > 0 and y > 0:
            px += (math.sqrt(x * x + y * y)) / 10
            temp_px = (math.sqrt(x * x + y * y)) / 10
        else:
            px += (abs(x + y)) / 10
            temp_px = (abs(x + y)) / 10
        remove_px[lastDraw] = temp_px
        length.config(text="%.2fm" % px)
        X.set(event.x)
        Y.set(event.y)

    # 橡皮擦
    elif what.get() == 2:
        lastDraw = canvas.create_rectangle(event.x - 10, event.y - 10, event.x + 10, event.y + 10,
                                           outline="#ececec", fill='#ececec', width=remove_size)


# 松开左键
def leftButtonUp(event):
    global lastDraw
    end.append(lastDraw)


def drag():
    what.set(0)


# 铅笔
def pen():
    what.set(1)


# 橡皮擦
def remove():
    what.set(2)


# 清屏
def clear():
    global px, length
    canvas.delete("line")
    px = 0
    length.config(text="%.2fm" % px)


# 撤销
def back():
    global end, remove_px, px, length
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

    length.config(text="%.2fm" % px)


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


def save_1():
    checkvar = '1'
    sava(checkvar)


def save_0():
    checkvar = '0'
    sava(checkvar)


# 保存
def sava(checkvar):
    x1 = 5
    y1 = title.winfo_y() + 40
    if checkvar == '1':
        x2 = f.winfo_x() + f.winfo_width() + frame_info.winfo_width() + 30
    elif checkvar == '0':
        x2 = f.winfo_x() + f.winfo_width() + 10
    y2 = f.winfo_y() + f.winfo_height() + 70

    txt = temp_txt if temp_txt else '路线设计'
    if not os.path.exists('./download'):
        os.mkdir('./download')
    path = os.getcwd() + f'/download/{txt}.png'
    try:
        ImageGrab.grab((x1, y1, x2, y2)).save(path)
        messagebox.showinfo("成功", f"保存成功,\n路径:{path}")
    except EOFError as e:
        print('Error saving image:', e)


# 打开文件保存路径
def open_file():
    if not os.path.exists('./download'):
        os.mkdir('./download')
    path = os.getcwd() + f'/download'
    subprocess.call(["open", path])


# # 清除水印
# def remove_f():
#     global state_f
#     canvas.delete(watermark)
#     state_f = 0


# 关于软件
def about():
    app = tk.Toplevel(win)
    app.title("关于软件")
    app.geometry("300x200")
    app_frame = tk.Frame(app)
    app_frame.pack()
    tk.Label(app_frame, image=icon_obj).pack(pady=15)
    tk.Label(app_frame, text="路线设计", font=("宋体", 15, "bold")).pack()
    tk.Label(app_frame, text="版本 1.0").pack()
    tk.Label(app_frame, text="Copyright © 2022 山东体育学院.\nAll rights reserved.").pack()
    tk.Label(app_frame, text="软件开发：许志亮 葛茂林").pack()


# 帮助文档
def open_web():
    webbrowser.open("https://github.com/kaliluying/Route_design/blob/main/README.md")


# 障碍号
tk.Label(win, text="障碍号：", font=FONT).place(x=830, y=20)
var_id = tk.StringVar()
e_id = tk.Entry(win, textvariable=var_id, width=4)
e_id.place(x=900, y=20)

tk.Button(win, text='确认', command=insert).place(x=870, y=50)

# 障碍物
tk.Button(win, text='进出口', command=gate).place(x=170, y=8)
tk.Button(win, text='指北针', command=compass).place(x=170, y=38)

tk.Button(win, text='水障', command=water_barrier).place(x=255, y=8)
tk.Button(win, text='砖墙', command=brick_wall).place(x=255, y=38)

tk.Button(win, text='起/终点线', command=line).place(x=332, y=8)
tk.Button(win, text='强制通过点', command=force).place(x=330, y=38)

tk.Button(win, text='利物浦', command=live).place(x=440, y=8)
tk.Button(win, text='单横木', command=monorail).place(x=440, y=38)

tk.Button(win, text='双横木', command=oxer).place(x=520, y=8)
tk.Button(win, text='三横木', command=tirail).place(x=520, y=38)

tk.Button(win, text='AB组合障碍', command=combination_ab).place(x=605, y=8)
tk.Button(win, text='ABC组合障碍', command=combination_abc).place(x=600, y=38)

# 路线图信息主容器
frame_l_info = tk.Frame(win)
frame_l_info.place(x=10, y=10)

# 路线二级容器
frame_lable = tk.Frame(frame_l_info)
frame_input = tk.Frame(frame_l_info)
frame_button = tk.Frame(frame_l_info)
frame_button.pack(side='bottom')
frame_lable.pack(side='left')
frame_input.pack(side='right')

# 路线图长度
tk.Label(frame_lable, text="长度(m):", font=FONT).pack()
var_l_w = tk.StringVar()
var_l_w.set('90')
var_l_w_inp = tk.Entry(frame_input, textvariable=var_l_w, width=5)
var_l_w_inp.pack()

# 路线图宽度
tk.Label(frame_lable, text="宽度(m):", font=FONT).pack()
var_l_h = tk.StringVar()
var_l_h.set("60")
var_l_h_inp = tk.Entry(frame_input, textvariable=var_l_h, width=5)
var_l_h_inp.pack()
tk.Button(frame_button, text="确认", command=found).pack()

# 路线图
f = tk.Frame(win, width=WIDTH, height=HEIGHT, bg="black", border=1)
f.place(x=5, y=170)
canvas = tk.Canvas(f, width=WIDTH, height=HEIGHT)
canvas.pack()

# 右上角显示路线长宽
w = WIDTH / 10
h = HEIGHT / 10
h1 = canvas.create_text(WIDTH - 40, 10, text=f"长：{w}m")
h2 = canvas.create_text(WIDTH - 40, 30, text=f"宽：{h}m")

# 左上角显示 5m的距离
canvas.create_text(35, 10, text="5m")
canvas.create_line(10, 15, 10, 20)
canvas.create_line(60, 15, 60, 20)
canvas.create_line(10, 20, 60, 20, )

# 右下显示，路线长度
length = tk.Label(win, text=f"{px / 10}m")
length.place(x=WIDTH - 30, y=140)

# 水印
watermark = canvas.create_text(WIDTH / 2, HEIGHT / 2, text="山东体育学院",
                               font=("行楷", int(WIDTH * 0.16), "bold", "italic"), fill="#e4e4dc", tags="watermark")

# 画图
canvas.bind('<Button-1>', leftButtonDown)  # 鼠标左键点击事件
canvas.bind('<B1-Motion>', leftButtonMove)  # 鼠标左键滚动事件
canvas.bind('<ButtonRelease-1>', leftButtonUp)  # 松开左键

# 标题
title = tk.Label(win, text="比赛名称", font=FONT)
title.place(x=350, y=120)

# 信息
info = [
    '比赛名称', '级别赛制', '比赛日期', '路线查看时间', '开赛时间', '判罚表', '障碍高度', '行进速度', '路线长度', '允许时间', '限制时间', '障碍数量', '跳跃数量', '附加赛',
    '路线设计师',
]

# 赛事信息主容器
frame_info = tk.Frame(win)
# 放赛事信息标题
frame_tit = tk.Frame(frame_info)
# 放赛事信息输入框
frame_inp = tk.Frame(frame_info)

frame_info.place(x=WIDTH + 30, y=200)
frame_tit.pack(side='left')
frame_inp.pack(side='right')

# 生成赛事信息
info_var = []
edit()

but1 = tk.Button(win, text="确认", command=dle)
but1.place(x=WIDTH + 80, y=790)
but2 = tk.Button(win, text="修改", command=edit)
but2.place(x=WIDTH + 230, y=790)

# 菜单栏
menu = tk.Menu(win)

# 工具栏
menuType = tk.Menu(menu, tearoff=0)
menu_sava = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="工具栏", menu=menuType)
menuType.add_radiobutton(label="指针拖动", command=drag, variable=what, value=0)
menuType.add_radiobutton(label="铅笔", command=pen, variable=what, value=1)
menuType.add_radiobutton(label="橡皮擦", command=remove, variable=what, value=2)

# 功能
function_menuType = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="功能", menu=function_menuType)
function_menuType.add_command(label="清屏", command=clear)
function_menuType.add_command(label="撤销", command=back)
# function_menuType.add_command(label="清除水印", command=remove_f)
function_menuType.add_command(label="打开文件保存位置", command=open_file)

menu_sava.add_command(label="保存(包含右侧赛事信息)", command=save_1)
menu_sava.add_command(label="保存(不包含右侧赛事信息)", command=save_0)

function_menuType.add_cascade(label="保存", menu=menu_sava)

# 字号
font_menuType = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="字号", menu=font_menuType)
font_menuType.add_command(label="通用", command=currency_font)
font_menuType.add_command(label="铅笔", command=currency_pen)
font_menuType.add_command(label="橡皮擦", command=currency_remove)

# 帮助
app_help = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="帮助", menu=app_help)
app_help.add_command(label="关于软件", command=about)
app_help.add_command(label="帮助文档", command=open_web)

win.config(menu=menu)

win.mainloop()
