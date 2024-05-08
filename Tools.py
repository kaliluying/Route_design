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

    def getstate(self):
        """
        获取状态
        :return:
        """
        try:
            try:
                return self.con['state']
            except:
                return self.kw['state']
        except:
            return ''

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
        self.insert(0, self.disabled_text)  # 重新设置禁用前的文本内容


def is_number(s):
    """
    检测字符串中是否是数字，支持正负整数，小数，中文数字如：一
    :param s:需要检测的字符串
    :return:
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


def merge(m, m1=0, state=1):
    """
    合并图片
    :param m:A B障碍的距离
    :param m1:B C障碍的距离
    :param state:是否为双横木
    :return:调用函数添加行进方向并返回图片地址
    """
    img_obj = Image.open(get_one_path())
    img_obj2 = Image.open(get_one_path())
    w, h = img_obj.size
    result = Image.new(img_obj.mode, (m + m1 + 10, h))
    result.paste(img_obj, box=(0, 0))
    if m1:
        a = 10
    else:
        a = 5
    result.paste(img_obj2, box=(m + m1 - a, 0))
    if m1:
        image3 = Image.open(get_one_path())
        result.paste(image3, box=(m - 5, 0))
        result.save("img/com_2.png")
        com_image = "img/com_2.png"
        return start_direction(expand(com_image, state))
    com_image = "img/com.png"
    result.save(com_image)
    return start_direction(expand(com_image, state))


def expand(path, state=1):
    """
    图片扩展
    :param path:图片地址
    :param state:是否为双横木
    :return:
    """
    img = Image.open(path)
    w, h = img.size
    l = r = t = b = 0
    if w < h:
        var_ex = h - w
        l = var_ex // 2
        r = var_ex - l
    elif state and w > h:
        var_ex = w - h
        t = var_ex // 2
        b = var_ex - t

    left_pad = l
    top_pad = t
    right_pad = r
    bottom_pad = b

    padding = (left_pad, top_pad, right_pad, bottom_pad)
    img2 = ImageOps.expand(img, padding, fill=(236, 236, 236, 0))
    directory = os.path.dirname(path)
    file_name = os.path.basename(path)
    image_name = file_name.replace('.', '-exp.')
    image_path = directory + "/" + image_name
    img2.save(image_path)
    return image_path


def start_direction(image_path):
    """
    添加行进方向
    :param image_path:
    :return:返回图片地址
    """
    img1 = Image.open(image_path)
    w, h = img1.size
    img2 = Image.open(direction_image)
    w1, h1 = img2.size
    img2 = img2.resize((w, h1))
    r, g, b, alpha = img2.split()
    img1.paste(img2, (0, h // 2 - 5), alpha)
    directory = os.path.dirname(image_path)
    file_name = os.path.basename(image_path)
    image_name = file_name.replace('.', '-dir.')
    image_path = directory + "/" + image_name
    img1.save(image_path)
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
    AB组合障碍
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

    :param state:
    :param m1:
    :param m2:
    :return:
    """
    if state == 1:
        path = start_direction(expand(get_one_path()))
    if state == 2:
        path = start_direction(merge(10))
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

    :param stare_a:
    :param state_b:
    :param state_c:
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
    result = Image.new(img_obj.mode, (a + b + c + a_b + b_c + 50, 40))
    result.paste(img_obj, box=(0, 0))
    result.paste(img_obj2, box=(a + a_b + (10 if a else 5), 0))
    result.paste(image3, box=(a + b + a_b + b_c + (10 if a else 5) + (10 if b else 5), 0))
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
    result = Image.new(img_obj.mode, (a + b + a_b + 45, 40))
    result.paste(img_obj, box=(0, 0))
    result.paste(img_obj2, box=(a + a_b + (10 if a else 5), 0))
    result.save("img/obs_ab.png")
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


# 删除旋转、备注编辑容器
def remove_from_edit():
    for i in frame_edit.winfo_children():
        for j in i.winfo_children():
            for d in j.winfo_children():
                d.destroy()


# 删除除功能容器的容器
def remove_from_not_com():
    for i in frame_function.winfo_children():
        if i.winfo_name() == '工作模块':
            for j in i.winfo_children():
                if j.winfo_name() == '功能容器':
                    pass
                else:
                    j.destroy()
        # else:
        #     i.destroy()


# 行进方向
direction_image = "img/direction2.png"
# 组合障碍
com_image = "img/com.png"
# 单横木行进方向
one_exp_dir_path = start_direction(expand(get_one_path()))
# 双横木行进方向
oxer_exp_dir_path = "img/oxer-exp-dir.png"
