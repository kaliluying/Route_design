import logging
import webbrowser
import subprocess
import tkinter.simpledialog
from tkinter import filedialog

# import numpy as np
import Common
from Common import set_len, get_len, get_cur, get_frame_stare, set_cur, set_line, state
from scale import CreateImg, CreateTxt, CreateParameter, T
from Tools import *

# from Common import *
import time

# 使用 state.xxx 访问全局状态，替代 global 声明


# 障碍号确认
def insert():
    var = var_id.get()
    CreateTxt(canvas, state.index_txt).create(var)
    state.index_txt += 1
    e_id.delete(0, "end")
    drag()


# 障碍参数确认
def parameter():
    var = var_parameter.get()
    CreateParameter(canvas, state.index_txt).create(var)
    state.index_txt += 1
    e_parameter.delete(0, "end")
    drag()


# 隐藏障碍参数
def hidden():
    if state.par_index:
        canvas.itemconfig("parameter", state="hidden")
        par_state.config(text="显示")
        state.par_index = 0
    else:
        canvas.itemconfig("parameter", state="normal")
        par_state.config(text="隐藏")
        state.par_index = 1


# 单横木
def monorail():
    image_path = expand(get_one_path())
    image_path = start_direction(image_path)
    CreateImg(canvas, state.index_img, image_path, obstacle="monorail").create()
    state.index_img += 1
    drag()


# 双横木
def oxer():
    image_path = merge(10)
    image_path = start_direction(image_path)
    CreateImg(canvas, state.index_img, image_path, obstacle="oxer").create()
    state.index_img += 1
    drag()


# 三横木
def tirail():
    image_path = merge(10, 10)
    index_img += 1
    CreateImg(canvas, index_img, image_path, obstacle="tirail").create()
    drag()


# AB组合障碍
def combination_ab():
    image_path = merge_ab(state=1, m1=30)
    CreateImg(canvas, state.index_img, image_path, obstacle="combination_ab").create()
    state.index_img += 1
    drag()


# ABC组合障碍
def combination_abc():
    image_path = merge_ab(state=1, m1=30, m2=30)
    CreateImg(canvas, state.index_img, image_path, obstacle="combination_abc").create()
    state.index_img += 1
    CreateImg(canvas, index_img, image_path, obstacle="combination_abc").create()
    drag()


# 利物浦
def live():
    image_path = live_one_tool()
    CreateImg(canvas, state.index_img, image_path, obstacle="live").create()
    state.index_img += 1
    drag()


# 强制通过点
def force():
    CreateImg(canvas, state.index_img, force_image).create()
    state.index_img += 1
    drag()


# 指北针
def compass():
    image_path = expand(compass_image)
    CreateImg(canvas, state.index_img, image_path).create()
    state.index_img += 1
    drag()


# 水障
def water_barrier():
    image_path = expand(water_barrier_iamge)
    image_path = start_direction(image_path)
    CreateImg(canvas, state.index_img, image_path, obstacle="water").create()
    state.index_img += 1
    drag()


# 砖墙
def brick_wall():
    image_path = expand(brick_wall_image)
    CreateImg(canvas, state.index_img, image_path).create()
    state.index_img += 1
    drag()


# 起/终点线
def line():
    image_path = expand(line_image)
    image_path = start_direction(image_path)
    CreateImg(canvas, state.index_img, image_path).create()
    state.index_img += 1
    drag()


# 进出口
def gate():
    image_path = expand(gate_image)
    CreateImg(canvas, state.index_img, image_path).create()
    state.index_img += 1
    drag()


# 圆
def circular():
    cir = int(var_cir.get()) * 10
    img = Image.open(circular_image)
    img = img.resize((cir, cir))
    img.save("./img/cir.png")
    cir_path = "./img/cir.png"
    CreateImg(canvas, state.index_img, cir_path).create()
    state.index_img += 1
    drag()


