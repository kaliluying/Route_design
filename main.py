import subprocess
import time
import tkinter.simpledialog
import webbrowser
from tkinter import filedialog
from Common import *
from functools import partial

from Tools import *
from scale import CreateImg, CreateTxt, CreateParameter, T


# 障碍号确认
def insert():
    global index_txt
    var = var_id.get()
    index_txt += 1
    CreateTxt(canvas, index_txt).create(var)
    e_id.delete(0, 'end')
    drag()


# 障碍备注
def parameter():
    global index_txt
    var = var_parameter.get()
    index_txt += 1
    CreateParameter(canvas, index_txt).create(var)
    e_parameter.delete(0, 'end')
    drag()


# 隐藏障碍参数
def hidden():
    global par_index
    if par_index:
        canvas.itemconfig('parameter', state='hidden')
        par_state.config(text='显示')
        par_index = 0
    else:
        canvas.itemconfig('parameter', state='normal')
        par_state.config(text='隐藏')
        par_index = 1


# 单横木
def monorail():
    global index_img
    image_path = expand(get_one_path())
    image_path = start_direction(image_path)
    index_img += 1
    CreateImg(canvas, index_img, image_path, obstacle='monorail').create()
    drag()


# 双横木
def oxer():
    global index_img
    image_path = merge(10)
    image_path = start_direction(image_path)
    index_img += 1
    CreateImg(canvas, index_img, image_path, obstacle='oxer').create()
    drag()


# 三横木
def tirail():
    global index_img
    image_path = merge(10, oxer='tirail')
    index_img += 1
    CreateImg(canvas, index_img, image_path, obstacle='tirail').create()
    drag()


def four():
    """
    四横木
    :return:
    """
    global index_img
    image_path = merge(15, oxer='four')
    index_img += 1
    CreateImg(canvas, index_img, image_path, obstacle='four').create()
    drag()


# AB组合障碍
def combination_ab():
    global index_img
    image_path = merge_ab(state=1, m1=30)
    index_img += 1
    CreateImg(canvas, index_img, image_path, obstacle="combination_ab").create()
    drag()


# ABC组合障碍
def combination_abc():
    global index_img
    image_path = merge_ab(state=1, m1=30, m2=30)
    index_img += 1
    CreateImg(canvas, index_img, image_path, obstacle="combination_abc").create()
    drag()


# 利物浦
def live():
    global index_img
    index_img += 1
    # image_path = expand(get_live_path())
    image_path = live_one_tool()
    CreateImg(canvas, index_img, image_path, obstacle='live').create()
    drag()


# 强制通过点
def force():
    global index_img
    index_img += 1
    CreateImg(canvas, index_img, force_image).create()
    drag()


# 指北针
def compass():
    global index_img
    index_img += 1
    image_path = expand(compass_image)
    CreateImg(canvas, index_img, image_path).create()
    drag()


# 水障
def water_barrier():
    global index_img
    index_img += 1
    image_path = expand(water_barrier_iamge)
    image_path = start_direction(image_path)
    CreateImg(canvas, index_img, image_path, obstacle='water').create()
    drag()


# 砖墙
def brick_wall():
    global index_img
    index_img += 1
    image_path = expand(brick_wall_image)
    CreateImg(canvas, index_img, image_path).create()
    drag()


# 起/终点线
def line():
    global index_img
    index_img += 1
    image_path = expand(line_image)
    image_path = start_direction(image_path)
    CreateImg(canvas, index_img, image_path).create()
    drag()


# 进出口
def gate():
    global index_img
    index_img += 1
    image_path = expand(gate_image)
    CreateImg(canvas, index_img, image_path).create()
    drag()


# 圆
def circular():
    global index_img
    index_img += 1
    cir = int(var_cir.get()) * 10
    img = Image.open(circular_image)
    img = img.resize((cir, cir))
    img.save('./img/cir.png')
    cir_path = './img/cir.png'
    CreateImg(canvas, index_img, cir_path).create()
    drag()


