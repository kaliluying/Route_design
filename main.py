import re
import math
import webbrowser
import tkinter as tk
from scale import Scale
import tkinter.filedialog
import tkinter.simpledialog
from tkinter import Checkbutton
from tkinter import messagebox
from SelectedCanvas import SelectedCanvas
from PIL import ImageGrab, Image, ImageOps, ImageTk

# 创建窗口
win = tk.Tk()
win.title("路线设计")

# 程序最大化
w = win.winfo_screenwidth()
h = win.winfo_screenheight()
win.geometry(f"{w}x{h}")
win.state("zoomed")
# win.iconbitmap("img/ic.ico")
win.iconphoto(False, tk.PhotoImage(file='img/ic.png'))
# 全局变量
WIDTH = 900
HEIGHT = 600
FONT = ("微软雅黑", 20)
X = tk.IntVar(value=0)
Y = tk.IntVar(value=0)
what = tk.IntVar(value=1)
lastDraw = 0
end = [0]
size = 1
font_size = 1
remove_size = 1
state_f = 1
px = 0

img_path = "img/one.png"

image = 'img/test-1.png'
# 组合障碍
com_image = "img/com.png"
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
# 行进方向
direction_image = "img/direction.png"
# 起/终点线
line_image = "img/line.png"
# 进出口
gate_image = "img/gate1.png"
# icon
icon_path = "img/ic.png"
icon_obj = ImageTk.PhotoImage(Image.open(icon_path))


# 检测字符串中是否是数字，支持正负整数，小数，中文数字如：一
def is_number(s):
    try:  # 如果能运行float(s)语句，返回True（字符串s是浮点数）
        float(s)
        return True
    except ValueError:  # ValueError为Python的一种标准异常，表示"传入无效的参数"
        pass  # 如果引发了ValueError这种异常，不做任何事情（pass：不做任何事情，一般用做占位语句）
    try:
        import unicodedata  # 处理ASCii码的包
        unicodedata.numeric(s)  # 把一个表示数字的字符串转换为浮点数返回的函数
        return True
    except (TypeError, ValueError):
        pass
    return False


# 合并图片
def merge(m, m1=0):
    global image, com_image
    img_obj = Image.open(image)
    img_obj2 = Image.open(image)
    result = Image.new(img_obj.mode, (m + m1 + 10, 40))
    result.paste(img_obj, box=(0, 0))
    result.paste(img_obj2, box=(m + m1, 0))
    if m1:
        image3 = Image.open(image)
        result.paste(image3, box=(m, 0))
        result.save("img/com2.png")
        com_image = "img/com2.png"
        return
    result.save("img/com.png")


# 图片扩展
def expand(path):
    img = Image.open(path)
    w, h = img.size
    if w < h:
        var_ex = h - w
        l = var_ex // 2
        r = var_ex - l
        t = 0
        b = 0
    elif w > h:
        var_ex = w - h
        t = var_ex // 2
        b = var_ex - t
        l = 0
        r = 0
    else:
        l = r = t = b = 0

    left_pad = l
    top_pad = t
    right_pad = r
    bottom_pad = b

    padding = (left_pad, top_pad, right_pad, bottom_pad)
    img2 = ImageOps.expand(img, padding, fill=(236, 236, 236, 0))
    image_path = path.replace('.', '-exp.')
    img2.save(image_path)
    return image_path