# 赛事信息确认
def dle():
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
                state.temp_txt = value.get()
                canvas.itemconfig("比赛名称", text=state.temp_txt)
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
        logging.warning("赛事信息确认: %s", e)
        messagebox.showerror("Error", "出错了")


# 修改赛事信息
def edit():
    temp_ = {}
    for i in range(len(info_var)):
        temp_[info[i]] = info_var[i].get()

    info_var.clear()
    pro_var.clear()
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


def allow(info_var, pro_value):
    try:
        s = info_var[7].get()
        l = info_var[8].get()
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
        logging.warning("赛事信息出错：%s", e)
        return False


# 生成路线图
def found():
    w = var_l_w.get()
    h = var_l_h.get()
    # if w.isdigit() and h.isdigit():
    state.WIDTH = int(float(w) * 10)
    state.HEIGHT = int(float(h) * 10)
    canvas.config(width=state.WIDTH + 30, height=state.HEIGHT + 70)
    canvas.coords("实际画布", 15, 50, state.WIDTH + 15, state.HEIGHT + 50)
    # canvas.place(x=175, y=130)
    but1.place(x=state.WIDTH + 260, y=700)
    but2.place(x=state.WIDTH + 360, y=700)
    frame_info.place(x=state.WIDTH + 200, y=150)
    canvas.delete(state.watermark)
    wid = state.WIDTH / 10
    hei = state.HEIGHT / 10
    canvas.itemconfig("长", text=f"长：{wid}m")
    canvas.itemconfig("宽", text=f"宽：{hei}m")
    canvas.coords("长", state.WIDTH - 40, 60)
    canvas.coords("宽", state.WIDTH - 40, 80)
    canvas.coords("实时路线", state.WIDTH - 40, 30)
    canvas.delete("bg")
    img = Image.open(fg_path)
    img = img.resize((WIDTH, HEIGHT))
    fg_img = ImageTk.PhotoImage(img)
    canvas.create_image(15, 50, image=fg_img, anchor="nw", tags=("不框选", "bg"))
    if state_f:
        font = 0.16 if sys_name == "Darwin" else 0.12
        watermark = canvas.create_text(
            WIDTH / 2,
            (HEIGHT + 20) / 2,
            text="山东体育学院",
            font=("行楷", int(WIDTH * font), "bold", "italic"),
            fill="#e4e4dc",
            tags=("watermark", "不框选"),
        )
        canvas.lower("watermark")
    # else:
    #     messagebox.showerror('错误', '请输入正整数')
    #     if w.isdigit():
    #         var_l_h_inp.delete(0, 'end')
    #     if h.isdigit():
    #         var_l_w_inp.delete(0, 'end')


# 鼠标左键按下
def leftButtonDown(event):
    if state.choice_tup and not (
        min(state.choice_tup[0], state.choice_tup[2]) < event.x < max(state.choice_tup[0], state.choice_tup[2])
        and min(state.choice_tup[1], state.choice_tup[3])
        < event.y
        < max(state.choice_tup[1], state.choice_tup[3])
    ):
        canvas.delete("choice")
        state.choice_tup.clear()
        canvas.dtag("choice_start", "choice_start")
    X.set(event.x)
    Y.set(event.y)
    move_x.set(event.x)
    move_y.set(event.y)


def create_line(x1, y1, x2, y2):
    id = canvas.create_line(x1, y1, x2, y2, tags=("line", "不框选"))
    # a = canvas.create_arc(x1, y1, x2, y2, start=135, extent=180, style='arc', tags='line')
    # canvas.create_rectangle(x1, y1, x2, y2, tags='line')
    return id