# 赛事信息确认
def dle():
    global temp_txt, entry_list, label_list
    try:
        data_dict = {'比赛名称': '', '级别赛制': '', '比赛日期': '', '路线查看时间': '', '开赛时间': '', '判罚表': '',
                     '障碍高度': '', '行进速度': '', '路线长度': '', '允许时间': '', '限制时间': '', '障碍数量': '',
                     '跳跃数量': '',
                     '附加赛': '', '路线设计师': ''}
        for entry, label, title in zip(entry_list, label_list, data_dict):
            text = entry.get().strip()
            data_dict[title] = text
        entry_list.clear()
        label_list.clear()
        # 将不为空的键值对取出
        filtered_dict = {key: value for key, value in data_dict.items() if value}

        for i in frame_info.winfo_children():
            i.destroy()

        for i, title in enumerate(filtered_dict):
            if title == '比赛名称':
                temp_txt = data_dict.get(title, "")
                canvas.itemconfig('比赛名称', text=temp_txt)
                continue
            title_label = ttk.Label(frame_info, text=title + ":")
            title_label.grid(row=i, column=0, sticky="e", padx=5, pady=5)

            label = ttk.Label(frame_info, text=filtered_dict.get(title, ""))
            label.grid(row=i, column=1, sticky="w", padx=5, pady=5)
            label_list.append(label)

        confirm_button = ttk.Button(frame_info, text="修改", command=partial(edit, filtered_dict),
                                    bootstyle="success-outline")
        confirm_button.grid(row=len(filtered_dict), column=1, sticky="n", padx=5, pady=5)

    except Exception as e:
        print("Error: " + str(e))
        messagebox.showerror("Error", "出错了")
        logging.warning("赛事信息确认", e)


def edit(current_dist=None):
    global entry_list, label_list
    data_dict = {'比赛名称': '', '级别赛制': '', '比赛日期': '', '路线查看时间': '', '开赛时间': '', '判罚表': '',
                 '障碍高度': '', '行进速度': '', '路线长度': '', '允许时间': '', '限制时间': '', '障碍数量': '',
                 '跳跃数量': '',
                 '附加赛': '', '路线设计师': ''}

    try:
        data_dict.update(current_dist)
    except TypeError:
        pass
    entry_list.clear()
    label_list.clear()
    for i in frame_info.winfo_children():
        i.destroy()

    for i, title in enumerate(data_dict):
        title_label = ttk.Label(frame_info, text=title + ":")
        title_label.grid(row=i, column=0, sticky="e", padx=5, pady=5)

        label = ttk.Label(frame_info, text=data_dict.get(title, ""))
        label.grid(row=i, column=1, sticky="w", padx=5, pady=5)
        label_list.append(label)

        entry = ttk.Entry(frame_info)
        entry.grid(row=i, column=1, sticky="w", padx=5, pady=5)
        entry.insert(0, data_dict.get(title, ""))
        entry_list.append(entry)
    confirm_button = ttk.Button(frame_info, text="确认", command=dle, bootstyle=CONFIRM_STYLE)
    confirm_button.grid(row=len(data_dict), column=1, sticky="n", padx=5, pady=5)


def allow(info_var, pro_value):
    try:
        s = info_var[7].get()
        l = info_var[8].get()
        if s.isdigit():
            s = float(s)
        else:
            s = float(s.split('/')[0][:-1])
        if l.isdigit():
            l = float(l)
        else:
            l = float(l.split('m')[0])
        t = s / l * 60
        pro_value.set('%.2fs' % t)
        return True
    except Exception as e:
        print('赛事信息出错：', e)
        logging.warning('赛事信息出错：', e)
        return False


# 生成路线图
def found():
    global WIDTH, HEIGHT, h1, h2, watermark, fg_img, fg_path
    w = var_l_w.get()
    h = var_l_h.get()
    # if w.isdigit() and h.isdigit():
    WIDTH = int(float(w) * 10)
    HEIGHT = int(float(h) * 10)
    canvas.config(width=WIDTH + 30, height=HEIGHT + 80)
    canvas.coords('实际画布', 15, 50, WIDTH + 15, HEIGHT + 50)
    # canvas.place(x=175, y=130)
    # but1.place(x=WIDTH + 260, y=700)
    # but2.place(x=WIDTH + 360, y=700)
    frame_info.place(x=WIDTH + 200, y=150)
    canvas.delete(watermark)
    wid = WIDTH / 10
    hei = HEIGHT / 10
    canvas.itemconfig('长', text=f"长：{wid}m")
    canvas.itemconfig('宽', text=f"宽：{hei}m")
    canvas.coords('长', WIDTH - 40, 60)
    canvas.coords('宽', WIDTH - 40, 80)
    canvas.coords('实时路线', WIDTH - 40, 30)
    canvas.coords('障碍x', 20, HEIGHT + 60)
    canvas.coords('障碍y', 20, HEIGHT + 70)
    canvas.coords('鼠标x', WIDTH - 10, HEIGHT + 60)
    canvas.coords('鼠标y', WIDTH - 10, HEIGHT + 70)
    canvas.delete('bg')
    img = Image.open(fg_path)
    img = img.resize((WIDTH, HEIGHT))
    fg_img = ImageTk.PhotoImage(img)
    canvas.create_image(15, 50, image=fg_img, anchor='nw', tags=('不框选', 'bg'))
    if state_f:
        font = 0.16 if sys_name == 'Darwin' else 0.12
        watermark = canvas.create_text(WIDTH / 2, (HEIGHT + 20) / 2, text="山东体育学院",
                                       font=("行楷", int(WIDTH * font), "bold", "italic"), fill="#e4e4dc",
                                       tags=("watermark", '不框选'))
        canvas.lower("watermark")
    # else:
    #     messagebox.showerror('错误', '请输入正整数')
    #     if w.isdigit():
    #         var_l_h_inp.delete(0, 'end')
    #     if h.isdigit():
    #         var_l_w_inp.delete(0, 'end')


