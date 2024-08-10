import json
import subprocess
import sys
import time
import tkinter.simpledialog
from tkinter import filedialog
from Common import *
from functools import partial

from Tools import *
from scale import CreateImg, CreateTxt, CreateParameter, T


def insert():
    """
    障碍号确认
    :return: 
    """
    global index_txt
    var = var_id.get()
    index_txt += 1
    CreateTxt(canvas, index_txt).create(var)
    e_id.delete(0, 'end')
    drag()


def parameter():
    """
    障碍备注
    :return: 
    """
    global index_txt
    var = var_parameter.get()
    index_txt += 1
    CreateParameter(canvas, index_txt).create(var)
    e_parameter.delete(0, 'end')
    drag()


def hidden():
    """
    隐藏障碍
    :return: 
    """
    global par_index
    if par_index:
        canvas.itemconfig('parameter', state='hidden')
        par_state.config(text='显示')
        par_index = 0
    else:
        canvas.itemconfig('parameter', state='normal')
        par_state.config(text='隐藏')
        par_index = 1


def monorail():
    """
    单横木
    :return: 
    """
    global index_img
    image_path = expand(get_one_path())
    image_path = start_direction(image_path)
    index_img += 1
    CreateImg(canvas, index_img, obstacle='monorail').create(image_path)
    drag()


def oxer():
    """
    双横木
    :return: 
    """
    global index_img
    image_path = merge(10)
    image_path = start_direction(image_path)
    index_img += 1
    CreateImg(canvas, index_img, obstacle='oxer').create(image_path)
    drag()


def tirail():
    """
    三横木
    :return: 
    """
    global index_img
    image_path = merge(10, oxer='tirail')
    index_img += 1
    CreateImg(canvas, index_img, obstacle='tirail').create(image_path)
    drag()


def four():
    """
    四横木
    :return:
    """
    global index_img
    image_path = merge(15, oxer='four')
    index_img += 1
    CreateImg(canvas, index_img, obstacle='four').create(image_path)
    drag()


def combination_ab():
    """
    AB组合障碍
    :return: 
    """
    global index_img
    image_path = merge_ab(state=1, m1=30)
    index_img += 1
    CreateImg(canvas, index_img, obstacle="combination_ab").create(image_path)
    drag()


def combination_abc():
    """
    ABC组合障碍
    :return: 
    """
    global index_img
    image_path = merge_ab(state=1, m1=30, m2=30)
    index_img += 1
    CreateImg(canvas, index_img, obstacle="combination_abc").create(image_path)
    drag()


def live():
    """
    利物浦
    :return: 
    """
    global index_img
    index_img += 1
    # image_path = expand(get_live_path())
    image_path = live_one_tool()
    CreateImg(canvas, index_img, obstacle='live').create(image_path)
    drag()


def force():
    """
    强制通过点
    :return: 
    """
    global index_img
    index_img += 1
    CreateImg(canvas, index_img).create(force_image)
    drag()


def compass():
    """
    指北针
    :return: 
    """
    global index_img
    index_img += 1
    image_path = expand(compass_image)
    CreateImg(canvas, index_img).create(image_path)
    drag()


def water_barrier():
    """
    水障
    :return: 
    """
    global index_img
    index_img += 1
    image_path = expand(water_barrier_iamge)
    image_path = start_direction(image_path)
    CreateImg(canvas, index_img, obstacle='water').create(image_path)
    drag()


def brick_wall():
    """
    砖墙
    :return: 
    """
    global index_img
    index_img += 1
    image_path = expand(brick_wall_image)
    image_path = start_direction(image_path)
    CreateImg(canvas, index_img).create(image_path)
    drag()


def line():
    """
    起/终点线
    :return: 
    """
    global index_img
    index_img += 1
    image_path = expand(line_image)
    image_path = start_direction(image_path)
    CreateImg(canvas, index_img).create(image_path)
    drag()


def gate():
    """
    进出口
    :return: 
    """
    global index_img
    index_img += 1
    image_path = expand(gate_image)
    CreateImg(canvas, index_img).create(image_path)
    drag()


def tree():
    """
    树
    :return: 
    """
    global index_img
    index_img += 1
    image_path = expand(tree_image)
    CreateImg(canvas, index_img).create(image_path)
    drag()


def joker():
    """
    小丑
    :return:
    """
    global index_img
    index_img += 1
    image_path = expand(joker_image)
    CreateImg(canvas, index_img).create(image_path)
    drag()


def circular():
    """
    圆
    :return: 
    """
    global index_img
    index_img += 1
    cir = int(var_cir.get()) * 10
    img = Image.open(circular_image)
    img = img.resize((cir, cir))
    img.save('./img/cir.png')
    cir_path = './img/cir.png'
    CreateImg(canvas, index_img).create(cir_path)
    drag()