# 鼠标左键滚动事件
def leftButtonMove(event):
    shu(event)
    if what.get() == 1:
        state.lastDraw = canvas.create_line(
            X.get(),
            Y.get(),
            event.x,
            event.y,
            fill="#000000",
            width=font_size,
            tags=("line", "不框选"),
            smooth=True,
        )
        x1, y1, x2, y2 = canvas.coords(state.lastDraw)
        state.px += (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) / 10
        temp_px = (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) / 10
        state.remove_px[state.lastDraw] = temp_px
        canvas.itemconfig("实时路线", text="%.2fm" % state.px)
        X.set(event.x)
        Y.set(event.y)
        state.click_num = 1

    # 橡皮擦
    elif what.get() == 2:
        te = canvas.find_overlapping(
            event.x - 10, event.y - 10, event.x + 10, event.y + 10
        )
        for i in te:
            canvas.delete(i)

    # 多选框移动
    elif what.get() == 0 and state.choice_tup:
        if min(state.choice_tup[0], state.choice_tup[2]) < event.x < max(
            state.choice_tup[0], state.choice_tup[2]
        ) and min(state.choice_tup[1], state.choice_tup[3]) < event.y < max(
            state.choice_tup[1], state.choice_tup[3]
        ):
            bbox = canvas.bbox("choice")
            canvas.move("choice_start", event.x - X.get(), event.y - Y.get())
            X.set(event.x)
            Y.set(event.y)
            try:
                state.choice_tup.clear()
                state.choice_tup.extend(list(bbox))
            except TypeError as e:
                logging.warning("多选框移动出错: %s", e)
    else:
        if get_frame_stare():
            canvas.delete("choice")
            canvas.create_rectangle(
                X.get(), Y.get(), event.x, event.y, tags="choice", dash=(3, 5)
            )


# 松开左键
def leftButtonUp(event):
    state.end.append(state.lastDraw)
    state.current_frame_stare = get_frame_stare()
    if what.get() == 1:
        if state.click_num == 1:
            if move_x.get() != event.x or move_y.get() != event.y:
                id = state.remove_px.keys()
                total = sum(state.remove_px.values())
                state.route_click.append((start_x.get(), start_y.get()))
                state.stack.append(("长度测量", (id, total)))
                state.remove_px = {}
            start_x.set(event.x)
            start_y.set(event.y)
            state.click_num = 2
        elif state.click_num == 2:
            end_x.set(event.x)
            end_y.set(event.y)
            id = create_line(start_x.get(), start_y.get(), end_x.get(), end_y.get())
            x1, y1, x2, y2 = canvas.coords(id)
            distance = (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) / 10
            state.px += distance
            state.route_click.append((start_x.get(), start_y.get()))
            state.stack.append(("长度测量", ([id], distance)))
            canvas.itemconfig("实时路线", text="%.2fm" % state.px)
            start_x.set(end_x.get())
            start_y.set(end_y.get())
    elif what.get() == 4:
        if state.click_num == 1:
            start_x.set(event.x)
            start_y.set(event.y)
            state.click_num = 2
        elif state.click_num == 2:
            end_x.set(event.x)
            end_y.set(event.y)
            start_x.set(end_x.get())
            start_y.set(end_y.get())
    if state.current_frame_stare:
        canvas.addtag_overlapping("choice_start", X.get(), Y.get(), event.x, event.y)
        canvas.dtag("不框选", "choice_start")
        state.choice_tup.append(X.get())
        state.choice_tup.append(Y.get())
        state.choice_tup.append(event.x)
        state.choice_tup.append(event.y)
    else:
        set_frame_stare(True)
    if canvas.find_withtag("choice") and what.get() != "3":
        items = canvas.find_withtag("choice_start")
        state.stack.append(("移动", items, (event.x - move_x.get(), event.y - move_y.get())))


