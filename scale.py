import Commom
from Tools import is_number, merge, oxer_obs_abc, obs_ab, remove_from_edit
from Commom import *

# 当前标签
current_tag = None
# 线段标签
line_tag = None


def set_cur(cur):
    global current_tag, line_tag
    current_tag = cur


def set_line(line):
    global line_tag
    line_tag = line


def get_cur():
    return current_tag, line_tag


def set_frame_stare(frame_stare):
    global current_frame_stare
    current_frame_stare = frame_stare


def get_frame_stare():
    return current_frame_stare


class T:
    def __init__(self, app, index):
        self.tag = None
        self.startx = 200
        self.starty = 100
        self.current_x = 200
        self.current_y = 100
        self.angle = 0
        self.app = app
        self.index = str(index)
        self.line_tag = None

    def mousedown(self, tag, event):
        """
        鼠标左键按下
        :param tag:
        :param event:
        :return:
        """
        self.app.delete('choice')
        set_frame_stare(False)
        if what.get() == 0:
            try:
                self.startx = event.x
                self.starty = event.y
            except:
                self.startx = event[0]
                self.starty = event[1]
            self.tag = tag
            set_cur(tag)
            self.app.lift(self.tag)

    def drag(self, tag, event):
        """
        鼠标拖动
        :param tag:
        :param event:
        :return:
        """
        global choice_tup
        if what.get() == 0 and not choice_tup:
            self.app.move(tag, event.x - self.startx, event.y - self.starty)
            if self.line_tag:
                self.app.move(self.line_tag, event.x - self.startx, event.y - self.starty)
            self.current_x += event.x - self.startx
            self.current_y += event.y - self.starty

            self.startx = event.x
            self.starty = event.y

    # def pop(self, tag, event):
    #     self.app.delete(tag)
    def mouseup(self, event):
        set_frame_stare(True)


class CreateTxt(T):

    def create_txt(self, txt):
        tag = "txt" + self.index
        text = self.app.create_text(self.startx, self.starty, text=txt, tags=tag)
        self.app.tag_bind(tag, "<Button-1>", partial(self.mousedown, tag))
        self.app.tag_bind(tag, "<B1-Motion>", partial(self.drag, text))
        # self.app.tag_bind(tag, "<Button-2>", partial(self.pop, tag))
        self.app.tag_bind(tag, "<ButtonRelease-1>", self.mouseup)


class CreateParameter(T):
    def create_parameter(self, txt):
        tag = "parameter" + self.index
        text = self.app.create_text(self.startx, self.starty, text=txt, tags=('parameter', tag))
        self.app.tag_bind(tag, "<Button-1>", partial(self.mousedown, tag))
        self.app.tag_bind(tag, "<B1-Motion>", partial(self.drag, text))
        # self.app.tag_bind(tag, "<Button-2>", partial(self.pop, tag))
        self.app.tag_bind(tag, "<ButtonRelease-1>", self.mouseup)