def custom():
    """
    自定义障碍
    :return: 
    """
    global index_img

    img_path = filedialog.askopenfilename(title='选择图片', filetypes=[("image", "*.jpg"), ("image", "*.png")])

    # image_path = expand(adjust_image_size(img_path))
    # image_path = start_direction(image_path)
    # image_path = start_direction(img_path)
    index_img += 1
    CreateImg(canvas, index_img, obstacle='diy').create(img_path)
    drag()


def fg():
    """
    设置背景图
    :return: 
    """
    global fg_img, fg_path
    fg_path = filedialog.askopenfilename(title='选择图片', filetypes=[("image", "*.jpg"), ("image", "*.png")])
    img = Image.open(fg_path)
    img = img.resize((WIDTH, HEIGHT))
    fg_img = ImageTk.PhotoImage(img)
    canvas.create_image(15, 50, image=fg_img, anchor='nw', tags=('不框选', 'bg'))


def del_fg():
    """
    删除背景图
    :return: 
    """
    canvas.delete('bg')


def dle():
    """
    赛事信息确认
    :return: 
    """
    global temp_txt, entry_list, label_list, filtered_dict
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
            elif title == '级别赛制':
                temp_txt = data_dict.get(title, "")
                canvas.itemconfig('级别赛制', text=temp_txt)
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
        print(f"{os.path.basename(__file__)}, line {sys._getframe().f_lineno}, {e}")
        messagebox.showerror("Error", "出错了")
        logging.warning("赛事信息确认", e)


def edit(current_dist=None):
    """
    赛事信息修改
    :param current_dist: 
    :return: 
    """
    global entry_list, label_list
    data_dict = {'比赛名称': '', '级别赛制': '', '比赛日期': '', '路线查看时间': '', '开赛时间': '', '判罚表': '',
                 '障碍高度': '', '行进速度': '', '路线长度': '', '允许时间': '', '限制时间': '', '障碍数量': '',
                 '跳跃数量': '', '附加赛': '', '路线设计师': ''}

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
        print(f"{os.path.basename(__file__)}, line {sys._getframe().f_lineno}, {e}", '赛事信息出错：', e)
        logging.warning('赛事信息出错：', e)
        return False


def found():
    """
    生成路线图
    :return: 
    """
    global WIDTH, HEIGHT, h1, h2, watermark, fg_img, fg_path
    w = var_l_w.get()
    h = var_l_h.get()
    # if w.isdigit() and h.isdigit():
    WIDTH = int(float(w) * 10)
    HEIGHT = int(float(h) * 10)
    canvas.config(width=WIDTH + 30, height=HEIGHT + 180)
    canvas.coords('实际画布', 30, 120, WIDTH + 15, HEIGHT + 120)
    # canvas.place(x=175, y=130)
    # but1.place(x=WIDTH + 260, y=700)
    # but2.place(x=WIDTH + 360, y=700)
    frame_info.place(x=WIDTH + 200, y=150)
    canvas.delete(watermark)
    wid = WIDTH / 10
    hei = HEIGHT / 10
    canvas.itemconfig('长', text=f"长：{wid}m")
    canvas.itemconfig('宽', text=f"宽：{hei}m")
    canvas.coords('长', WIDTH - 40, 130)
    canvas.coords('宽', WIDTH - 40, 150)
    canvas.coords('实时路线', WIDTH - 40, 100)
    canvas.coords('障碍x', 35, HEIGHT + 130)
    canvas.coords('障碍y', 35, HEIGHT + 140)
    canvas.coords('鼠标x', WIDTH - 10, HEIGHT + 130)
    canvas.coords('鼠标y', WIDTH - 10, HEIGHT + 140)
    # canvas.coords('比赛名称', (WIDTH + 40) / 2, 120)
    canvas.delete('bg')
    try:
        img = Image.open(fg_path)
        img = img.resize((WIDTH, HEIGHT))
        fg_img = ImageTk.PhotoImage(img)
        canvas.create_image(15, 50, image=fg_img, anchor='nw', tags=('不框选', 'bg'))
    except AttributeError as e:
        print(f"{os.path.basename(__file__)}, line {sys._getframe().f_lineno}, {e}", '背景图错误：', e)

    if state_f:
        font = 0.16 if sys_name == 'Darwin' else 0.1
        watermark = canvas.create_text((WIDTH + 35) / 2, (HEIGHT + 220) / 2, text="山东体育学院",
                                       font=("行楷", int(WIDTH * font), "bold", "italic"), fill="#e4e4dc",
                                       tags=("watermark", '不框选'))
        canvas.lower("watermark")
    # else:
    #     messagebox.showerror('错误', '请输入正整数')
    #     if w.isdigit():
    #         var_l_h_inp.delete(0, 'end')
    #     if h.isdigit():
    #         var_l_w_inp.delete(0, 'end')


def leftButtonDown(event):
    """
    鼠标左键按下
    :param event: 
    :return: 
    """
    global choice_tup, current_line
    if choice_tup and not (min(choice_tup[0], choice_tup[2]) < event.x < max(choice_tup[0], choice_tup[2])
                           and min(choice_tup[1], choice_tup[3]) < event.y < max(choice_tup[1], choice_tup[3])):
        canvas.delete('choice')
        choice_tup.clear()
        canvas.dtag('choice_start', 'choice_start')
    X.set(event.x)
    Y.set(event.y)
    move_x.set(event.x)
    move_y.set(event.y)
    current_line = [(event.x, event.y)]