# def create_arc(x1, y1, x2, y2):
#     x = x1 - x2
#     y = y1 - y2
#     if x != 0 and y != 0:
#         r = (math.sqrt(x * x + y * y)) / 2
#     else:
#         r = (abs(x + y)) / 2
#
#     num_points = 300
#     x0 = (x1 + x2) / 2
#     y0 = (y1 + y2) / 2
#
#     # 生成圆上的点的极角
#     theta = np.linspace(0, 2 * np.pi, num_points)
#
#     # 计算每个极角对应的 x, y 坐标
#     x = x0 + r * np.cos(theta)
#     y = y0 + r * np.sin(theta)
#
#     x = list(map(int, x))
#     y = list(map(int, y))
#
#     index = 0
#     while len(x) >= index:
#         canvas.create_line(x[index], y[index], x[index + 1], y[index + 1], tags='line')
#         index += 10


# 拖动
def drag():
    what.set(0)
    set_color()
    no_what.set(0)


# 铅笔
def pen():
    what.set(1)
    set_color()
    no_what.set(1)
    state.click_num = 1


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


def set_color():
    id = what.get()
    no_id = no_what.get()
    if id == 0:
        but_0.config(fg="red")
    elif id == 1:
        but_1.config(fg="red")
    # elif id == 2:
    #     but_2.config(fg='red')
    elif id == 3:
        but_3.config(fg="red")
    # elif id == 4:
    #     but_4.config(fg='red')

    if id != no_id:
        if no_id == 0:
            but_0.config(fg="black")
        elif no_id == 1:
            but_1.config(fg="black")
        # elif no_id == 2:
        #     but_2.config(fg='black')
        elif no_id == 3:
            but_3.config(fg="black")
        # elif no_id == 4:
        #     but_4.config(fg='black')


# 清屏
def clear():
    canvas.delete("line")
    canvas.delete("rubber")
    state.px = 0
    canvas.itemconfig("实时路线", text="%.2fm" % state.px)
    state.click_num = 1
    to_be_deleted = []
    for i in range(len(state.stack)):
        if state.stack[i][0] == "长度测量":
            to_be_deleted.append(i)
    for idx in reversed(to_be_deleted):
        state.stack.pop(idx)


# 撤销
def back():
    temp = 0
    temp_dict = {}
    iteration = state.remove_px.keys()
    for i in range(state.end[-2] + 1, state.end[-1] + 1):
        if next(iter(state.remove_px)) > i:
            continue
        canvas.delete(i)
    for i in iteration:
        if i > state.end[-2]:
            temp += state.remove_px[i]
            temp_dict[i] = state.remove_px[i]
    for i in temp_dict.keys():
        if i in state.remove_px:
            del state.remove_px[i]
    state.end.pop()
    state.px -= temp

    canvas.itemconfig("实时路线", text="%.2fm" % state.px)


# 通用字号
def currency_font():
    state.size = tkinter.simpledialog.askinteger("输入字号", prompt="", initialvalue=state.size)
    state.font_size = state.remove_size = state.size


# 铅笔字号
def currency_pen():
    state.font_size = tkinter.simpledialog.askinteger(
        "输入字号", prompt="", initialvalue=state.font_size
    )


# 橡皮擦字号
def currency_remove():
    state.remove_size = tkinter.simpledialog.askinteger(
        "输入字号", prompt="", initialvalue=state.remove_size
    )


def save_1():
    checkvar = "1"
    save(checkvar)


def save_0():
    checkvar = "0"
    save(checkvar)


# 保存
def save(checkvar):
    current_time = time.strftime("%Y%m%d-%H%M%S")
    txt = state.temp_txt if state.temp_txt else "路线设计_" + current_time
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

        # Win
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
            # os.system(cmd)
            # subprocess.call(cmd)
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


# 打开文件保存路径
def open_file():
    if not os.path.exists("./ms_download"):
        os.mkdir("./ms_download")
    path = os.getcwd() + f"/ms_download"
    if sys_name == "Windows":
        subprocess.Popen(["explorer", path])
    else:
        subprocess.call(["open", path])


# 置底
def set_state():
    cur, line = get_cur()
    canvas.lower(cur)
    canvas.lower("watermark")