# 添加行进方向
def start_direction(image_path):
    img1 = Image.open(image_path)
    w, h = img1.size
    img2 = Image.open(direction_image)
    w1, h1 = img2.size
    img2 = img2.resize((w, h1))
    r, g, b, alpha = img2.split()
    img1.paste(img2, (0, h // 2 - 8), alpha)
    image_path = image_path.replace('.', '-dir.')
    img1.save(image_path)
    return image_path


# 障碍号确认
def insert():
    var = var_id.get()
    s = SelectedCanvas()
    s.create_widget(tk.Label, text=var, fg='black')
    s.place(x=900, y=100)
    s.remove()
    e_id.delete(0, 'end')


# 单横木
def monorail():
    image_path = expand(img_path)
    image_path = start_direction(image_path)
    mon = SelectedCanvas()
    scale = Scale(win, image_path, mon)
    scale.run()


# 双横木
def oxer():
    image_path = expand(oxer_image)
    image_path = start_direction(image_path)
    ox = SelectedCanvas()
    scale = Scale(win, image_path, ox)
    scale.run()


# 组合障碍
def combination():
    a_b = var_a_b.get()
    b_c = var_b_c.get()
    if (not a_b and not b_c) or (not is_number(a_b) and not is_number(b_c)):
        messagebox.showinfo("警告", "请输入数字")
        return
    if is_number(a_b) and is_number(b_c):
        m = a_b
        m1 = b_c
        m = int(float(m) * 10)
        m1 = int(float(m1) * 10)
        merge(m, m1)
        image_path = expand(com_image)
        image_path = start_direction(image_path)
        s = SelectedCanvas()
        com = Scale(win, image_path, s)
        com.run()

    else:
        m = a_b if is_number(a_b) else b_c
        m = int(float(m) * 10)
        merge(m)
        image_path = expand(com_image)
        image_path = start_direction(image_path)
        s = SelectedCanvas()
        com = Scale(win, image_path, s)
        com.run()


# 利物浦
def live():
    image_path = expand(live_image)
    image_path = start_direction(image_path)
    li = SelectedCanvas()
    scale = Scale(win, image_path, li)
    scale.run()


# 强制通过点
def force():
    # image_path = expand(force_image)
    fo = SelectedCanvas()

    fo.create_widget(tk.Label, image=force_obj)
    fo.place(x=1000, y=100)
    fo.remove()


# 指北针
def compass():
    image_path = expand(compass_image)
    com = SelectedCanvas()
    scale = Scale(win, image_path, com)
    scale.run()


# 水障
def water_barrier():
    image_path = expand(water_barrier_iamge)
    image_path = start_direction(image_path)
    water = SelectedCanvas()
    scale = Scale(win, image_path, water)
    scale.run()


# 砖墙
def brick_wall():
    image_path = expand(brick_wall_image)
    brick = SelectedCanvas()
    scale = Scale(win, image_path, brick)
    scale.run()


# 起/终点线
def line():
    image_path = expand(line_image)
    image_path = start_direction(image_path)
    li = SelectedCanvas()
    scale = Scale(win, image_path, li)
    scale.run()


# 进出口
def gate():
    image_path = expand(gate_image)
    ga = SelectedCanvas()
    scale = Scale(win, image_path, ga)
    scale.run()


# 赛事标题确认
def title_ok():
    txt = var_title.get()
    china_list = re.findall(r"[\u4e00-\u9fa5]", txt)
    china = len(china_list) * 20
    letter = (len(txt) - len(china_list)) * 10
    t_x = (WIDTH // 2) - (china // 2 + letter // 2)
    if t_x < 0: messagebox.showinfo('INFO', "长度过长")
    title.configure(text=txt)
    title.place(x=t_x, y=120)


# 清除赛事标题
def title_rm():
    text.delete(0, 'end')


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
                                           font=("行楷", int(WIDTH * 0.16), "bold", "italic"), fill="#e4e4dc")

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
    global lastDraw, px, length

    if what.get() == 1:
        lastDraw = canvas.create_line(X.get(), Y.get(), event.x, event.y,
                                      fill='#000000', width=font_size)
        x = event.x - X.get()
        y = event.y - Y.get()
        if x > 0 and y > 0:
            px += (math.sqrt(x * x + y * y)) / 10
        else:
            px += (abs(x + y)) / 10

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


# 铅笔
def pen():
    what.set(1)


# 橡皮擦
def remove():
    what.set(2)


# 清屏
def clear():
    global lastDraw, end, h1, h2, watermark, length, px
    for item in canvas.find_all():
        canvas.delete(item)
    wid = WIDTH / 10
    hei = HEIGHT / 10
    h1 = canvas.create_text(WIDTH - 40, 10, text=f"长：{wid}m")
    h2 = canvas.create_text(WIDTH - 40, 30, text=f"宽：{hei}m")

    canvas.create_text(35, 10, text="5m")
    canvas.create_line(10, 15, 10, 20)
    canvas.create_line(60, 15, 60, 20)
    canvas.create_line(10, 20, 60, 20)
    px = 0
    length.config(text="%.2fm" % px)

    if state_f:
        watermark = canvas.create_text(WIDTH / 2, HEIGHT / 2, text="山东体育学院",
                                       font=("行楷", int(WIDTH * 0.16), "bold", "italic"), fill="#e4e4dc")
    end = [0]
    lastDraw = 0


# 撤销
def back():
    global end
    try:
        for i in range(end[-2], end[-1] + 1):
            canvas.delete(i)
        end.pop()
    except:
        end = [0]
    # wid = WIDTH / 10
    # hei = HEIGHT / 10
    # h1 = canvas.create_text(WIDTH - 40, 10, text=f"长：{wid}m")
    # h2 = canvas.create_text(WIDTH - 40, 30, text=f"宽：{hei}m")
    #
    # canvas.create_text(30, 10, text="5m")
    # canvas.create_line(10, 15, 10, 20)
    # canvas.create_line(50, 15, 50, 20)
    # canvas.create_line(10, 20, 50, 20)


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


# 保存
def selectExcelfile():
    filename = tkinter.filedialog.asksaveasfilename(filetypes=[('.png', 'PNG')], initialfile="路线设计")
    var_path.delete(0, 'end')
    var_path.insert(tk.INSERT, filename)


# 保存
def preservation():
    path = var_path.get()
    if not path: return
    x1 = 5
    y1 = title.winfo_y() + 40
    if checkvar.get() == '1':
        x2 = f.winfo_x() + f.winfo_width() + frame_info.winfo_width() + 30
    elif checkvar.get() == '0':
        x2 = f.winfo_x() + f.winfo_width() + 10
    else:
        x2 = f.winfo_x() + f.winfo_width()
    y2 = f.winfo_y() + f.winfo_height() + 70
    try:
        ImageGrab.grab((x1, y1, x2, y2)).save(path)

        messagebox.showinfo("成功", "保存成功")
    except EOFError as e:
        print('Error saving image:', e)
    var_path.delete('0', 'end')


# 清除水印
def remove_f():
    global state_f
    canvas.delete(watermark)
    state_f = 0


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


# 帮助文档
def open_web():
    webbrowser.open("https://gitee.com")


# 障碍号
tk.Label(win, text="障碍号：", font=FONT).place(x=850, y=20)
var_id = tk.StringVar()
e_id = tk.Entry(win, textvariable=var_id)
e_id.place(x=930, y=20)

tk.Button(win, text='确认', command=insert).place(x=980, y=50)

tk.Button(win, text='单横木', command=monorail).place(x=1150, y=10)
tk.Button(win, text='双横木', command=oxer).place(x=1150, y=50)

tk.Label(win, text='A-->B:').place(x=1250, y=15)
var_a_b = tk.StringVar()
a_b = tk.Entry(win, textvariable=var_a_b, width=10)
a_b.place(x=1295, y=13)
tk.Label(win, text='B-->C:').place(x=1250, y=50)
var_b_c = tk.StringVar()
b_c = tk.Entry(win, textvariable=var_b_c, width=10)
b_c.place(x=1295, y=48)
tk.Button(win, text='组合障碍', command=combination).place(x=1300, y=80)

# 路线图信息主容器
frame_l_info = tk.Frame(win)
frame_l_info.place(x=10, y=10)

# 路线二级容器
frame_lable = tk.Frame(frame_l_info)
frame_input = tk.Frame(frame_l_info)
frame_button = tk.Frame(frame_l_info)
frame_lable.pack(side='left')
frame_button.pack(side='right')
frame_input.pack(side='right')

# 路线图长度
tk.Label(frame_lable, text="路线图长度(m):", font=FONT).pack()
var_l_w = tk.StringVar()
var_l_w.set('90')
var_l_w_inp = tk.Entry(frame_input, textvariable=var_l_w)
var_l_w_inp.pack()

# 路线图宽度
tk.Label(frame_lable, text="路线图宽度(m):", font=FONT).pack()
var_l_h = tk.StringVar()
var_l_h.set("60")
var_l_h_inp = tk.Entry(frame_input, textvariable=var_l_h)
var_l_h_inp.pack()
tk.Button(frame_button, text="确认", command=found).pack(padx=5, pady=5)

# 保存
tk.Label(win, text="保存:", font=FONT).place(x=10, y=70)
var_path = tk.Entry(win, bg='white', width=20)
var_path.place(x=60, y=70)
tk.Button(win, text='浏览', command=selectExcelfile).place(x=260, y=70)
bt = tk.Button(win, text="下载", command=preservation)
bt.place(x=330, y=70)
checkvar = tk.StringVar(value="0")
Checkbutton(win, text="包括右侧赛事信息", variable=checkvar, onvalue=1, offvalue=0).place(x=90, y=100)

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
                               font=("行楷", int(WIDTH * 0.16), "bold", "italic"), fill="#e4e4dc")

# 画图
canvas.bind('<Button-1>', leftButtonDown)  # 鼠标左键点击事件
canvas.bind('<B1-Motion>', leftButtonMove)  # 鼠标左键滚动事件
canvas.bind('<ButtonRelease-1>', leftButtonUp)  # 松开左键

# 标题
title = tk.Label(win, text="比赛名称", font=FONT)
title.place(x=350, y=120)

# 输入标题
tk.Label(win, text="比赛名:", font=FONT).place(x=410, y=20)
var_title = tk.StringVar()
text = tk.Entry(win, textvariable=var_title, width=35)
text.place(x=500, y=20)
tk.Button(win, text="确认", command=title_ok).place(x=550, y=50)
tk.Button(win, text="清除", command=title_rm).place(x=700, y=50)

# 信息
info = [
    '级别赛制', '比赛日期', '路线查看时间', '开赛时间', '判罚表', '障碍高度', '行进速度', '路线长度', '允许时间', '限制时间', '障碍数量', '跳跃数量', '附加赛', '路线设计师',
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
menu.add_cascade(label="工具栏", menu=menuType)
menuType.add_command(label="铅笔", command=pen)
menuType.add_command(label="橡皮擦", command=remove)
menuType.add_command(label="清屏", command=clear)
menuType.add_command(label="撤销", command=back)
menuType.add_command(label="清除水印", command=remove_f)

# 字号
font_menuType = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="字号", menu=font_menuType)
font_menuType.add_command(label="通用", command=currency_font)
font_menuType.add_command(label="铅笔", command=currency_pen)
font_menuType.add_command(label="橡皮擦", command=currency_remove)

# 障碍
obstacle = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="障碍", menu=obstacle)
obstacle.add_command(label="起/终点线", command=line)
obstacle.add_command(label="利物浦", command=live)
obstacle.add_command(label="砖墙", command=brick_wall)
obstacle.add_command(label="水障", command=water_barrier)
obstacle.add_command(label="进出口", command=gate)
obstacle.add_command(label="指北针", command=compass)
obstacle.add_command(label="强制通过点", command=force)

# 帮助
app_help = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="帮助", menu=app_help)
app_help.add_command(label="关于软件", command=about)
app_help.add_command(label="开发者信息", command=currency_font)
app_help.add_command(label="帮助文档", command=open_web)

win.config(menu=menu)

win.mainloop()