# 鼠标左键按下
def leftButtonDown(event):
    global choice_tup
    if choice_tup and not (min(choice_tup[0], choice_tup[2]) < event.x < max(choice_tup[0], choice_tup[2])
                           and min(choice_tup[1], choice_tup[3]) < event.y < max(choice_tup[1], choice_tup[3])):
        canvas.delete('choice')
        choice_tup.clear()
        canvas.dtag('choice_start', 'choice_start')
    X.set(event.x)
    Y.set(event.y)
    move_x.set(event.x)
    move_y.set(event.y)


def create_line(x1, y1, x2, y2):
    id = canvas.create_line(x1, y1, x2, y2, tags=("line", '不框选'))
    # a = canvas.create_arc(x1, y1, x2, y2, start=135, extent=180, style='arc', tags='line')
    # canvas.create_rectangle(x1, y1, x2, y2, tags='line')
    return id


# 鼠标左键滚动事件
def leftButtonMove(event):
    global lastDraw, px, remove_px, click_num, choice_tup, current_frame_stare
    shu(event)
    # 画线
    if what.get() == 1:
        lastDraw = canvas.create_line(X.get(), Y.get(), event.x, event.y,
                                      fill='#000000', width=font_size, tags=("line", '不框选'), smooth=True)
        x1, y1, x2, y2 = canvas.coords(lastDraw)
        px += (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) / 10
        temp_px = (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) / 10
        # x = abs(event.x - X.get())
        # y = abs(event.y - Y.get())
        # if x != 0 and y != 0:
        #     px += (math.sqrt(x * x + y * y)) / 10
        #     temp_px = (math.sqrt(x * x + y * y)) / 10
        # else:
        #     px += (abs(x + y)) / 10
        #     temp_px = (abs(x + y)) / 10
        remove_px[lastDraw] = temp_px
        canvas.itemconfig('实时路线', text="%.2fm" % px)
        X.set(event.x)
        Y.set(event.y)
        click_num = 1

    # 橡皮擦
    elif what.get() == 2:
        te = canvas.find_overlapping(event.x - 10, event.y - 10, event.x + 10, event.y + 10)
        for i in te:
            canvas.delete(i)

    # 多选框移动
    elif what.get() == 0 and choice_tup:
        if min(choice_tup[0], choice_tup[2]) < event.x < max(choice_tup[0], choice_tup[2]) \
                and min(choice_tup[1], choice_tup[3]) < event.y < max(choice_tup[1], choice_tup[3]):
            bbox = canvas.bbox('choice')
            canvas.move('choice_start', event.x - X.get(), event.y - Y.get())
            X.set(event.x)
            Y.set(event.y)
            try:
                choice_tup.clear()
                choice_tup.extend(list(bbox))
            except TypeError as e:
                print('多选框移动出错', e)
                logging.warning('多选框移动出错', e)
    else:
        if get_frame_stare():
            canvas.delete('choice')
            canvas.create_rectangle(X.get(), Y.get(), event.x, event.y, tags='choice', dash=(3, 5))
            # current_frame_stare = True