# 删除
def pop(id=None):
    if id:
        cur, line = get_cur()
        canvas.delete(id)
        if id == cur:
            remove_from_not_com()
        return
    items = canvas.find_withtag("choice_start")[:-1]
    if items:
        canvas.itemconfig("choice_start", state="hidden")
        choice_tup.clear()
        stack.append(("删除", items))
    else:
        cur, line = get_cur()
        canvas.itemconfig(cur, state="hidden")
        canvas.itemconfig(line, state="hidden")
        stack.append(("删除", (cur, line)))

    remove_from_not_com()


# 网格辅助线
def grid():
    if state.grid_start:
        canvas.itemconfig("grid", stat="hidden")
        state.grid_start = 0
    elif state.create_grid and not state.grid_start:
        canvas.itemconfig("grid", stat="normal")
        state.grid_start = 1

    if not state.create_grid:
        range_x = (WIDTH + 30) // 100
        range_y = (HEIGHT + 70) // 100
        index_x = 15
        index_y = 50
        for i in range(range_x):
            canvas.create_line(
                index_x, 50, index_x, HEIGHT + 50, dash=(5, 3), tags=("grid", "不框选")
            )
            index_x += 100
        for i in range(range_y):
            canvas.create_line(
                15, index_y, WIDTH + 15, index_y, dash=(5, 3), tags=("grid", "不框选")
            )
            index_y += 100
        state.create_grid = True
        state.grid_start = 1


def info():
    if state.aux_stare:
        canvas.itemconfig("辅助信息", stat="hidden")
        aux_info.config(text="显示辅助信息")
        state.aux_stare = False
    else:
        canvas.itemconfig("辅助信息", stat="normal")
        aux_info.config(text="隐藏辅助信息")
        state.aux_stare = True


# 清除水印
def remove_f():
    canvas.delete(state.watermark)
    state.state_f = 0


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
    tk.Label(
        app_frame, text="Copyright © 2022 山东体育学院.\nAll rights reserved."
    ).pack()
    tk.Label(app_frame, text="软件开发：许志亮 葛茂林").pack()


# 帮助文档
def open_web():
    webbrowser.open("https://gitee.com/gmlwb/ms/blob/master/README.md")


# 自定义障碍
def custom():
    img_path = filedialog.askopenfilename(
        title="选择Excel文件", filetypes=[("image", "*.jpg"), ("image", "*.png")]
    )
    CreateImg(canvas, state.index_img, img_path).create()
    state.index_img += 1
    drag()


# 设置背景图
def fg():
    state.fg_path = filedialog.askopenfilename(
        title="选择Excel文件", filetypes=[("image", "*.jpg"), ("image", "*.png")]
    )
    img = Image.open(state.fg_path)
    img = img.resize((WIDTH, HEIGHT))
    state.fg_img = ImageTk.PhotoImage(img)
    canvas.create_image(15, 50, image=state.fg_img, anchor="nw", tags=("不框选", "bg"))


# 删除背景图
def del_fg():
    canvas.delete("bg")


# 障碍物
tk.Button(frame_temp_1, text="进出口", command=gate).pack()
tk.Button(frame_temp_1, text="指北针", command=compass).pack()
#
tk.Button(frame_temp_2, text="水障", command=water_barrier).pack()
tk.Button(frame_temp_2, text="砖墙", command=brick_wall).pack()
#
tk.Button(frame_temp_3, text="起/终点线", command=line).pack()
tk.Button(frame_temp_3, text="强制通过点", command=force).pack()

tk.Button(frame_temp_4, text="利物浦", command=live).pack()
tk.Button(frame_temp_4, text="单横木", command=monorail).pack()

tk.Button(frame_temp_5, text="双横木", command=oxer).pack()
tk.Button(frame_temp_5, text="三横木", command=tirail).pack()

tk.Button(frame_temp_6, text="AB组合障碍", command=combination_ab).pack()
tk.Button(frame_temp_6, text="ABC组合障碍", command=combination_abc).pack()

