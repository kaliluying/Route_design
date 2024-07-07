from Common import *


class Entry(ttk.Entry):
    def __init__(self, master=None, undo=True, cnf={}, **kw):
        """
        对Entry进行重写
        :param master:
        :param undo:
        :param cnf:
        :param kw:
        """
        ttk.Entry.__init__(self, master, cnf, **kw)
        self.con = None
        self.kw = kw
        self.undo_stack = []
        self.current_value = ''
        self.disabled_text = ""
        self.undo_ = undo
        self.bind('<Key>', self.on_key)
        self.bind("<Command-KeyPress-z>", self.undo if self.undo_ else '')
        self.bind("<Control-KeyPress-z>", self.undo if self.undo_ else '')

    def config(self, cnf=None, **kw):
        """
        从Entry中提取一些数据
        :param cnf:
        :param kw:
        :return:
        """
        ttk.Entry.configure(self, cnf, **kw)
        self.con = kw

    def getname(self):
        """
        获取name
        :return:
        """
        return self.kw['name']

    def on_key(self, event):
        """
        处理键盘按键事件。
        对于特定的按键事件（如回车、退格、删除），更新当前值并可能将其加入撤销栈。
        :param event: 一个包含按键信息的事件对象。
        :return:
        """
        if event.keysym in ('Return', 'KP_Enter'):
            # 当按下回车键时，将当前值加入撤销栈
            self.undo_stack.append(self.current_value)
        elif event.keysym == 'BackSpace':
            # 当按下退格键时，重置当前值为文本框当前的内容
            self.current_value = self.get()
        elif event.keysym == 'Delete':
            # 当按下删除键时，重置当前值为文本框当前的内容
            self.current_value = self.get()
        else:
            # 对于其他按键，将当前值加入撤销栈，并更新当前值为文本框当前的内容
            self.undo_stack.append(self.current_value)
            self.current_value = self.get()

    def undo(self, event):
        """
        撤销
        :param event: 一个包含按键信息的事件对象。
        :return:
        """
        if self.undo_stack:
            self.current_value = self.undo_stack.pop()
            self.delete(0, ttk.END)
            self.insert(0, self.current_value)

    def disable(self):
        """
        输入框禁用
        :return:
        """
        self.disabled_text = self.get()  # 保存禁用前的文本内容
        self['state'] = 'disabled'
        self.delete(0, ttk.END)
        self.insert(0, "已禁用")

    def enable(self):
        """
        输入框激活
        :return:
        """
        self['state'] = 'normal'
        self.delete(0, ttk.END)
        if self.disabled_text:
            self.insert(0, self.disabled_text)  # 重新设置禁用前的文本内容
        else:
            self.insert(0, "50")  # 恢复初始状态


def is_number(s):
    """
    检测字符串中是否是数字，支持正负整数，小数，中文数字如：一
    :param s: 需要检测的字符串
    :return: 返回布尔值
    """
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