def leftButtonMove(event):
    """
    鼠标左键滚动事件
    :param event: 
    :return: 
    """
    global lastDraw, px, remove_px, click_num, choice_tup, current_frame_stare, current_line, rect_stare
    shu(event)

    if rect_stare:
        return

    # 获取点击位置的 item id
    item_id = event.widget.find_closest(event.x, event.y)[0]
    # 获取该 item 的 tag
    tags = event.widget.gettags(item_id)
    if 'rect_arc' in tags:
        return

        # 画线
    if what.get() == 1:
        lastDraw = canvas.create_line(X.get(), Y.get(), event.x, event.y,
                                      fill='#000000', width=font_size, tags=("line", '不框选'), smooth=True)

        current_line.append((event.x, event.y))

        x1, y1, x2, y2 = canvas.coords(lastDraw)

        lenth = (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) / 10
        update_px(lenth)
        temp_px = (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) / 10

        remove_px[lastDraw] = temp_px
        # canvas.itemconfig('实时路线', text="%.2fm" % px)
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
            # print(canvas.find_withtag('choice_start'))
            # for i in canvas.find_withtag('choice_start'):
            #     try:
            #         x, y = canvas.coords(i)
            #         canvas.image_data[i].current_x, canvas.image_data[
            #             i].current_y = x, y
            #     except KeyError:
            #         pass
            X.set(event.x)
            Y.set(event.y)
            # for i in canvas.find_withtag('choice_start')[:-1]:
            #     canvas.image_data[i].current_x, canvas.image_data[i].current_y = event.x - X.get(), event.y - Y.get()
            try:
                choice_tup.clear()
                choice_tup.extend(list(bbox))
            except TypeError as e:
                print(f"{os.path.basename(__file__)}, line {sys._getframe().f_lineno}, {e}", '多选框移动出错', e)
                logging.warning('多选框移动出错', e)
    else:
        if get_frame_stare():
            canvas.delete('choice')
            canvas.create_rectangle(X.get(), Y.get(), event.x, event.y, tags='choice', dash=(3, 5))
            # current_frame_stare = True


def leftButtonUp(event):
    """
    松开左键
    :param event: 
    :return: 
    """
    global lastDraw, click_num, px, choice_tup, choice_start, remove_px, lines, current_line, rect_stare
    rect_stare = False
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
            lines.append(current_line)
            current_line = None

        elif click_num == 2:
            end_x.set(event.x)
            end_y.set(event.y)
            # click_num = 1
            id = canvas.create_line(start_x.get(), start_y.get(), end_x.get(), end_y.get(), tags=("line", '不框选'),
                                    smooth=True)

            # x = abs(end_x.get() - start_x.get())
            # y = abs(end_y.get() - start_y.get())
            # temp_px = (abs(x + y)) / 10
            x1, y1, x2, y2 = canvas.coords(id)
            distance = (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) / 10
            # px += distance
            update_px(distance)
            route_click.append((start_x.get(), start_y.get()))
            stack.append(('长度测量', ([id], distance)))
            # canvas.itemconfig('实时路线', text="%.2fm" % px)
            # remove_px[lastDraw] = px
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
        choice_tup.clear()


def drag():
    """
    拖动
    :return:
    """
    what.set(0)
    set_color()
    # no_what.set(0)


def pen():
    """
    铅笔
    :return:
    """
    global click_num
    what.set(1)
    set_color()
    # no_what.set(1)
    click_num = 1


def remove():
    """
    橡皮擦
    :return:
    """
    what.set(2)
    set_color()
    # no_what.set(2)


def rotate():
    """
    旋转
    :return:
    """
    what.set(3)
    set_color()
    # no_what.set(3)


def arc():
    """
    画弧
    :return:
    """
    if check_var.get():
        # for i in T.all_instances:

        for i in T.all_instances:
            if i.ui_state:
                try:
                    i.draw_rectangles()
                except AttributeError:
                    pass
    else:
        canvas.delete("rect_arc")


def set_color():
    id = what.get()
    # no_id = no_what.get()
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


def clear():
    """
    清屏
    :return: 
    """
    global px, click_num, stack, lines
    canvas.delete("line")
    canvas.delete("rubber")
    lines.clear()
    # px = 0
    update_px(0, clear=True)
    # canvas.itemconfig('实时路线', text="%.2fm" % px)
    click_num = 1
    to_be_deleted = []
    for i in range(len(stack)):
        if stack[i][0] == '长度测量':
            to_be_deleted.append(i)
    for idx in reversed(to_be_deleted):
        stack.pop(idx)


def back():
    """
    撤销
    :return: 
    """
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
    update_px(temp, start=False)
    # px -= temp
    #
    # canvas.itemconfig('实时路线', text="%.2fm" % px)