tk.Button(frame_temp_7, text="自定义障碍", command=custom).pack()
tk.Button(frame_temp_7, text="导入背景图", command=fg).pack()

if sys_name == "Darwin":
    width = 5
elif sys_name == "Windows":
    width = 10
# 工作模块
but_0 = tk.Button(
    frame_command_left, text="拖动", command=drag, fg="red", width=width, height=1
)
but_0.pack()
but_3 = tk.Button(
    frame_command_left, text="旋转", command=rotate, width=width, height=1
)
but_3.pack()

# but_4 = tk.Button(frame_command_left, text='画弧', command=arc, width=width, height=1)
# but_4.pack()
# but_2 = tk.Button(frame_command_left, text='橡皮', command=remove, width=width, height=1)
# but_2.pack()
tk.Button(frame_mea_com_rig, text="清屏", command=clear, width=width, height=1).pack()
# tk.Button(frame_command_right, text='撤销', command=back, width=width, height=1).pack()
tk.Button(
    frame_command_right, text="置底", command=set_state, width=width, height=1
).pack()
tk.Button(frame_command_right, text="删除", command=pop, width=width, height=1).pack()

# 辅助模块
tk.Button(
    frame_aux_com_lef, text="网格辅助线", command=grid, width=width, height=1
).pack()
aux_info = tk.Button(
    frame_aux_com_rig, text="隐藏辅助信息", command=info, width=width, height=1
)
aux_info.pack()

# 障碍参数
tk.Label(frame_aux_tit, text="障碍备注：", font=FONT).pack(pady=5)
var_parameter = tk.StringVar()
e_parameter = Entry(frame_aux_inp, textvariable=var_parameter, width=8)
e_parameter.pack(pady=5)

tk.Button(frame_aux_tit, text="确认", command=parameter).pack()
par_state = tk.Button(frame_aux_inp, text="隐藏", command=hidden)
par_state.pack()

# 圆
tk.Label(frame_aux_tit2, text="圆(m)：", font=FONT).pack()
var_cir = tk.StringVar()
e_id = Entry(frame_aux_inp2, textvariable=var_cir, width=3)
e_id.pack()

tk.Button(frame_aux_but, text="确认", command=circular).pack()

# 测量模块
but_1 = tk.Button(
    frame_mea_com_lef, text="长度测量", command=pen, width=width, height=1
)
but_1.pack()

# 障碍号
tk.Label(frame_temp_9, text="障碍号：", font=FONT).pack(side="left")
var_id = tk.StringVar()
e_id = Entry(frame_temp_9, textvariable=var_id, width=4)
e_id.pack(side="left")

tk.Button(frame_temp_8, text="确认", command=insert).pack(padx=1)

tk.Label(win, text="全局障碍长度(m):", font=FONT).place(x=200, y=10)
var_len = tk.StringVar(value="4")
len_entt = Entry(win, textvariable=var_len, width=4)
len_entt.place(x=330, y=10)

tk.Button(win, text="确认", command=partial(set_len, var_len)).place(x=300, y=40)

tk.Button(win, text="清除水印", command=remove_f).place(x=180, y=40)

# 路线图长度
tk.Label(win, text="长度(m):", font=FONT).place(x=10, y=10)
var_l_w = tk.StringVar()
var_l_w.set("90")
var_l_w_inp = Entry(win, textvariable=var_l_w, width=5)
var_l_w_inp.place(x=80, y=10)

# 路线图宽度
tk.Label(win, text="宽度(m):", font=FONT).place(x=10, y=40)
var_l_h = tk.StringVar()
var_l_h.set("60")
var_l_h_inp = Entry(win, textvariable=var_l_h, width=5)
var_l_h_inp.place(x=80, y=40)

tk.Button(win, text="确认", command=found).place(x=50, y=70)

canvas.create_rectangle(
    15, 50, WIDTH + 15, HEIGHT + 50, state="disabled", tags=("不框选", "实际画布")
)

