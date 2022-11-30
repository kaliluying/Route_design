import Commom
from Tools import is_number, merge, combination, com_abc, oxer_obs_abc, obs_ab
from Commom import *

current_tag = None


def set_cur(cur):
    global current_tag
    current_tag = cur


def get_cur():
    return current_tag


class T:
    def __init__(self, app, index):
        self.tag = None
        self.startx = 90
        self.starty = 10
        self.angle = 0
        self.app = app
        self.index = str(index)

    def mousedown(self, tag, event):
        """
        鼠标左键按下
        :param event:
        :return:
        """
        if what.get() == 0:
            self.startx = event.x
            self.starty = event.y
            self.tag = tag
            set_cur(tag)
            self.app.lift(self.tag)

    def drag(self, tag, event):
        if what.get() == 0:
            self.app.move(tag, event.x - self.startx, event.y - self.starty)
            self.startx = event.x
            self.starty = event.y

    def pop(self, tag, event):
        self.app.delete(tag)


class CreateTxt(T):

    def create_txt(self, txt):
        tag = "txt" + self.index
        text = self.app.create_text(self.startx, self.starty, text=txt, tags=tag)
        self.app.tag_bind(tag, "<Button-1>", partial(self.mousedown, tag))
        self.app.tag_bind(tag, "<B1-Motion>", partial(self.drag, text))
        self.app.tag_bind(tag, "<Button-2>", partial(self.pop, tag))


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

    def create_img(self):
        self.tag = "img" + self.index
        self.img_file = ImageTk.PhotoImage(self.img_obj)
        img_id = self.app.create_image(self.startx, self.starty, image=self.img_file,
                                       anchor="n", tag=self.tag)
        self.app.tag_bind(self.tag, "<Button-1>", partial(self.mousedown, self.tag))
        self.app.tag_bind(self.tag, "<B1-Motion>", partial(self.drag, img_id))
        self.app.tag_bind(self.tag, "<Button-2>", partial(self.pop, self.tag))

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
            for i in frame_edit.winfo_children():
                for j in i.winfo_children():
                    for d in j.winfo_children():
                        print(d)


    def update_img(self):
        """
        从聚焦生成的输入框中获取值更新图片
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
                pass
            else:
                messagebox.showerror("错误", "请输入数字")
                i.delete(0, 'end')
                return
        if self.obstacle == "oxer":
            val = self.info[0]
            self.img_updata(int(val))
        elif self.obstacle == "tirail":
            val_a = int(self.info[0])
            val_b = int(self.info[1])
            self.img_updata(val_a, val_b)
        elif self.obstacle == "combination_ab":
            temp = {}
            for key, val in self.com_info.items():
                if key.count('_') == 2 and val != '0':
                    temp[key] = (int(val) * 10)
                elif key.count('_') == 1 and val != '0':
                    temp[key] = (int(val) / 10)
                else:
                    temp[key] = 0
            print(temp)
            a, a_b, b = temp.values()
            a, a_b, b = round(a), round(a_b), round(b)
            print(a, a_b, b)
            self.img_path = obs_ab(a, b, a_b)
            self.img = Image.open(self.img_path)
            self.temp_path = ImageTk.PhotoImage(self.img)
            self.app.itemconfig(self.tag, image=self.temp_path)
        elif self.obstacle == "combination_abc":
            a, a_b, b, b_c, c = self.com_info.values()
            a, a_b, b, b_c, c = int(a), int(a_b), int(b), int(b_c), int(c)
            self.img_path = oxer_obs_abc(a, b, c, a_b, b_c)
            self.img = Image.open(self.img_path)
            self.temp_path = ImageTk.PhotoImage(self.img)
            self.app.itemconfig(self.tag, image=self.temp_path)

    def img_updata(self, m1, m2=0):
        self.img_path = merge(m1, m1=m2)
        self.img = Image.open(self.img_path)
        self.temp_path = ImageTk.PhotoImage(self.img)
        self.app.itemconfig(self.tag, image=self.temp_path)

    def butt(self):
        """
        按钮
        :return:
        """
        for i in frame_edit.winfo_children():
            for j in i.winfo_children():
                for d in j.winfo_children():
                    d.destroy()

        tk.Label(frame_focus_x_ladel, text="旋转： ", font=FONT).pack()
        self.var = tk.StringVar()
        self.var.set(str(self.angle))
        tk.Entry(frame_focus_x_ent, textvariable=self.var, width=5).pack()
        tk.Button(frame_focus_x_but, text="确认", command=partial(self.rotate, self.tag, self.var)).pack()
        tk.Label(frame_focus_z_ladel, text="备注： ", font=FONT).pack()
        var_name = tk.StringVar(value=self.name)
        tk.Entry(frame_focus_z_ent, textvariable=var_name, width=5).pack()
        tk.Button(frame_focus_z_but, text="确认", command=partial(self.set_name, var_name)).pack()
        # tk.Button(frame_edit, text="放置", command=self.set_state).pack()

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
        self.img = self.rotate_bound(angle)
        self.temp_path = ImageTk.PhotoImage(self.img)
        self.app.itemconfig(id, image=self.temp_path)
        self.var.set(str(int(angle)))

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
