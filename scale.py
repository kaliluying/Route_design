import Commom
from Tools import is_number, merge, oxer_obs_abc, obs_ab, remove_from_edit, water_wh, live_edit, Entry
from Commom import *


class T:
    all_instances = []

    def __init__(self, app, index):
        self.__class__.all_instances.append(self)
        self.tag = None
        self.startx = 160
        self.starty = 25
        self.current_x = 160
        self.current_y = 25
        self.angle = 0
        self.temp_angle = 0
        self.app = app
        self.index = str(index)
        self.line_tag = None
        self.id = None

    def mousedown(self, tag, event):
        """
        鼠标左键按下
        :param tag:
        :param event:
        :return:
        """
        global choice_tup
        set_frame_stare(False)
        try:
            if choice_tup and not (min(choice_tup[0], choice_tup[2]) < event.x < max(choice_tup[0], choice_tup[2])
                                   and min(choice_tup[1], choice_tup[3]) < event.y < max(choice_tup[1], choice_tup[3])):
                self.app.delete('choice')
                choice_tup.clear()
                self.app.dtag('choice_start', 'choice_start')
        except Exception as e:
            print(e)
            logging.warning(e)
        if what.get() == 0:
            try:
                self.startx = event.x
                self.starty = event.y
                move_x.set(event.x)
                move_y.set(event.y)
            except:
                self.startx = event[0]
                self.starty = event[1]
            self.tag = tag
            set_cur(self.id)
            self.app.lift(self.tag)

    def drag(self, tag, event):
        """
        鼠标拖动
        :param tag:
        :param event:
        :return:
        """
        # global choice_tup
        if what.get() == 0 and not choice_tup:
            set_frame_stare(False)
            self.app.move(tag, event.x - self.startx, event.y - self.starty)
            if self.line_tag:
                self.app.move(self.line_tag, event.x - self.startx, event.y - self.starty)
            self.current_x += event.x - self.startx
            self.current_y += event.y - self.starty

            self.startx = event.x
            self.starty = event.y

    def mouseup(self, event):
        # set_frame_stare(True)
        dx = event.x - move_x.get()
        dy = event.y - move_y.get()
        if dx or dy:
            stack.append(('移动', (self.id,), (dx, dy)))
        if what.get() == 3 and self.temp_angle != self.angle:
            rotate_.append(self.angle)
            stack.append(("旋转", self))


class CreateTxt(T):

    def create(self, txt):
        self.tag = "txt-" + self.index
        text = self.app.create_text(self.startx, self.starty, text=txt, tags=self.tag)
        self.id = text
        stack.append(('创建', text))
        self.app.tag_bind(self.tag, "<Button-1>", partial(self.mousedown, self.tag))
        self.app.tag_bind(self.tag, "<B1-Motion>", partial(self.drag, text))
        # self.app.tag_bind(tag, "<Button-2>", partial(self.pop, tag))
        self.app.tag_bind(self.tag, "<ButtonRelease-1>", self.mouseup)
        self.mousedown(self.tag, [200, 100])


class CreateParameter(T):
    def create(self, txt):
        self.tag = "parameter-" + self.index
        text = self.app.create_text(self.startx, self.starty, text=txt, tags=('parameter', self.tag))
        self.id = text
        stack.append(('创建', text))
        self.app.tag_bind(self.tag, "<Button-1>", partial(self.mousedown, self.tag))
        self.app.tag_bind(self.tag, "<B1-Motion>", partial(self.drag, text))
        # self.app.tag_bind(tag, "<Button-2>", partial(self.pop, tag))
        self.app.tag_bind(self.tag, "<ButtonRelease-1>", self.mouseup)
        self.mousedown(self.tag, [200, 100])