# 右上角显示路线长宽
w = WIDTH / 10
h = HEIGHT / 10
h1 = canvas.create_text(
    WIDTH - 40, 60, text=f"长：{w}m", tags=("辅助信息", "不框选", "长")
)
h2 = canvas.create_text(
    WIDTH - 40, 80, text=f"宽：{h}m", tags=("辅助信息", "不框选", "宽")
)

# 左上角显示 5m的距离
canvas.create_text(45, 60, text="5m", tags=("辅助信息", "不框选"))
canvas.create_line(20, 65, 20, 70, tags=("辅助信息", "不框选"))
canvas.create_line(70, 65, 70, 70, tags=("辅助信息", "不框选"))
canvas.create_line(20, 70, 70, 70, tags=("辅助信息", "不框选"))

# 右上显示，路线长度
canvas.create_text(
    WIDTH - 40, 30, text=f"{state.px / 10}m", tags=("实时路线", "不框选", "辅助信息")
)


# 鼠标实时坐标
def shu(event):
    x = event.x / 10 - 1.5
    y = event.y / 10 - 5
    canvas.itemconfig("鼠标x", text=f"x:{x:.2f}")
    canvas.itemconfig("鼠标y", text=f"y:{y:.2f}")


# 右下角显示鼠标实时坐标
canvas.create_text(
    WIDTH - 10, HEIGHT + 60, text="x:", tags=("辅助信息", "不框选", "鼠标x")
)
canvas.create_text(
    WIDTH - 10, HEIGHT + 70, text="y:", tags=("辅助信息", "不框选", "鼠标y")
)

canvas.bind("<Motion>", shu)

# 左下显示当前障碍坐标
canvas.create_text(20, HEIGHT + 60, text=f"x:", tags=("辅助信息", "不框选", "障碍x"))
canvas.create_text(20, HEIGHT + 70, text=f"y:", tags=("辅助信息", "不框选", "障碍y"))

# 水印
font = 0.16 if sys_name == "Darwin" else 0.12
watermark = canvas.create_text(
    WIDTH / 2,
    (HEIGHT + 20) / 2,
    text="山东体育学院",
    font=("行楷", int(WIDTH * font), "bold", "italic"),
    fill="#e4e4dc",
    tags=("watermark", "不框选"),
    state="disabled",
)

# 画图
canvas.bind("<Button-1>", leftButtonDown)  # 鼠标左键点击事件
canvas.bind("<B1-Motion>", leftButtonMove)  # 鼠标左键移动事件
canvas.bind("<ButtonRelease-1>", leftButtonUp)  # 松开左键

# 标题
canvas.create_text(
    (WIDTH + 40) / 2,
    20,
    text="比赛名称",
    font=("微软雅黑", 18),
    tags=("比赛名称", "不框选"),
)

# 信息
info = [
    "比赛名称",
    "级别赛制",
    "比赛日期",
    "路线查看时间",
    "开赛时间",
    "判罚表",
    "障碍高度",
    "行进速度",
    "路线长度",
    "允许时间",
    "限制时间",
    "障碍数量",
    "跳跃数量",
    "附加赛",
    "路线设计师",
]

# 赛事信息主容器
frame_info = tk.Frame(win)
# 放赛事信息标题
frame_tit = tk.Frame(frame_info)
# 放赛事信息输入框
frame_inp = tk.Frame(frame_info)
# 建议信息容器
frame_por = tk.Frame(frame_info)

frame_info.place(x=WIDTH + 200, y=150)
frame_tit.pack(side="left")
frame_por.pack(side="right")
frame_inp.pack(side="right")

# 生成赛事信息
info_var = []
pro_var = []
edit()

but1 = tk.Button(win, text="确认", command=dle)
but1.place(x=WIDTH + 260, y=700)
but2 = tk.Button(win, text="修改", command=edit)
but2.place(x=WIDTH + 360, y=700)