def currency_font():
    """
    通用字号
    :return: 
    """
    global font_size, remove_size, size
    size = tkinter.simpledialog.askinteger('输入字号', prompt='', initialvalue=size)
    font_size = remove_size = size


def currency_pen():
    """
    铅笔字号
    :return: 
    """
    global font_size
    font_size = tkinter.simpledialog.askinteger('输入字号', prompt='', initialvalue=font_size)


def currency_remove():
    """
    橡皮擦字号
    :return: 
    """
    global remove_size
    remove_size = tkinter.simpledialog.askinteger('输入字号', prompt='', initialvalue=remove_size)


def save_1():
    """
    保存图片包含右侧赛事信息
    :return:
    """
    checkvar = True
    download(checkvar)


def save_0():
    """
    保存图片不包含右侧赛事信息
    :return:
    """
    checkvar = False
    download(checkvar)


def download(checkvar):
    """
    保存图片
    :return: 
    """
    current_time = time.strftime("%Y%m%d-%H%M%S")
    txt = temp_txt if temp_txt else '路线设计_' + current_time
    if not os.path.exists('./ms_download'):
        os.mkdir('./ms_download')
    path = filedialog.asksaveasfilename(title='保存为图片', filetypes=[("JPEG", ".jpg")],
                                        initialdir=os.getcwd() + '/ms_download', initialfile=txt)
    if path:
        width = canvas.winfo_width()
        height = canvas.winfo_height()
        x0 = canvas.winfo_rootx() + 10  # 帧在屏幕上的左上角 x 坐标
        y0 = canvas.winfo_rooty()  # 帧在屏幕上的左上角 y 坐标
        frame_x1 = 0
        frame_y1 = 0
        if checkvar:
            frame_width = frame_info.winfo_width()
            frame_height = frame_info.winfo_height()
            frame_x0 = frame_info.winfo_rootx() + 10  # 帧在屏幕上的左上角 x 坐标
            frame_y0 = frame_info.winfo_rooty()  # 帧在屏幕上的左上角 y 坐标
            frame_x1 = frame_x0 + frame_width - 5  # 帧在屏幕上的右下角 x 坐标
            frame_y1 = frame_y0 + frame_height  # 帧在屏幕上的右下角 y 坐标
            x1 = x0 + width - 5  # 帧在屏幕上的右下角 x 坐标
            y1 = y0 + height  # 帧在屏幕上的右下角 y 坐标
        else:
            x1 = x0 + width - 5  # 帧在屏幕上的右下角 x 坐标
            y1 = y0 + height  # 帧在屏幕上的右下角 y 坐标
        if sys_name == 'Windows':
            path += '.jpg'

        x1 = max(x1, frame_x1)
        y1 = max(y1, frame_y1)
        ImageGrab.grab(bbox=(x0, y0, x1, y1)).convert("RGB").save(path)

        messagebox.showinfo("成功", f"保存成功,\n路径:{path}")


def open_file():
    """
    打开文件保存路径
    :return: 
    """
    if not os.path.exists('./ms_download'):
        os.mkdir('./ms_download')
    if sys_name == 'Windows':
        subprocess.Popen(["explorer", os.getcwd() + r'\ms_download'])
    else:
        subprocess.call(["open", os.getcwd() + r'/ms_download'])


def set_state():
    """
    置底
    :return: 
    """
    cur, line = get_cur()
    canvas.lower(cur)
    canvas.lower("watermark")


def pop(id=None):
    """
    删除
    :param id: 
    :return: 
    """
    if id:
        cur, line = get_cur()
        try:
            for i in id:
                canvas.delete(i)

        except:
            canvas.delete(id)

        if id == cur:
            canvas.delete(line)
            remove_from_not_com()
        return
    items = canvas.find_withtag("choice_start")[:-1]
    if items:
        canvas.itemconfig('choice', state='hidden')
        canvas.itemconfig('choice_start', state='hidden')
        canvas.dtag('choice_start', 'choice_start')
        for i in items:
            try:
                for arc_ in arc_list:
                    if i in arc_:
                        length = compute_arc_length(i)
                        update_px(length / 10, start=False)
                canvas.image_data[i].ui_state = not canvas.image_data[i].ui_state
            except KeyError:
                pass

            for arc_ in arc_list:
                if i in arc_:
                    arc_list.remove(arc_)
        choice_tup.clear()
        stack.append(('删除', items))
    else:
        cur, line = get_cur()
        canvas.itemconfig(cur, state='hidden')
        canvas.itemconfig(line, state='hidden')
        stack.append(('删除', (cur, line), get_obstacle()))
        get_obstacle().ui_state = not get_obstacle().ui_state

    remove_from_not_com()