# 松开左键
def leftButtonUp(event):
    global lastDraw, click_num, px, choice_tup, choice_start, remove_px
    end.append(lastDraw)
    current_frame_stare = get_frame_stare()
    # 画线
    if what.get() == 1:
        if click_num == 1:
            if move_x.get() != event.x or move_y.get() != event.y:
                id = remove_px.keys()
                total = sum(remove_px.values())
                route_click.append((start_x.get(), start_y.get()))
                stack.append(('长度测量', (id, total)))
                remove_px = {}
            start_x.set(event.x)
            start_y.set(event.y)
            click_num = 2
        elif click_num == 2:
            end_x.set(event.x)
            end_y.set(event.y)
            # click_num = 1
            id = create_line(start_x.get(), start_y.get(), end_x.get(), end_y.get())

            # x = abs(end_x.get() - start_x.get())
            # y = abs(end_y.get() - start_y.get())
            # temp_px = (abs(x + y)) / 10
            x1, y1, x2, y2 = canvas.coords(id)
            distance = (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) / 10
            px += distance
            route_click.append((start_x.get(), start_y.get()))
            stack.append(('长度测量', ([id], distance)))
            canvas.itemconfig('实时路线', text="%.2fm" % px)
            # remove_px[lastDraw] = px
            start_x.set(end_x.get())
            start_y.set(end_y.get())
    # 画弧
    elif what.get() == 4:
        if click_num == 1:
            start_x.set(event.x)
            start_y.set(event.y)
            click_num = 2
        elif click_num == 2:
            end_x.set(event.x)
            end_y.set(event.y)
            # create_arc(start_x.get(), start_y.get(), end_x.get(), end_y.get())
            start_x.set(end_x.get())
            start_y.set(end_y.get())
    if current_frame_stare:
        canvas.addtag_overlapping('choice_start', X.get(), Y.get(), event.x, event.y)
        canvas.dtag('不框选', 'choice_start')
        choice_tup.append(X.get())
        choice_tup.append(Y.get())
        choice_tup.append(event.x)
        choice_tup.append(event.y)
    else:
        set_frame_stare(True)
    if canvas.find_withtag('choice') and what.get() != '3':
        # TODO
        items = canvas.find_withtag('choice_start')
        stack.append(('移动', items, (event.x - move_x.get(), event.y - move_y.get())))
    if len(canvas.find_withtag('choice_start')) == 1:
        canvas.delete('choice')


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
    """
    拖动
    :return:
    """
    what.set(0)
    set_color()
    no_what.set(0)


def pen():
    """
    铅笔
    :return:
    """
    global click_num
    what.set(1)
    set_color()
    no_what.set(1)
    click_num = 1


def remove():
    """
    橡皮擦
    :return:
    """
    what.set(2)
    set_color()
    no_what.set(2)


def rotate():
    """
    旋转
    :return:
    """
    what.set(3)
    set_color()
    no_what.set(3)


def arc():
    """
    画弧
    :return:
    """
    what.set(4)
    set_color()
    no_what.set(4)


def set_color():
    id = what.get()
    no_id = no_what.get()
    if id == 0:
        # 拖动
        but_3.state(['!selected'])
        but_1.state(['!selected'])
    elif id == 1:
        # 铅笔
        but_3.state(['!selected'])
        but_0.state(['!selected'])
    # elif id == 2:
    #     but_2.config(fg='red')
    elif id == 3:
        # 旋转
        but_0.state(['!selected'])
        but_1.state(['!selected'])
    # elif id == 4:
    #     but_4.config(fg='red')
    # if but_0.state()[1] == but_1.state()[1] == but_3.state()[1] == 'selected':
    #     but_0.state(['selected'])
    if 'selected' not in but_0.state() and 'selected' not in but_1.state() and 'selected' not in but_3.state():
        but_0.state(['selected'])
        drag()


# 清屏
def clear():
    global px, click_num, stack
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


def save_1():
    checkvar = '1'
    sava(checkvar)


def save_0():
    checkvar = '0'
    sava(checkvar)