# 菜单栏
menu = tk.Menu(win)

# 工具栏
menuType = tk.Menu(menu, tearoff=0)
# menu_sava = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="工具栏", menu=menuType)
menuType.add_radiobutton(label="指针拖动", command=drag, variable=what, value=0)
menuType.add_radiobutton(label="旋转", command=rotate, variable=what, value=3)
menuType.add_radiobutton(label="长度测量", command=pen, variable=what, value=1)
# menuType.add_radiobutton(label="橡皮擦", command=remove, variable=what, value=2)

# 功能
function_menuType = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="功能", menu=function_menuType)
function_menuType.add_command(label="清屏", command=clear)
# function_menuType.add_command(label="撤销", command=back)
function_menuType.add_command(label="清除水印", command=remove_f)
function_menuType.add_command(label="打开文件下载位置", command=open_file)
function_menuType.add_command(label="下载", command=save_1)

# def save():
#     with open('ms.pkl', 'wb') as f:
#         for i in T.all_instances:
#             print(i.__dict__)
#             dill.dump(i.__dict__, f)

# dill.dump_session('ms.pkl')


# function_menuType.add_command(label="保存", command=save)


# def load():
#     with open('ms.pkl', 'rb') as f:
#         circle_data = dill.load(f)
#         circle = T(**circle_data)
#         circle.create()
# dill.load_session('ms.pkl')


# function_menuType.add_command(label="加载", command=load)
function_menuType.add_command(label="删除背景", command=del_fg)

# menu_sava.add_command(label="保存(包含右侧赛事信息)", command=save_1)
# menu_sava.add_command(label="保存(不包含右侧赛事信息)", command=save_0)

# function_menuType.add_cascade(label="保存", menu=menu_sava)

# 字号
font_menuType = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="字号", menu=font_menuType)
# font_menuType.add_command(label="通用", command=currency_font)
font_menuType.add_command(label="长度测量", command=currency_pen)
# font_menuType.add_command(label="橡皮擦", command=currency_remove)

# 帮助
app_help = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="帮助", menu=app_help)
app_help.add_command(label="关于软件", command=about)
app_help.add_command(label="帮助文档", command=open_web)

win.config(menu=menu)


# 撤销
def undo(event):
    if state.stack and event.widget == win:
        item = state.stack.pop()
        if item[0] == "创建":
            pop(id=item[1])
        elif item[0] == "移动":
            for i in item[1]:
                canvas.move(i, -item[2][0], -item[2][1])
        elif item[0] == "删除":
            for i in item[1]:
                canvas.itemconfig(i, state="normal")
        elif item[0] == "长度测量":
            id, temp_px = item[1]
            for i in id:
                pop(i)
            state.px -= temp_px
            canvas.itemconfig("实时路线", text="%.2fm" % state.px)
            x, y = state.route_click.pop()
            start_x.set(x)
            start_y.set(y)
        elif item[0] == "旋转":
            obj = item[1]
            state.rotate_.pop()
            obj.rotate(obj.id, state.rotate_[-1])


# 绑定ctrl+z兼容Mac和win
win.bind("<Command-KeyPress-z>", undo)
win.bind("<Control-KeyPress-z>", undo)


def get_all_widgets(root):
    widgets = []
    for widget in root.winfo_children():
        widgets.append(widget)
        widgets.extend(get_all_widgets(widget))
    return widgets


def save():
    widgets = get_all_widgets(win)
    # print(widgets)
    win.destroy()


def unfocus_click(event):
    if "ent" not in str(event.widget):
        win.focus_set()


def delete(event):
    if "ent" not in str(event.widget):
        pop()


win.bind("<Button-1>", unfocus_click)
win.bind("<BackSpace>", delete)
# win.protocol("WM_DELETE_WINDOW", save)

# 初始化 Focus（延迟导入避免循环依赖）
from focus import Focus
focus = Focus(win)

win.mainloop()