def grid():
    """
    网格辅助线
    :return: 
    """
    global grid_start

    if grid_start:
        canvas.delete('grid')
        grid_start = 0
    elif not grid_start:
        range_x = (WIDTH + 15) // 100
        range_y = (HEIGHT + 70) // 100
        index_x = 30
        index_y = 50
        step = 100
        # 垂直线
        for i in range(range_x):
            canvas.create_line(index_x, 50, index_x, HEIGHT + 50, dash=(5, 3), tags=('grid', '不框选'), smooth=True)
            index_x += step
        # 水平线
        for i in range(range_y):
            canvas.create_line(30, index_y, WIDTH + 15, index_y, dash=(5, 3), tags=('grid', '不框选'), smooth=True)
            index_y += step
        grid_start = 1


def info():
    """
    辅助信息
    :return: 
    """
    global aux_stare
    if aux_stare:
        canvas.itemconfig('辅助信息', stat='hidden')
        aux_stare = False
    else:
        canvas.itemconfig('辅助信息', stat='normal')
        aux_stare = True


def remove_f():
    """
    清除水印
    :return: 
    """
    global state_f
    canvas.delete(watermark)
    state_f = 0


def about():
    """
    关于软件
    :return: 
    """
    app = ttk.Toplevel(win)
    app.title("关于软件")
    app.geometry("300x200")
    app_frame = ttk.Frame(app)
    app_frame.pack()
    ttk.Label(app_frame, image=icon_obj).pack(pady=15)
    ttk.Label(app_frame, text="路线设计", font=("宋体", 15, "bold")).pack()
    ttk.Label(app_frame, text=f"版本 {CURRENT_VERSION}").pack()
    ttk.Label(app_frame, text="Copyright © 2024 山东体育学院.\nAll rights reserved.").pack()
    ttk.Label(app_frame, text="软件开发：许志亮 葛茂林").pack()


def open_web():
    """
    帮助文档
    :return: 
    """
    webbrowser.open("https://gitee.com/gmlwb/ms/blob/master/README.md")


def get_center(rect):
    """
    获取矩形中心点
    :param rect:
    :return:
    """
    x1, y1, c_x, c_y, c_x2, c_y2, x2, y2 = canvas.coords(rect)
    return (x1 + x2) / 2, (y1 + y2) / 2


def save():
    """
    保存成路线图数据
    :return:
    """

    if not os.path.exists('./backup'):
        os.mkdir('./backup')

    current_time = time.strftime("%Y%m%d-%H%M%S")
    txt = temp_txt if temp_txt else '路线设计_' + current_time

    path = filedialog.asksaveasfilename(title='保存路线图数据', filetypes=[("JSON files", "*.json")],
                                        initialdir=os.getcwd() + '/backup', initialfile=txt)
    if path:
        save_dict = {}

        # 保存障碍信息
        for i in T.all_instances:
            if i.ui_state:
                save_dict.update(i.save())

        # 保存路线图长度
        save_dict['var_l_w'] = var_l_w.get()
        # 保存路线图宽度
        save_dict['var_l_h'] = var_l_h.get()
        # 保存赛事信息
        save_dict['filtered_dict'] = filtered_dict
        # 保存路线
        save_dict['lines'] = lines
        # 保存全局障碍长度
        save_dict['var_len'] = var_len.get()
        # 保存弧线信息
        temp_arc = []
        for arc, rect1, rect2, control_point in arc_list:
            rect1_center = get_center(rect1)
            rect2_center = get_center(rect2)
            temp_arc.append((arc, rect1, rect2, rect1_center, rect2_center, control_point))
        save_dict['arc_list'] = temp_arc
        # 保存图片索引
        save_dict['index_img'] = index_img
        # 保存比赛名称位置
        save_dict['title'] = canvas.coords('比赛名称')
        # 保存级别赛制
        save_dict['level'] = canvas.coords('级别赛制')

        if sys_name == 'Windows':
            path += '.json'

        with open(path, 'w', encoding='utf-8') as file:
            json.dump(save_dict, file, ensure_ascii=False)
        messagebox.showinfo("保存成功", f"程序状态已保存至{path}")


def load():
    """
    加载路线图数据
    :return: 
    """
    global lines, arc_list, index_img
    file_path = filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    # reload_window()
    if file_path:
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                state = json.load(file)

            # 删除画布障碍
            for i in T.all_instances:
                canvas.delete(i.tag)
            canvas.delete('arc')

            # 加载标题坐标
            canvas.coords('比赛名称', state['title'])
            canvas.coords('级别赛制', state['level'])

            # 加载弧线
            set_rect_center(state['arc_list'])

            # 加载障碍
            for key, value in state.items():
                if '障碍组件' in key:
                    CreateImg(canvas, value['index'], value['img_path'], ).load(**value)
                elif '障碍号' in key:
                    CreateTxt(canvas, value['index']).load(**value)
                elif '障碍备注' in key:
                    CreateParameter(canvas, value['index']).load(**value)

            # 更新路线图
            var_l_h.set(state['var_l_h'])
            var_l_w.set(state['var_l_w'])
            found()

            # 更新赛事信息
            edit(state['filtered_dict'])

            # 加载路线
            lines = state['lines']
            for line in lines:
                for i in range(len(line) - 1):
                    x0, y0 = line[i]
                    x1, y1 = line[i + 1]
                    canvas.create_line(x0, y0, x1, y1, fill='#000000', width=font_size, tags=("line", '不框选'),
                                       smooth=True)

            # 全局障碍
            set_len(state['var_len'])
            index_img = state['index_img']

            messagebox.showinfo("加载成功", "程序状态已从文件加载")
        except Exception as e:
            print(f"{os.path.basename(__file__)}, line {sys._getframe().f_lineno}, {e}", e)
            messagebox.showerror("加载失败", f"无法加载文件: {e}")