class CreateImg(T):
    def __init__(self, app, index, img_path, obstacle=None):
        super(CreateImg, self).__init__(app, index)
        self.frame_button = None
        self.frame_input = None
        self.img_path = img_path
        self.img_obj = Image.open(self.img_path)
        self.temp_path = None
        self.img_file = None
        self.obstacle = obstacle
        self.focus = focus
        self.info = []
        self.com_info = {}
        self.state = {}
        self.name = ''
        self.state_line = 0

    def create_img(self):
        self.tag = "img" + self.index
        self.img_file = ImageTk.PhotoImage(self.img_obj)
        img_id = self.app.create_image(self.startx, self.starty, image=self.img_file,
                                       tag=self.tag)
        self.app.tag_bind(self.tag, "<Button-1>", partial(self.mousedown, self.tag))
        self.app.tag_bind(self.tag, "<B1-Motion>", partial(self.drag, img_id))
        # self.app.tag_bind(self.tag, "<Button-2>", partial(self.pop, self.tag))
        self.mousedown(self.tag, [200, 100])
        set_frame_stare(True)
        self.app.tag_bind(self.tag, "<ButtonRelease-1>", self.mouseup)

    def mousedown(self, tag, event):
        """
        鼠标左键点击事件
        :param tag:
        :param event:
        :return:
        """
        T.mousedown(self, tag, event)
        self.butt()
        if self.obstacle in ["oxer", "tirail", "combination_ab", "combination_abc"]:
            self.frame_input, self.frame_button = self.focus.update(self, self.obstacle, info=self.info,
                                                                    state=self.state, com_info=self.com_info)
            button = self.frame_button.winfo_children()[0]
            button.config(command=self.update_img)
        else:
            if frame_function.winfo_children()[-2].winfo_name() == '障碍编辑容器':
                frame_function.winfo_children()[-2].destroy()
        if self.obstacle in ["oxer", "tirail", "combination_ab", "combination_abc", 'monorail']:
            if self.state_line:
                self.state_line = 0
                self.app.delete(self.line_tag)
            else:
                self.state_line = 1

                # 辅助线
                self.guide()
                set_line(self.line_tag)

    def guide(self):
        if 90 < self.angle < 180 or 270 < self.angle <= 359:
            ang = 90 - self.angle % 90
        elif 180 < self.angle < 270:
            ang = self.angle % 180
        else:
            ang = self.angle

        if self.angle == 90:
            x1 = x2 = self.current_x
            y1 = self.current_y - 150
            y2 = self.current_y + 150

            self.line_tag = self.app.create_line(x1, y1, x2, y2, dash=(5, 3))
            return
        elif self.angle == 180:
            y1 = y2 = self.current_y
            x1 = self.current_x - 150
            x2 = self.current_x + 150
            self.line_tag = self.app.create_line(x1, y1, x2, y2, dash=(5, 3))
            return

        k = math.tan(self.angle * math.pi / 180)
        b = -self.current_y - k * self.current_x
        if ang <= 45:
            x1 = self.current_x - 150
            y1 = -(((self.current_x - 150) * k) + b)
            x2 = self.current_x + 150
            y2 = -(((self.current_x + 150) * k) + b)
        elif ang > 45:
            y1 = self.current_y - 150
            y2 = self.current_y + 150
            m1 = (y2 - b) / k
            m2 = (y1 - b) / k
            m = (m1 + m2) / 2
            n = m - self.current_x
            x1 = m1 - n
            x2 = m2 - n

        # k = math.tan(self.angle * math.pi / 180)
        # b = -self.current_y - k * self.current_x
        # x1 = self.current_x - 100
        # y1 = -(((self.current_x - 100) * k) + b)
        # x2 = self.current_x + 100
        # y2 = -(((self.current_x + 100) * k) + b)

        self.line_tag = self.app.create_line(x1, y1, x2, y2, dash=(5, 3))

    def update_img(self):
        """
        从输入框中获取值更新图片
        :return:
        """
        self.info.clear()
        for i in self.frame_input.winfo_children():
            if self.obstacle == "combination_ab" or self.obstacle == "combination_abc":
                if is_number(i.get()):
                    self.com_info[i.getname()] = i.get()
                    self.state[i.getname()] = i.getstate()
                    if self.state[i.getname()] == "disabled":
                        self.com_info[i.getname()] = "0"
                    continue
                elif i.get() == '':
                    self.com_info[i.getname()] = '0'
                    self.state[i.getname()] = i.getstate()
                    continue
                else:
                    messagebox.showerror("错误", "请输入数字")
                    i.delete(0, 'end')
                    return
            if is_number(i.get()):
                self.info.append(i.get())
            elif i.get() == '':
                self.info.append('1')
            else:
                messagebox.showerror("错误", "请输入数字")
                i.delete(0, 'end')
                return
        if self.obstacle == "oxer":
            val = int(float(self.info[0]) * 10)
            self.img_updata(val)
        elif self.obstacle == "tirail":
            val_a = float(self.info[0]) * 10
            val_b = float(self.info[1]) * 10
            self.img_updata(val_a, val_b)
        elif self.obstacle == "combination_ab":
            temp = {}
            for key, val in self.com_info.items():
                if key.count('_') == 2 and val != '0':
                    temp[key] = float(val) * 10
                elif key.count('_') == 1 and val != '0':
                    temp[key] = float(val) / 10
                else:
                    temp[key] = 0
            a, a_b, b = temp.values()
            a, a_b, b = round(a), round(a_b), round(b)
            self.img_path = obs_ab(a, b, a_b)
            self.img = Image.open(self.img_path)
            self.temp_path = ImageTk.PhotoImage(self.img)
            self.app.itemconfig(self.tag, image=self.temp_path)
        elif self.obstacle == "combination_abc":
            temp = {}
            for key, val in self.com_info.items():
                if key.count('_') == 2 and val != '0':
                    temp[key] = (int(val) * 10)
                elif key.count('_') == 1 and val != '0':
                    temp[key] = (int(val) / 10)
                else:
                    temp[key] = 0
            a, a_b, b, b_c, c = temp.values()
            a, a_b, b, b_c, c = int(a), int(a_b), int(b), int(b_c), int(c)
            self.img_path = oxer_obs_abc(a, b, c, a_b, b_c)
            self.img = Image.open(self.img_path)
            self.temp_path = ImageTk.PhotoImage(self.img)
            self.app.itemconfig(self.tag, image=self.temp_path)
        self.rotate(self.tag, self.angle)

    def img_updata(self, m1, m2=0.0):
        m1 = int(m1)
        m2 = int(m2)
        self.img_path = merge(m1, m1=m2)
        self.img = Image.open(self.img_path)
        self.temp_path = ImageTk.PhotoImage(self.img)
        self.app.itemconfig(self.tag, image=self.temp_path)

    def create_frame(self):
        # 旋转、备注编辑主容器
        frame_edit = tk.Frame(frame_function, name='旋转、备注')
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

    def butt(self):
        """
        按钮
        :return:
        """
        self.create_frame()
        remove_from_edit()

        tk.Label(frame_focus_x_ladel, text="旋转： ", font=("微软雅黑", 15)).pack()
        self.var = tk.StringVar()
        self.var.set(str(int(self.angle)))
        tk.Entry(frame_focus_x_ent, textvariable=self.var, width=5).pack()
        tk.Button(frame_focus_x_but, text="确认", command=partial(self.rotate, self.tag, self.var)).pack()
        tk.Label(frame_focus_z_ladel, text="备注： ", font=("微软雅黑", 15)).pack()
        var_name = tk.StringVar(value=self.name)
        tk.Entry(frame_focus_z_ent, textvariable=var_name, width=5).pack()
        tk.Button(frame_focus_z_but, text="确认", command=partial(self.set_name, var_name)).pack()

    def set_state(self):
        self.app.lower(self.tag)
        self.app.lower("watermark")

    def set_name(self, name):
        self.name = name.get()

    def drag(self, tag, event):
        """
        拖动旋转
        :param tag:
        :param event:
        :return:
        """
        T.drag(self, tag, event)
        if what.get() == 3:
            x = event.x - self.startx
            y = event.y - self.starty
            if x != 0 and y != 0:
                if (x < 0 and y >= 0) or (x < 0 and y < 0):
                    self.angle += (math.sqrt(x * x + y * y))
                elif (y < 0 and x >= 0) or (y > 0 and x > 0):
                    self.angle += -(math.sqrt(x * x + y * y))
            else:
                self.angle += (x + y)
            self.rotate(tag, self.angle)
            self.startx = event.x
            self.starty = event.y

    def rotate(self, id, var):
        """
        旋转
        :param id:
        :param state:
        :return:
        """
        try:
            angle = int(var.get())
        except:
            angle = var
        angle = angle % 360
        self.angle = angle
        self.img = self.rotate_bound(angle)
        self.temp_path = ImageTk.PhotoImage(self.img)
        self.app.itemconfig(id, image=self.temp_path)
        self.var.set(str(int(angle)))
        set_cur(self.tag)

        if self.obstacle in ["oxer", "tirail", "combination_ab", "combination_abc",
                             'monorail'] and self.state_line:
            self.app.delete(self.line_tag)
            self.guide()
            set_line(self.line_tag)

    def rotate_bound(self, angle):
        """
        旋转图片
        :param angle: 旋转角度 正为逆时针旋转，反之
        :return: 返回图对象
        """
        img = Image.open(self.img_path)
        img2 = img.convert('RGBA')
        img2 = img2.rotate(angle, expand=True)
        return img2