class CreateImg(T):
    def __init__(self, app, index, img_path, obstacle=None):
        super(CreateImg, self).__init__(app, index)
        self.var = None
        self.img = None
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

    def create(self):
        self.tag = "img-" + self.index
        self.img_file = ImageTk.PhotoImage(self.img_obj)
        img_id = self.app.create_image(self.startx, self.starty, image=self.img_file,
                                       tag=self.tag)
        self.id = img_id
        stack.append(('创建', img_id))
        self.app.tag_bind(self.tag, "<Button-1>", partial(self.mousedown, self.tag))
        self.app.tag_bind(self.tag, "<B1-Motion>", partial(self.drag, img_id))
        # self.app.tag_bind(self.tag, "<Button-2>", partial(self.pop, self.tag))
        self.mousedown(self.tag, [200, 100])
        set_frame_stare(True)
        self.app.tag_bind(self.tag, "<ButtonRelease-1>", self.mouseup)
        # no_what.set(0)
        # set_color()

    def mousedown(self, tag, event):
        """
        鼠标左键点击事件
        :param tag:
        :param event:
        :return:
        """
        T.mousedown(self, tag, event)
        self.butt()
        if what.get() == '3':
            self.temp_angle = self.angle
        if self.obstacle in ["oxer", "tirail", "combination_ab", "combination_abc", 'water', 'live']:
            self.frame_input, self.frame_button = self.focus.update(self, self.obstacle, info=self.info,
                                                                    state=self.state, com_info=self.com_info)
            button = self.frame_button.winfo_children()[0]
            button.config(command=self.update_img)
        else:
            if frame_function.winfo_children()[0].winfo_children()[1].winfo_name() == '障碍编辑容器':
                frame_function.winfo_children()[0].winfo_children()[1].destroy()

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
            elif self.obstacle == 'live':
                if is_number(i.get()):
                    self.com_info[i.winfo_name()] = i.get()
                    self.state[i.winfo_name()] = i.getstate()
                    if self.state[i.winfo_name()] == "disabled":
                        self.com_info[i.winfo_name()] = "0"
                    continue
                elif i.get() == '':
                    self.com_info[i.winfo_name()] = '0'
                    self.state[i.winfo_name()] = i.getstate()
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
                    temp[key] = float(val) * 10
                elif key.count('_') == 1 and val != '0':
                    temp[key] = float(val) / 10
                else:
                    temp[key] = 0
            a, a_b, b, b_c, c = temp.values()
            a, a_b, b, b_c, c = int(a), int(a_b), int(b), int(b_c), int(c)
            self.img_path = oxer_obs_abc(a, b, c, a_b, b_c)
            self.img = Image.open(self.img_path)
            self.temp_path = ImageTk.PhotoImage(self.img)
            self.app.itemconfig(self.tag, image=self.temp_path)
        elif self.obstacle == 'water':
            w = int(float(self.info[0]) * 10)
            h = int(float(self.info[1]) * 10)
            self.img_path = water_wh(w, h)
            self.img = Image.open(self.img_path)
            self.temp_path = ImageTk.PhotoImage(self.img)
            self.app.itemconfig(self.tag, image=self.temp_path)
        elif self.obstacle == 'live':
            w = int(float(self.com_info['water_w_ent']) * 10)
            h = int(float(self.com_info['water_h_ent']) * 10)
            self.img_path = live_edit(w, h)
            self.img = Image.open(self.img_path)
            self.temp_path = ImageTk.PhotoImage(self.img)
            self.app.itemconfig(self.tag, image=self.temp_path)
        self.to_rotate(self.tag, self.angle)

    def img_updata(self, m1, m2=0.0):
        m1 = int(m1)
        m2 = int(m2)
        self.img_path = merge(m1, m1=m2)
        self.img = Image.open(self.img_path)
        self.temp_path = ImageTk.PhotoImage(self.img)
        self.app.itemconfig(self.tag, image=self.temp_path)

    @staticmethod
    def create_frame():
        # 旋转、备注编辑主容器
        frame_edit = ttk.Frame(frame_job, name='旋转、备注')
        frame_edit.pack()

        # 旋转容器
        frame_x = ttk.Frame(frame_edit, name='旋转')
        frame_x.pack()
        frame_focus_x_ladel = ttk.Frame(frame_x)
        frame_focus_x_ent = ttk.Frame(frame_x)
        frame_focus_x_but = ttk.Frame(frame_x)
        frame_focus_x_but.pack(side='bottom')
        frame_focus_x_ladel.pack(side='left')
        frame_focus_x_ent.pack(side='right')

        # 备注容器
        frame_z = ttk.Frame(frame_edit, name='备注')
        frame_z.pack()
        frame_focus_z_ladel = ttk.Frame(frame_z)
        frame_focus_z_ent = ttk.Frame(frame_z)
        frame_focus_z_but = ttk.Frame(frame_z)
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

        ttk.Label(frame_focus_x_ladel, text="旋转： ", font=("微软雅黑", 15)).pack()
        self.var = ttk.StringVar()
        self.var.set(str(int(self.angle)))
        Entry(frame_focus_x_ent, textvariable=self.var, width=5, undo=True).pack()

        ttk.Button(frame_focus_x_but, text="确认", command=partial(self.to_rotate, self.tag, self.var)).pack()
        ttk.Label(frame_focus_z_ladel, text="备注： ", font=("微软雅黑", 15)).pack()
        var_name = ttk.StringVar(value=self.name if self.name else self.tag)
        Entry(frame_focus_z_ent, textvariable=var_name, width=5).pack()
        ttk.Button(frame_focus_z_but, text="确认", command=partial(self.set_name, var_name)).pack()
        w = 5 if sys_name == 'Darwin' else 10
        ttk.Button(frame_aux_com_rig, text='障碍辅助线', command=self.bar_aux, name='障碍辅助线', width=w).pack()

    def bar_aux(self):
        # if self.obstacle in ["oxer", "tirail", "combination_ab", "combination_abc", 'monorail']:
        if self.state_line:
            self.state_line = 0
            self.app.delete(self.line_tag)
        else:
            self.state_line = 1

            # 辅助线
            bbox = self.app.bbox(self.tag)
            self.current_x = bbox[0] + ((bbox[2] - bbox[0]) / 2)
            self.current_y = bbox[1] + ((bbox[3] - bbox[1]) / 2)
            self.guide()
            set_line(self.line_tag)

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
            # if x != 0 and y != 0:
            #     if (x < 0 and y >= 0) or (x < 0 and y < 0):
            #         self.angle += (math.sqrt(x * x + y * y))
            #     elif (y < 0 and x >= 0) or (y > 0 and x > 0):
            #         self.angle += -(math.sqrt(x * x + y * y))
            # else:
            #     self.angle += (x + y)
            if x < 0:
                x = -x
            self.angle += x / 15
            self.to_rotate(tag, self.angle, state=False)
            # self.startx = event.x
            # self.starty = event.y

    def to_rotate(self, id, var, state=True):
        try:
            angle = int(var.get())
        except:
            angle = var
        angle = angle % 360
        self.angle = angle
        self.rotate(id, angle)
        if state:
            rotate_.append(angle)
            stack.append(("旋转", self))

    def rotate(self, id, angle):
        """
        旋转
        :param angle:
        :param id:
        :return:
        """
        self.img = self.rotate_bound(angle)
        self.temp_path = ImageTk.PhotoImage(self.img)
        self.app.itemconfig(id, image=self.temp_path)
        self.var.set(str(int(angle)))
        set_cur(self.id)
        self.angle = angle

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