def sava(checkvar):
    """
    根据用户输入保存文件的函数。它提示用户选择保存文件的位置，将画布转换为 EPS 文件，
    然后使用 Ghostscript 将 EPS 文件转换为 JPG 文件。返回 Ghostscript 进程的退出代码。
    """
    current_time = time.strftime("%Y%m%d-%H%M%S")
    txt = temp_txt if temp_txt else '路线设计_' + current_time
    if not os.path.exists('./ms_download'):
        os.mkdir('./ms_download')
    path = filedialog.asksaveasfilename(title='保存为图片', filetypes=[("PNG", ".png")],
                                        initialdir=os.getcwd() + '/ms_download', initialfile=txt)
    if path:
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        x0 = canvas.winfo_rootx()  # 帧在屏幕上的左上角 x 坐标
        y0 = canvas.winfo_rooty()  # 帧在屏幕上的左上角 y 坐标
        x1 = x0 + width  # 帧在屏幕上的右下角 x 坐标
        y1 = y0 + height  # 帧在屏幕上的右下角 y 坐标
        ImageGrab.grab(bbox=(x0, y0, x1, y1)).save(path)  # 截取屏幕区域并保存为图片
        messagebox.showinfo("成功", f"保存成功,\n路径:{path}")

        # return exitcode


# 打开文件保存路径
def open_file():
    if not os.path.exists('./ms_download'):
        os.mkdir('./ms_download')
    if sys_name == 'Windows':
        subprocess.Popen(["explorer", os.getcwd() + r'\ms_download'])
    else:
        subprocess.call(["open", os.getcwd() + r'/ms_download'])


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
        canvas.itemconfig('choice_start', state='hidden')
        choice_tup.clear()
        stack.append(('删除', items))
    else:
        cur, line = get_cur()
        canvas.itemconfig(cur, state='hidden')
        canvas.itemconfig(line, state='hidden')
        stack.append(('删除', (cur, line)))

    remove_from_not_com()


# 网格辅助线
def grid():
    global create_grid, grid_start
    if grid_start:
        canvas.itemconfig('grid', stat='hidden')
        grid_start = 0
    elif create_grid and not grid_start:
        canvas.itemconfig('grid', stat='normal')
        grid_start = 1

    if not create_grid:
        range_x = (WIDTH + 30) // 100
        range_y = (HEIGHT + 70) // 100
        index_x = 15
        index_y = 50
        for i in range(range_x):
            canvas.create_line(index_x, 50, index_x, HEIGHT + 50, dash=(5, 3), tags=('grid', '不框选'))
            index_x += 100
        for i in range(range_y):
            canvas.create_line(15, index_y, WIDTH + 15, index_y, dash=(5, 3), tags=('grid', '不框选'))
            index_y += 100
        create_grid = True
        grid_start = 1


def info():
    global aux_stare
    if aux_stare:
        canvas.itemconfig('辅助信息', stat='hidden')
        aux_stare = False
    else:
        canvas.itemconfig('辅助信息', stat='normal')
        aux_stare = True


# 清除水印
def remove_f():
    global state_f
    canvas.delete(watermark)
    state_f = 0


# 关于软件
def about():
    app = ttk.Toplevel(win)
    app.title("关于软件")
    app.geometry("300x200")
    app_frame = ttk.Frame(app)
    app_frame.pack()
    ttk.Label(app_frame, image=icon_obj).pack(pady=15)
    ttk.Label(app_frame, text="路线设计", font=("宋体", 15, "bold")).pack()
    ttk.Label(app_frame, text="版本 1.0").pack()
    ttk.Label(app_frame, text="Copyright © 2022 山东体育学院.\nAll rights reserved.").pack()
    ttk.Label(app_frame, text="软件开发：许志亮 葛茂林").pack()


# 帮助文档
def open_web():
    webbrowser.open("https://gitee.com/gmlwb/ms/blob/master/README.md")


# 自定义障碍
def custom():
    global index_img

    img_path = filedialog.askopenfilename(title='选择Excel文件', filetypes=[("image", "*.jpg"), ("image", "*.png")])

    # image_path = expand(adjust_image_size(img_path))
    # image_path = start_direction(image_path)
    # image_path = start_direction(img_path)
    index_img += 1
    CreateImg(canvas, index_img, img_path).create()
    drag()


# 设置背景图
def fg():
    global fg_img, fg_path
    fg_path = filedialog.askopenfilename(title='选择Excel文件', filetypes=[("image", "*.jpg"), ("image", "*.png")])
    img = Image.open(fg_path)
    img = img.resize((WIDTH, HEIGHT))
    fg_img = ImageTk.PhotoImage(img)
    canvas.create_image(15, 50, image=fg_img, anchor='nw', tags=('不框选', 'bg'))


# 删除背景图
def del_fg():
    canvas.delete('bg')


frame_map = ttk.Frame(win, name="路线图").place(x=10, y=10)