def unfocus_click(event):
    if 'ent' not in str(event.widget):
        win.focus_set()


def delete(event):
    if 'ent' not in str(event.widget):
        pop()


def undo(event):
    """
    撤销
    :param event: 
    :return: 
    """
    global px, route_click, lines
    if stack and event.widget == win:
        item = stack.pop()
        if item[0] == '创建':
            pop(id=item[1])
            item[-1].ui_state = 0
        elif item[0] == '移动':
            for index, value in enumerate(item[1]):
                canvas.move(value, -item[2][0], -item[2][1])
                if index == len(item[1]) - 1:
                    break
                x, y = canvas.coords(value)
                canvas.image_data[value].current_x, canvas.image_data[value].current_y = x, y
        elif item[0] == '删除':
            for i in item[1]:
                canvas.itemconfig(i, state='normal')
                canvas.image_data[i].ui_state = not canvas.image_data[i].ui_state
        elif item[0] == '长度测量':
            id, temp_px = item[1]
            temp_line = []
            for i in id:
                temp_line.append(canvas.coords(i))
                pop(i)
            lines.pop()
            update_px(temp_px, start=False)
            # px -= temp_px
            # canvas.itemconfig('实时路线', text="%.2fm" % px)
            x, y = route_click.pop()
            start_x.set(x)
            start_y.set(y)
        elif item[0] == '旋转':
            obj = item[1]
            rotate_.pop()
            obj.rotate(obj.id, rotate_[-1])


def tit_click(event):
    """
    标题栏点击
    :param event:
    :return:
    """
    global tit_x, tit_y
    tit_x, tit_y = event.x, event.y


def tit_move(event):
    """
    标题栏移动
    :param event:
    :return:
    """
    global tit_x, tit_y
    set_frame_stare(False)
    canvas.move('比赛名称', event.x - tit_x, event.y - tit_y)
    tit_x, tit_y = event.x, event.y


def level_click(event):
    """
    等级按钮点击
    :param event:
    :return:
    """
    global level_x, level_y
    level_x, level_y = event.x, event.y


def level_move(event):
    """
    等级按钮移动
    :param event:
    :return:
    """
    global level_x, level_y
    set_frame_stare(False)
    canvas.move('级别赛制', event.x - level_x, event.y - level_y)
    level_x, level_y = event.x, event.y


frame_map = ttk.Frame(win, name="路线图")
frame_map.place(x=10, y=10)

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

ttk.Button(frame_map, bootstyle=CONFIRM_STYLE, text="确认", command=found).grid(row=3, column=1, sticky='w')

frame_obstacle_length = ttk.Frame(win, name="全局障碍")
frame_obstacle_length.place(x=180, y=10)
ttk.Label(frame_obstacle_length, text='全局障碍长度(m):', font=FONT).grid(row=1, column=3, sticky='e', padx=5, pady=5)
var_len = ttk.StringVar(value='4')
len_ent = Entry(frame_obstacle_length, textvariable=var_len, width=4)
len_ent.grid(row=1, column=4, sticky='e', padx=5, pady=5)

ttk.Button(frame_obstacle_length, bootstyle=CONFIRM_STYLE, text='确认', command=partial(set_len, var_len)).grid(row=2,
                                                                                                                column=4,
                                                                                                                sticky='e',
                                                                                                                padx=5,
                                                                                                                pady=5)

# 障碍物
ttk.Button(frame_create, bootstyle=BUTTON_STYLE, text='进出口', command=gate).grid(row=0, column=0)
ttk.Button(frame_create, bootstyle=BUTTON_STYLE, text='指北针', command=compass).grid(row=1, column=0)
#
ttk.Button(frame_create, bootstyle=BUTTON_STYLE, text='水障', command=water_barrier).grid(row=0, column=1)
ttk.Button(frame_create, bootstyle=BUTTON_STYLE, text='砖墙', command=brick_wall).grid(row=1, column=1)
#
ttk.Button(frame_create, bootstyle=BUTTON_STYLE, text='起/终点线', command=line).grid(row=0, column=2)
ttk.Button(frame_create, bootstyle=BUTTON_STYLE, text='强制通过点', command=force).grid(row=1, column=2)

ttk.Button(frame_create, bootstyle=BUTTON_STYLE, text='利物浦', command=live).grid(row=0, column=3)
ttk.Button(frame_create, bootstyle=BUTTON_STYLE, text='单横木', command=monorail).grid(row=1, column=3)