def merge(m, state=1, oxer=None):
    """
    合并图片
    :param m: A B障碍的距离
    :param state: 是否为双横木
    :param oxer: 三横木
    :return: 调用函数添加行进方向并返回图片地址
    """
    img_obj = Image.open(get_one_path())
    img_obj2 = Image.open(get_one_path())
    w, h = img_obj.size
    result = Image.new(img_obj.mode, (m + 10, h))
    result.paste(img_obj, box=(0, 0))
    result.paste(img_obj2, box=(m, 0))
    if oxer == 'tirail':
        image3 = Image.open(get_one_path())
        result.paste(image3, box=(m // 2, 0))
        result.save("img/com_2.png")
        com_image = "img/com_2.png"
        return start_direction(expand(com_image, state))
    elif oxer == 'four':
        image3 = Image.open(get_one_path())
        image4 = Image.open(get_one_path())
        result.paste(image3, box=(int(m // 3), 0))
        result.paste(image4, box=(int(m // 3 * 2), 0))
        result.save("img/com_four.png")
        com_image = "img/com_four.png"
        return start_direction(expand(com_image, state))

    com_image = "img/com.png"
    result.save(com_image)
    return start_direction(expand(com_image, state))


def expand(path, state=1):
    """
    对图片进行扩边处理。

    :param path: 图片的文件路径。
    :param state: 图片是否为横幅（宽大于高）的状态，1 表示是，其他值表示否。
    :return: 扩边后图片的文件路径。
    """
    img = Image.open(path)  # 打开图片
    w, h = img.size  # 获取图片的宽和高
    l = r = t = b = 0  # 初始化各边的扩边长度

    # 根据图片宽度和高度的关系以及state参数来计算需要扩边的长度
    if w < h:
        var_ex = h - w  # 高大于宽时，计算需要在宽度方向上扩展的长度
        l = var_ex // 2  # 左边扩边长度
        r = var_ex - l  # 右边扩边长度
    elif state and w > h:
        var_ex = w - h  # 宽大于高且state为1时，计算需要在高度方向上扩展的长度
        t = var_ex // 2  # 上边扩边长度
        b = var_ex - t  # 下边扩边长度

    # 计算扩边的四个方向的值
    left_pad = l
    top_pad = t
    right_pad = r
    bottom_pad = b

    # 应用扩边操作
    padding = (left_pad, top_pad, right_pad, bottom_pad)
    img2 = ImageOps.expand(img, padding, fill=(236, 236, 236, 0))  # 扩边，填充颜色为(236, 236, 236, 0)

    # 处理图片保存的路径
    directory = os.path.dirname(path)  # 获取图片文件路径的目录部分
    file_name = os.path.basename(path)  # 获取图片文件的名称
    image_name = file_name.replace('.', '-exp.')  # 替换文件名中的点为'-exp.'，用于标识扩边后的图片
    image_path = directory + "/" + image_name  # 拼接扩边后图片的保存路径
    img2.save(image_path)  # 保存扩边后的图片

    return image_path  # 返回扩边后图片的文件路径


def start_direction(image_path):
    """
    为指定图片添加行进方向标志。

    :param image_path: 需要添加行进方向的图片的文件路径。
    :return: 返回添加了行进方向后的图片的新文件路径。
    """
    # 打开输入图片
    img1 = Image.open(image_path)
    # 获取输入图片的尺寸
    w, h = img1.size
    # 打开方向图
    img2 = Image.open(direction_image)
    # 获取方向图的尺寸
    w1, h1 = img2.size
    # 将方向图调整至与输入图片宽度相同
    img2 = img2.resize((w, h1))
    # 分离方向图的RGBA通道，为后续透明叠加做准备
    r, g, b, alpha = img2.split()
    # 将方向图透明叠加在输入图片的中央偏上位置
    img1.paste(img2, (0, h // 2 - 5), alpha)
    # 获取输入图片的目录路径和文件名
    directory = os.path.dirname(image_path)
    file_name = os.path.basename(image_path)
    # 生成添加行进方向后图片的新文件名
    image_name = file_name.replace('.', '-dir.')
    # 拼接生成新图片的完整路径
    image_path = directory + "/" + image_name
    # 保存处理后的图片
    img1.save(image_path)
    # 返回新图片的路径
    return image_path


def combination(m1, m2, m3):
    """
    AB组合障碍
    :param m1: 障碍间距
    :param m2: 障碍间距
    :param m3: 障碍间距
    :return: 调用函数添加行进方向并返回图片地址
    """
    img_obj = Image.open(get_one_path())
    img_obj2 = Image.open(get_one_path())
    img_obj3 = Image.open(get_one_path())
    img_obj4 = Image.open(get_one_path())

    result = Image.new(img_obj.mode, (m1 + m2 + m3 + 20, 40))
    result.paste(img_obj, box=(0, 0))
    result.paste(img_obj2, box=(m1 + 5, 0))
    result.paste(img_obj3, box=(m1 + m2 + 10, 0))
    result.paste(img_obj4, box=(m1 + m2 + m3 + 15, 0))
    result.save("img/com_3.png")
    com_image = "img/com_3.png"
    return start_direction(expand(com_image))


def com_abc(m1=0, m2=0, m3=0, m4=0, m5=0):
    """
    ABC组合障碍
    :param m1: 障碍间距
    :param m2: 障碍间距
    :param m3: 障碍间距
    :param m4: 障碍间距
    :param m5: 障碍间距
    :return: 调用函数添加行进方向并返回图片地址
    """
    img_obj1 = img_obj2 = img_obj3 = img_obj4 = img_obj5 = img_obj6 = Image.open(get_one_path())
    result = Image.new(img_obj1.mode, (m1 + m2 + m3 + m4 + m5 + 30, 40))

    if m1:
        result.paste(img_obj1, box=(m1 + 5, 0))
    result.paste(img_obj2, box=(0, 0))
    if m3:
        result.paste(img_obj3, box=(m1 + m2 + 10, 0))
    result.paste(img_obj4, box=(m1 + m2 + m3 + 15, 0))
    if m5:
        result.paste(img_obj5, box=(m1 + m2 + m3 + m4 + 20, 0))
    result.paste(img_obj6, box=(m1 + m2 + m3 + + m4 + m5 + 25, 0))

    result.save("img/com_abc.png")
    com_image = "img/com_abc.png"
    return start_direction(expand(com_image))


def merge_ab(state, m1=0, m2=0):
    """
    都是双横木时
    :param state:
    :param m1:
    :param m2:
    :return:
    """
    if state == 1:
        path = start_direction(expand(get_one_path()))
    if state == 2:
        path = start_direction(merge(5))
    img_obj = Image.open(path)
    img_obj2 = Image.open(path)
    var = 45
    if m2:
        var = 50
    result = Image.new(img_obj.mode, (m1 + m2 + var, 40))
    result.paste(img_obj, box=(0, 0))
    result.paste(img_obj2, box=(m1 + 5, 0))
    if m2:
        image3 = Image.open(path)
        result.paste(image3, box=(m1 + m2 + 10, 0))
        result.save("img/com_abc.png")
        com_image = "img/com_abc.png"
        return com_image
    com_image = "img/com_ab.png"
    result.save(com_image)
    return com_image


def oxer_obs_ab(stare_a, state_b, state_c=0, a=0, b=0, c=0, a_b=30, b_c=0):
    """
    ABC组合障碍是否为双横木更新
    :param stare_a: 障碍A是否为双横木
    :param state_b: 障碍B是否为双横木
    :param state_c: 障碍C是否为双横木
    :param a:
    :param b:
    :param c:
    :param a_b:
    :param b_c:
    :return:
    """
    a_img = one_exp_dir_path
    b_img = one_exp_dir_path
    c_img = one_exp_dir_path
    if stare_a == "1":
        a_img = merge(a + 5)
    if state_b == "1":
        b_img = merge(b + 5)
    if state_c == "1":
        c_img = merge(c + 5)
    var = 45
    if state_c:
        var = 50
    img_obj = Image.open(a_img)
    img_obj2 = Image.open(b_img)
    result = Image.new(img_obj.mode, (a + b + c + a_b + b_c + var, 40))
    result.paste(img_obj, box=(0, 0))
    result.paste(img_obj2, box=(a_b + 5, 0))
    if state_c:
        image3 = Image.open(c_img)
        result.paste(image3, box=(a_b + b_c + 10, 0))
        result.save("img/oxer_obs_abc.png")
        com_image = "img/oxer_obs_abc.png"
        result.save(com_image)
        return com_image
    com_image = "img/oxer_obs_ab.png"
    result.save(com_image)
    return com_image


def oxer_obs_abc(a=0, b=0, c=0, a_b=30, b_c=0):
    """

    :param a:
    :param b:
    :param c:
    :param a_b:
    :param b_c:
    :return:
    """
    a_img = merge(a if a else 0, state=0)
    img_obj = Image.open(a_img)
    b_img = merge(b if b else 0, state=0)
    img_obj2 = Image.open(b_img)
    c_img = merge(c if c else 0, state=0)
    image3 = Image.open(c_img)
    result = Image.new(img_obj.mode, (a + b + c + a_b + b_c + 55, 40))
    result.paste(img_obj, box=(0, 0))
    result.paste(img_obj2, box=(a + a_b, 0))
    result.paste(image3, box=(a + b + a_b + b_c, 0))
    result.save("img/obs_abc.png")
    com_image = "img/obs_abc.png"
    result.save(com_image)
    return com_image


def obs_ab(a=0, b=0, a_b=30):
    """
    :param a:
    :param b:
    :param a_b:
    :return:
    """
    a_img = merge(a if a else 0, state=0)
    img_obj = Image.open(a_img)
    b_img = merge(b if b else 0, state=0)
    img_obj2 = Image.open(b_img)
    result = Image.new(img_obj.mode, (a + b + a_b + 50, 40))
    result.paste(img_obj, box=(0, 0))
    result.paste(img_obj2, box=(a + a_b, 0))
    # result.paste(img_obj2, box=(a + a_b + (10 if a else 5), 0))
    # result.save("img/obs_ab.png")
    com_image = "img/obs_ab.png"
    result.save(com_image)
    return com_image


def water_wh(w, h):
    """
    水障调整
    :param w:
    :param h:
    :return:
    """
    img = Image.open(water_barrier_iamge)
    img = img.resize((w, h))
    img.save("img/water_wh.png")
    return start_direction(expand("img/water_wh.png"))


def live_two_tool(path='img/liverpool3.png'):
    """
    利物浦单横木变双横木
    :return:
    """
    img = Image.open(path)
    img2 = Image.open('img/one.png')
    w, h = img.size
    result = Image.new(img.mode, (w, h))
    result.paste(img, box=(0, 0))
    result.paste(img2, box=(0, 0))
    result.paste(img2, box=(w - 5, 0))
    result.save("img/live_two.png")
    return start_direction(expand("img/live_two.png"))


def live_one_tool(path=get_live_path()):
    img = Image.open(path)
    img2 = Image.open('img/one.png')
    w, h = img.size
    result = Image.new(img.mode, (w, h))
    result.paste(img, box=(0, 0))
    result.paste(img2, box=(int(w / 2 - 1), 0))
    result.save("img/live_one.png")
    return start_direction(expand("img/live_one.png"))


def live_edit(w, h):
    img = Image.open(get_live_path())
    img = img.resize((w, h))
    img.save("img/live_wh.png")
    id = get_live()
    if id == '1' or id == 1:
        return live_two_tool("img/live_wh.png")
    elif id == 0 or id == '0':
        a = live_one_tool("img/live_wh.png")
        return a


def remove_from_edit():
    """
    删除旋转、备注编辑容器
    :return:
    """
    for i in frame_edit.winfo_children():
        for j in i.winfo_children():
            for d in j.winfo_children():
                d.destroy()


def remove_from_not_com():
    """
    删除除功能容器的容器
    :return:
    """
    for i in frame_function.winfo_children():
        if i.winfo_name() == '工作模块':
            for j in i.winfo_children():
                if j.winfo_name() != '功能容器':
                    j.destroy()

        # else:
        #     i.destroy()


def calculate_bezier_length(id, pre_id=None, num_points=100, start=True):
    """
    计算贝塞尔曲线长度
    :param id: 当前点的id
    :param pre_id: 上一点的id
    :param num_points: 计算曲线长度的点数
    :param start: 加还是减
    :return:
    """
    global px

    def bezier(t, p0, p1, p2):
        return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
                (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1])

    x1, y1, ctrl_x, ctrl_y, x2, y2 = canvas.coords(id)
    p0 = (x1, y1)
    p1 = (ctrl_x, ctrl_y)
    p2 = (x2, y2)
    try:
        pre_x1, pre_y1, pre_ctrl_x, pre_ctrl_y, pre_x2, pre_y2 = canvas.coords(pre_id)
        pre_p0 = (pre_x1, pre_y1)
        pre_p1 = (pre_ctrl_x, pre_ctrl_y)
        pre_p2 = (pre_x2, pre_y2)

        pre_length = 0
        pre_point = pre_p0

        for i in range(1, num_points + 1):
            t = i / num_points
            current_point = bezier(t, pre_p0, pre_p1, pre_p2)
            segment_length = math.sqrt((current_point[0] - pre_point[0]) ** 2 + (current_point[1] - pre_point[1]) ** 2)
            pre_length += segment_length
            pre_point = current_point
    except:
        print("计算前一段曲线长度失败")
        pre_length = 0

    length = 0
    prev_point = p0

    for i in range(1, num_points + 1):
        t = i / num_points
        current_point = bezier(t, p0, p1, p2)
        segment_length = math.sqrt((current_point[0] - prev_point[0]) ** 2 + (current_point[1] - prev_point[1]) ** 2)
        length += segment_length
        prev_point = current_point

    if start:
        px += length / 10 - pre_length / 10
    else:
        px -= length / 10 - pre_length / 10
    canvas.itemconfig('实时路线', text="%.2fm" % px)


def compute_arc_length(arc):
    """
    计算弧线长度
    :param arc:
    :return:
    """

    def bezier(t, p0, p1, p2):
        return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0],
                (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1])

    num_points = 100
    coords = canvas.coords(arc)
    x1, y1, ctrl_x, ctrl_y, x2, y2 = coords
    p0 = (x1, y1)
    p1 = (ctrl_x, ctrl_y)
    p2 = (x2, y2)

    length = 0
    prev_point = p0

    for i in range(1, num_points + 1):
        t = i / num_points
        current_point = bezier(t, p0, p1, p2)
        segment_length = math.sqrt(
            (current_point[0] - prev_point[0]) ** 2 + (current_point[1] - prev_point[1]) ** 2)
        length += segment_length
        prev_point = current_point

    return length


def update_arc_px(cur, pre):
    global px
    px += (cur - pre) / 10
    canvas.itemconfig('实时路线', text="%.2fm" % px)


def update_px(length, start=True, clear=False):
    global px
    if clear:
        canvas.itemconfig('实时路线', text="%.2fm" % 0)
        return
    if start:
        px += length
    else:
        px -= length

    canvas.itemconfig('实时路线', text="%.2fm" % px)


# 行进方向
direction_image = "img/direction2.png"
# 组合障碍
com_image = "img/com.png"
# 单横木行进方向
one_exp_dir_path = start_direction(expand(get_one_path()))
# 双横木行进方向
oxer_exp_dir_path = "img/oxer-exp-dir.png"