# 路线图长度
ttk.Label(frame_map, text="长度(m):", font=FONT).grid(row=1, column=0, sticky='e', padx=5, pady=5)
var_l_w = ttk.StringVar()
var_l_w.set('90')
var_l_w_inp = Entry(frame_map, textvariable=var_l_w, width=5)
var_l_w_inp.grid(row=1, column=1, sticky='e', padx=5, pady=5)

# 路线图宽度
ttk.Label(frame_map, text="宽度(m):", font=FONT).grid(row=2, column=0, sticky='e', padx=5, pady=5)
var_l_h = ttk.StringVar()
var_l_h.set("60")
var_l_h_inp = Entry(frame_map, textvariable=var_l_h, width=5)
var_l_h_inp.grid(row=2, column=1, sticky='e', padx=5, pady=5)

ttk.Button(win, bootstyle=CONFIRM_STYLE, text="确认", command=found).grid(row=3, column=1, sticky='e', padx=5, pady=5)

ttk.Label(frame_map, text='全局障碍长度(m):', font=FONT).grid(row=1, column=3, sticky='e', padx=5, pady=5)
var_len = ttk.StringVar(value='4')
len_entt = Entry(frame_map, textvariable=var_len, width=4)
len_entt.grid(row=1, column=4, sticky='e', padx=5, pady=5)

ttk.Button(frame_map, bootstyle=CONFIRM_STYLE, text='确认', command=partial(set_len, var_len)).grid(row=2, column=4,
                                                                                                    sticky='e', padx=5,
                                                                                                    pady=5)

download_path = './demo.png'


def download(path):
    # for i in T.all_instances:
    #     attributes = vars(i)
    #     # 遍历属性字典并打印
    #     print(attributes)
    #     # for attribute, value in attributes.items():
    #     #     print(attribute, "=", value)
    # x = frame_info.winfo_x()
    # y = frame_info.winfo_y()
    width = canvas.winfo_width()
    height = canvas.winfo_height()
    x0 = canvas.winfo_rootx()  # 帧在屏幕上的左上角 x 坐标
    y0 = canvas.winfo_rooty()  # 帧在屏幕上的左上角 y 坐标
    x1 = x0 + width  # 帧在屏幕上的右下角 x 坐标
    y1 = y0 + height  # 帧在屏幕上的右下角 y 坐标
    ImageGrab.grab(bbox=(x0, y0, x1, y1)).save(path)  # 截取屏幕区域并保存为图片


ttk.Button(win, bootstyle="success-outline", text="保存", command=partial(download, download_path)).place(x=180, y=40)

# 障碍物
ttk.Button(frame_temp_1, bootstyle=BUTTON_STYLE, text='进出口', command=gate).pack()
ttk.Button(frame_temp_1, bootstyle=BUTTON_STYLE, text='指北针', command=compass).pack()
#
ttk.Button(frame_temp_2, bootstyle=BUTTON_STYLE, text='水障', command=water_barrier).pack()
ttk.Button(frame_temp_2, bootstyle=BUTTON_STYLE, text='砖墙', command=brick_wall).pack()
#
ttk.Button(frame_temp_3, bootstyle=BUTTON_STYLE, text='起/终点线', command=line).pack()
ttk.Button(frame_temp_3, bootstyle=BUTTON_STYLE, text='强制通过点', command=force).pack()

ttk.Button(frame_temp_4, bootstyle=BUTTON_STYLE, text='利物浦', command=live).pack()
ttk.Button(frame_temp_4, bootstyle=BUTTON_STYLE, text='单横木', command=monorail).pack()

ttk.Button(frame_temp_5, bootstyle=BUTTON_STYLE, text='双横木', command=oxer).pack()
ttk.Button(frame_temp_5, bootstyle=BUTTON_STYLE, text='三横木', command=tirail).pack()

ttk.Button(frame_temp_6, bootstyle=BUTTON_STYLE, text='AB组合障碍', command=combination_ab).pack()
ttk.Button(frame_temp_6, bootstyle=BUTTON_STYLE, text='ABC组合障碍', command=combination_abc).pack()

ttk.Button(frame_temp_7, bootstyle=BUTTON_STYLE, text='自定义障碍', command=custom).pack()
ttk.Button(frame_temp_7, bootstyle=BUTTON_STYLE, text='导入背景图', command=fg).pack()

# 障碍号
ttk.Label(frame_temp_9, text="障碍号：", font=FONT).pack(side="left")
var_id = ttk.StringVar()
e_id = Entry(frame_temp_9, textvariable=var_id, width=4)
e_id.pack(side="left")