ttk.Button(frame_create, bootstyle=BUTTON_STYLE, text='双横木', command=oxer).grid(row=0, column=4)
ttk.Button(frame_create, bootstyle=BUTTON_STYLE, text='三横木', command=tirail).grid(row=1, column=4)

ttk.Button(frame_create, bootstyle=BUTTON_STYLE, text='AB组合障碍', command=combination_ab).grid(row=0, column=5)
ttk.Button(frame_create, bootstyle=BUTTON_STYLE, text='ABC组合障碍', command=combination_abc).grid(row=1, column=5)

ttk.Button(frame_create, bootstyle=BUTTON_STYLE, text='自定义障碍', command=custom).grid(row=0, column=6)
ttk.Button(frame_create, bootstyle=BUTTON_STYLE, text='导入背景图', command=fg).grid(row=1, column=6)

# 障碍号
ttk.Label(frame_create, text="障碍号：", font=FONT).grid(row=0, column=7)
var_id = ttk.StringVar()
e_id = Entry(frame_create, textvariable=var_id, width=4)
e_id.grid(row=0, column=8)

ttk.Button(frame_create, bootstyle=CONFIRM_STYLE, text='确认', command=insert).grid(row=1, column=8)

width = 6

# 工作模块
but_0 = ttk.Checkbutton(frame_command, text='拖动', command=drag, width=width, bootstyle="round-toggle")
but_0.grid(row=0, column=1, padx=0, pady=0)
but_0.state(['selected'])
but_3 = ttk.Checkbutton(frame_command, text='旋转', command=rotate, width=width, bootstyle="round-toggle")
but_3.grid(row=1, column=1, padx=0, pady=0)
but_3.state(['!selected'])

# but_2 = ttk.Button(frame_command_left, text='橡皮', command=remove, width=width, height=1)
# but_2.pack()

ttk.Button(frame_command, bootstyle=BUTTON_STYLE, text='置底', command=set_state, width=width).grid(row=0, column=0,
                                                                                                    padx=0, pady=0)
ttk.Button(frame_command, bootstyle=BUTTON_STYLE, text='删除', command=pop, width=width).grid(row=1, column=0, padx=0,
                                                                                              pady=0)

# 辅助模块
ttk.Button(frame_command, bootstyle=BUTTON_STYLE, text='网格辅助线', command=grid, width=width).grid(row=2, column=0,
                                                                                                     padx=0, pady=0)
aux_info = ttk.Checkbutton(frame_command, bootstyle="round-toggle", text='辅助信息', command=info, width=width)
aux_info.grid(row=2, column=1, padx=0, pady=0)
aux_info.state(['selected'])

arc_info = ttk.Checkbutton(frame_command, bootstyle="round-toggle", text='弧线', command=arc, width=width,
                           variable=check_var, )
arc_info.grid(row=3, column=1, padx=0, pady=0)

# 障碍参数
ttk.Label(frame_aux_info, text="障碍备注：", font=FONT).grid(row=0, column=0, padx=0, pady=0)
var_parameter = ttk.StringVar()
e_parameter = Entry(frame_aux_info, textvariable=var_parameter, width=5)
e_parameter.grid(row=0, column=1, padx=0, pady=0)

ttk.Button(frame_aux_info, bootstyle=CONFIRM_STYLE, text='确认', command=parameter).grid(row=1, column=0, padx=0,
                                                                                         pady=0)
par_state = ttk.Button(frame_aux_info, bootstyle="success-outline", text='隐藏', command=hidden)
par_state.grid(row=1, column=1, padx=0, pady=0)

# 圆
ttk.Label(frame_aux_info, text="圆(m)：", font=FONT).grid(row=2, column=0, padx=0, pady=0, sticky='e')
var_cir = ttk.StringVar()
e_id = Entry(frame_aux_info, textvariable=var_cir, width=5)
e_id.grid(row=2, column=1, sticky='w')
ttk.Button(frame_aux_info, bootstyle=CONFIRM_STYLE, text='确认', command=circular).grid(row=3, column=1, padx=0, pady=0,
                                                                                        sticky='w')

# 测量模块
but_1 = ttk.Checkbutton(frame_mea_com, bootstyle="round-toggle", text='画路线', command=pen, width=width)
but_1.grid(row=0, column=0, padx=1, pady=1)

ttk.Button(frame_mea_com, bootstyle=BUTTON_STYLE, text='清空路线', command=clear, width=width).grid(row=0, column=1,
                                                                                                    padx=0, pady=0)

canvas.create_rectangle(30, 120, WIDTH + 15, HEIGHT + 120, state='disabled', tags=('不框选', '实际画布'))

# 右上角显示路线长宽
w = WIDTH / 10
h = HEIGHT / 10
h1 = canvas.create_text(WIDTH - 40, 130, text=f"长：{w}m", tags=('辅助信息', '不框选', '长'))
h2 = canvas.create_text(WIDTH - 40, 150, text=f"宽：{h}m", tags=('辅助信息', '不框选', '宽'))