ttk.Button(frame_temp_8, bootstyle=CONFIRM_STYLE, text='确认', command=insert).pack(padx=1)

if sys_name == 'Darwin':
    width = 5
elif sys_name == 'Windows':
    width = 5
# 工作模块
but_0 = ttk.Checkbutton(frame_command_left, text='拖动', command=drag, width=width, bootstyle="round-toggle")
but_0.pack()
but_0.state(['selected'])
but_3 = ttk.Checkbutton(frame_command_left, text='旋转', command=rotate, width=width, bootstyle="round-toggle")
but_3.pack()
but_3.state(['!selected'])

# but_4 = ttk.Button(frame_command_left, text='画弧', command=arc, width=width, height=1)
# but_4.pack()
# but_2 = ttk.Button(frame_command_left, text='橡皮', command=remove, width=width, height=1)
# but_2.pack()
ttk.Button(frame_mea_com_rig, bootstyle=BUTTON_STYLE, text='清空路线', command=clear, width=width).pack(side='right')
# ttk.Button(frame_command_right, text='撤销', command=back, width=width, height=1).pack()
ttk.Button(frame_command_right, bootstyle=BUTTON_STYLE, text='置底', command=set_state, width=width).pack()
ttk.Button(frame_command_right, bootstyle=BUTTON_STYLE, text='删除', command=pop, width=width).pack()

# 辅助模块
ttk.Button(frame_aux_com_lef, bootstyle=BUTTON_STYLE, text='网格辅助线', command=grid, width=width).pack()
aux_info = ttk.Checkbutton(frame_aux_com_rig, bootstyle="round-toggle", text='辅助信息', command=info, width=width)
aux_info.pack()
aux_info.state(['selected'])

# 障碍参数
ttk.Label(frame_aux_tit, text="障碍备注：", font=FONT).pack(pady=5)
var_parameter = ttk.StringVar()
e_parameter = Entry(frame_aux_inp, textvariable=var_parameter, width=8)
e_parameter.pack(pady=5)

ttk.Button(frame_aux_tit, bootstyle=CONFIRM_STYLE, text='确认', command=parameter).pack()
par_state = ttk.Button(frame_aux_inp, bootstyle="success-outline", text='隐藏', command=hidden)
par_state.pack()

# 圆
ttk.Label(frame_aux_tit2, text="圆(m)：", font=FONT).pack()
var_cir = ttk.StringVar()
e_id = Entry(frame_aux_inp2, textvariable=var_cir, width=3)
e_id.pack()

ttk.Button(frame_aux_but, bootstyle=CONFIRM_STYLE, text='确认', command=circular).pack()

# 测量模块
but_1 = ttk.Checkbutton(frame_mea_com_lef, bootstyle="round-toggle", text='长度测量', command=pen, width=width)
but_1.pack()

canvas.create_rectangle(15, 50, WIDTH + 15, HEIGHT + 50, state='disabled', tags=('不框选', '实际画布'))

# 右上角显示路线长宽
w = WIDTH / 10
h = HEIGHT / 10
h1 = canvas.create_text(WIDTH - 40, 60, text=f"长：{w}m", tags=('辅助信息', '不框选', '长'))
h2 = canvas.create_text(WIDTH - 40, 80, text=f"宽：{h}m", tags=('辅助信息', '不框选', '宽'))

# 左上角显示 5m的距离
canvas.create_text(45, 60, text="5m", tags=('辅助信息', '不框选'))
canvas.create_line(20, 65, 20, 70, tags=('辅助信息', '不框选'))
canvas.create_line(70, 65, 70, 70, tags=('辅助信息', '不框选'))
canvas.create_line(20, 70, 70, 70, tags=('辅助信息', '不框选'))

# 右上显示，路线长度
canvas.create_text(WIDTH - 40, 30, text=f"{px / 10}m", tags=('实时路线', '不框选', '辅助信息'))


# 鼠标实时坐标
def shu(event):
    x = event.x / 10 - 1.5
    y = event.y / 10 - 5
    canvas.itemconfig('鼠标x', text=f'x:{x:.2f}')
    canvas.itemconfig('鼠标y', text=f'y:{y:.2f}')


# 右下角显示鼠标实时坐标
canvas.create_text(WIDTH - 10, HEIGHT + 60, text='x:', tags=('辅助信息', '不框选', '鼠标x'))
canvas.create_text(WIDTH - 10, HEIGHT + 70, text='y:', tags=('辅助信息', '不框选', '鼠标y'))

canvas.bind('<Motion>', shu)

# 左下显示当前障碍坐标
canvas.create_text(30, HEIGHT + 60, text=f"x:", tags=('辅助信息', '不框选', '障碍x'))
canvas.create_text(30, HEIGHT + 70, text=f"y:", tags=('辅助信息', '不框选', '障碍y'))

# 水印
font = 0.16 if sys_name == 'Darwin' else 0.12
watermark = canvas.create_text(WIDTH / 2, (HEIGHT + 20) / 2, text="山东体育学院",
                               font=("行楷", int(WIDTH * font), "bold", "italic"), fill="#e4e4dc",
                               tags=("watermark", '不框选'), state='disabled')

# 画图
canvas.bind('<Button-1>', leftButtonDown)  # 鼠标左键点击事件
canvas.bind('<B1-Motion>', leftButtonMove)  # 鼠标左键移动事件
canvas.bind('<ButtonRelease-1>', leftButtonUp)  # 松开左键

# 标题
canvas.create_text((WIDTH + 40) / 2, 20, text='比赛名称', font=("微软雅黑", 18), tags=('比赛名称', '不框选'))

# 赛事信息主容器
frame_info = ttk.Frame(win)

entry_list = []
label_list = []

# 放赛事信息标题
frame_tit = ttk.Frame(frame_info)
# 放赛事信息输入框
frame_inp = ttk.Frame(frame_info)
# 建议信息容器
frame_por = ttk.Frame(frame_info)

frame_info.place(x=WIDTH + 200, y=150)

# 生成赛事信息
info_var = []
pro_var = []
edit()

# 菜单栏
menu = ttk.Menu(win)

# 障碍
obstacle_menu = ttk.Menu(menu, tearoff=0)
menu.add_cascade(label="障碍", menu=obstacle_menu)
obstacle_menu.add_command(label="四横木", command=four)

# 工具栏
menuType = ttk.Menu(menu, tearoff=0)
# menu_sava = ttk.Menu(menu, tearoff=0)
menu.add_cascade(label="工具栏", menu=menuType)
menuType.add_radiobutton(label="指针拖动", command=drag, variable=what, value=0)
menuType.add_radiobutton(label="旋转", command=rotate, variable=what, value=3)
menuType.add_radiobutton(label="长度测量", command=pen, variable=what, value=1)
# menuType.add_radiobutton(label="橡皮擦", command=remove, variable=what, value=2)

# 功能
function_menuType = ttk.Menu(menu, tearoff=0)
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
font_menuType = ttk.Menu(menu, tearoff=0)
menu.add_cascade(label="字号", menu=font_menuType)
# font_menuType.add_command(label="通用", command=currency_font)
font_menuType.add_command(label="长度测量", command=currency_pen)
# font_menuType.add_command(label="橡皮擦", command=currency_remove)

# 帮助
app_help = ttk.Menu(menu, tearoff=0)
menu.add_cascade(label="帮助", menu=app_help)
app_help.add_command(label="关于软件", command=about)
app_help.add_command(label="帮助文档", command=open_web)

win.config(menu=menu)


# 撤销
def undo(event):
    global px, route_click
    if stack and event.widget == win:
        item = stack.pop()
        if item[0] == '创建':
            pop(id=item[1])
        elif item[0] == '移动':
            for i in item[1]:
                canvas.move(i, -item[2][0], -item[2][1])
        elif item[0] == '删除':
            for i in item[1]:
                canvas.itemconfig(i, state='normal')
        elif item[0] == '长度测量':
            id, temp_px = item[1]
            for i in id:
                pop(i)
            px -= temp_px
            canvas.itemconfig('实时路线', text="%.2fm" % px)
            x, y = route_click.pop()
            start_x.set(x)
            start_y.set(y)
        elif item[0] == '旋转':
            obj = item[1]
            rotate_.pop()
            obj.rotate(obj.id, rotate_[-1])


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
    if 'ent' not in str(event.widget):
        win.focus_set()


def delete(event):
    if 'ent' not in str(event.widget):
        pop()


win.bind('<Button-1>', unfocus_click)
win.bind('<BackSpace>', delete)
# win.protocol("WM_DELETE_WINDOW", save)

win.mainloop()