# 左上角显示 5m的距离
canvas.create_text(60, 130, text="5m", tags=('辅助信息', '不框选'))
canvas.create_line(35, 135, 35, 140, tags=('辅助信息', '不框选'))
canvas.create_line(85, 135, 85, 140, tags=('辅助信息', '不框选'))
canvas.create_line(35, 140, 85, 140, tags=('辅助信息', '不框选'))

# 右上显示，路线长度
canvas.create_text(WIDTH - 40, 100, text=f"{px / 10}m", tags=('实时路线', '不框选', '辅助信息'))


# 鼠标实时坐标
def shu(event):
    x = event.x / 10 - 1.5
    y = event.y / 10 - 5
    canvas.itemconfig('鼠标x', text=f'x:{x:.2f}')
    canvas.itemconfig('鼠标y', text=f'y:{y:.2f}')


# 右下角显示鼠标实时坐标
canvas.create_text(WIDTH - 10, HEIGHT + 130, text='x:', tags=('辅助信息', '不框选', '鼠标x'))
canvas.create_text(WIDTH - 10, HEIGHT + 140, text='y:', tags=('辅助信息', '不框选', '鼠标y'))

canvas.bind('<Motion>', shu)

# 左下显示当前障碍坐标
canvas.create_text(35, HEIGHT + 130, text=f"x:", tags=('辅助信息', '不框选', '障碍x'))
canvas.create_text(35, HEIGHT + 140, text=f"y:", tags=('辅助信息', '不框选', '障碍y'))

# 水印
font = 0.16 if sys_name == 'Darwin' else 0.1
# watermark = canvas.create_text((WIDTH + 35) / 2, (HEIGHT + 220) / 2, text="山东体育学院",
#                                font=("行楷", int(WIDTH * font), "bold", "italic"), fill="#e4e4dc",
#                                tags=("watermark", '不框选'), state='disabled')

watermark = canvas.create_text((WIDTH + 35) / 2, (HEIGHT + 220) / 2, text="DEMO",
                               font=("行楷", int(WIDTH * font), "bold", "italic"), fill="#e4e4dc",
                               tags=("watermark", '不框选'), state='disabled')

# 画图
canvas.bind('<Button-1>', leftButtonDown)  # 鼠标左键点击事件
canvas.bind('<B1-Motion>', leftButtonMove)  # 鼠标左键移动事件
canvas.bind('<ButtonRelease-1>', leftButtonUp)  # 松开左键

# 标题
canvas.create_text((WIDTH + 40) / 2, 20, text='比赛名称', font=("微软雅黑", 18), tags=('比赛名称', '不框选'))
tit_x = 0
tit_y = 0
canvas.tag_bind('比赛名称', '<Button-1>', tit_click)
canvas.tag_bind('比赛名称', '<B1-Motion>', tit_move)

# 赛事级别
canvas.create_text((WIDTH + 40) / 2, 40, text='级别赛制', font=("微软雅黑", 14), tags=('级别赛制', '不框选'))

level_x = 0
level_y = 0
canvas.tag_bind('级别赛制', '<Button-1>', level_click)
canvas.tag_bind('级别赛制', '<B1-Motion>', level_move)

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
obstacle_menu.add_command(label="树", command=tree)
obstacle_menu.add_command(label="小丑", command=joker)

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
# function_menuType.add_command(label="下载路线图", command=download)

menu_sava = ttk.Menu(menu, tearoff=0)
menu_sava.add_command(label="包含右侧赛事信息", command=save_1)
menu_sava.add_command(label="不包含右侧赛事信息", command=save_0)
function_menuType.add_cascade(label="下载路线图", menu=menu_sava)

function_menuType.add_command(label="保存路线图", command=save)
function_menuType.add_command(label="加载路线图", command=load)
function_menuType.add_command(label="删除背景", command=del_fg)

# def text():
#     width = frame_info.winfo_width()
#     height = frame_info.winfo_height()
#     x0 = frame_info.winfo_rootx() + 10  # 帧在屏幕上的左上角 x 坐标
#     y0 = frame_info.winfo_rooty()  # 帧在屏幕上的左上角 y 坐标
#     print(f"frame_info: {width}x{height}+{x0}+{y0}")
#
#
# function_menuType.add_command(label="测试", command=text)

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

# 绑定ctrl+z兼容Mac和win
win.bind("<Command-KeyPress-z>", undo)
win.bind("<Control-KeyPress-z>", undo)

win.bind('<Button-1>', unfocus_click)
win.bind('<BackSpace>', delete)

# 版本检测
t = threading.Thread(target=lambda: check_for_update(win), name='update_thread')
t.daemon = True  # 守护为True，设置True线程会随着进程一同关闭
t.start()


def processWheel(event):
    try:
        if get_obstacle().obstacle == 'diy':
            get_obstacle().zoom(event)
    except:
        pass


# 绑定滚轮事件
canvas.bind("<MouseWheel>", processWheel)

win.mainloop()
