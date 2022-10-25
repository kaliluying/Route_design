from Tools import is_number, merge, combination, com_abc
from Commom import *


# class Scale:
#     """
#     组件缩放，旋转
#     """
#
#     def __init__(self, win, img_path, obj, obstacle=None, focus=None):
#         """
#         初始化项目
#         :param win: 窗口
#         :param img_path: 图片路径
#         :param obj: SelectedCanvas对象
#         """
#         self.frame_button = None
#         self.frame_input = None
#         self.obstacle = obstacle
#         self.tk_image = None  # 储存变形后的图片对象
#         self.win = win  # 主窗口
#         self.win_size = []  # 储存窗口大小
#         self.img = Image.open(img_path)  # 图片对象
#         self.img_path = img_path  # 图片路径
#         self.w_box = 40  # 组件宽度
#         self.h_box = 40  # 组件高度
#         self.obj = obj  # SelectedCanvas对象
#         self.loop = None  # 循环
#         self.flash = True  # 初始化是不改变图片尺寸
#         self.start = 1  # 状态
#         self.angle = 0  # 角度
#         self.focus = focus  # 工具类
#         self.info = []
#         self.com_info = {}
#         self.state = {}
#
#     def pic_with_win_auto_size(self):
#         """
#         创建标签，放入图片
#         :return:
#         """
#         # w, h = self.img.size
#         self.obj.create_widget(tk.Label, height=self.h_box)
#         # pil_image_resized = self.resize(w, h)
#         self.tk_image = ImageTk.PhotoImage(self.img)
#         self.obj.widget.configure(image=self.tk_image)
#
#     def resize(self, w, h):
#         """
#         对一个图片对象进行缩放，让它在一个矩形框内，还能保持比例
#         :param w: 图片宽
#         :param h: 图片高
#         :return: 返回图片对象
#         """
#         if self.start:
#             factor = 1
#             self.start = 0
#         else:
#             f1 = self.w_box / w
#             f2 = self.h_box / h
#             factor = min(f1, f2)
#         height = int(h * factor)
#         # width = int(w * factor)
#         if height <= 0:
#             height = 1
#         return self.img.resize((w, height), Image.Resampling.LANCZOS)
#
#     def auto_size(self):
#         """
#         先记录窗口大小的数据，若数据发生变化，则变化图片的尺寸。
#         :return:
#         """
#         self.w_box = self.obj.width
#         self.h_box = self.obj.height
#         temp = [self.w_box, self.h_box]
#         self.win_size.append(temp)
#
#         if len(self.win_size) > 2:
#             del self.win_size[0]
#
#         if len(self.win_size) == 2 and self.win_size[0] != self.win_size[1]:
#             self.pic_with_win_auto_size()
#
#     def game_loop(self):
#         """
#         监听标签宽高变化
#         :return:
#         """
#         self.auto_size()
#         self.loop = self.win.after(100, self.game_loop)
#
#     def close_win(self):
#         """
#         结束监听，销毁窗口
#         :return:
#         """
#         # self.win.after_cancel(self.loop)
#         self.win.destroy()
#
#     def rotate(self, event):
#         """
#         键盘监听事件
#         :param event:
#         :return:
#         """
#         if event.char == 'd':
#             self.angle += 30
#             self.img = self.rotate_bound(self.angle)
#             self.pic_with_win_auto_size()
#         elif event.char == 'a':
#             self.angle -= 30
#             self.img = self.rotate_bound(self.angle)
#             self.pic_with_win_auto_size()
#
#     def pop(self, event):
#         """
#         按下删除键后执行的方法
#         :param event:
#         :return:
#         """
#         if self.obstacle in ["oxer", "tirail", "combination_ab", "combination_abc"]:
#             self.focus.remove()
#         self.obj.destroy()
#
#     def update(self, event):
#         """
#         聚焦显示框
#         :param event:
#         :return:
#         """
#         if self.obstacle in ["oxer", "tirail", "combination_ab", "combination_abc"]:
#             self.frame_input, self.frame_button = self.focus.update(self, self.obstacle, info=self.info,
#                                                                     state=self.state, com_info=self.com_info)
#             button = self.frame_button.winfo_children()[0]
#             button.config(command=self.update_img)
#
#     def update_img(self):
#         """
#         从聚焦生成的输入框中获取值更新图片
#         :return:
#         """
#         self.info.clear()
#         for i in self.frame_input.winfo_children():
#             if self.obstacle == "combination_ab" or self.obstacle == "combination_abc":
#                 if is_number(i.get()):
#                     self.com_info[i.getname()] = i.get()
#                     self.state[i.getname()] = i.getstate()
#                     if self.state[i.getname()] == "disabled":
#                         self.com_info[i.getname()] = "0"
#                     continue
#                 elif i.get() == '':
#                     self.com_info[i.getname()] = '0'
#                     self.state[i.getname()] = i.getstate()
#                     continue
#                 else:
#                     messagebox.showerror("错误", "请输入数字")
#                     i.delete(0, 'end')
#                     return
#             if is_number(i.get()):
#                 self.info.append(i.get())
#             elif i.get() == '':
#                 pass
#             else:
#                 messagebox.showerror("错误", "请输入数字")
#                 i.delete(0, 'end')
#                 return
#         if self.obstacle == "oxer":
#             val = self.info[0]
#             self.img_updata(int(val))
#         elif self.obstacle == "tirail":
#             val_a = int(self.info[0])
#             val_b = int(self.info[1])
#             self.img_updata(val_a, val_b)
#         elif self.obstacle == "combination_ab":
#             m1, m2, m3 = self.com_info.values()
#             m1, m2, m3 = int(m1), int(m2), int(m3)
#             if m1 and m2 and m3:
#                 self.img_path = combination(m1, m2, m3)
#                 self.img = Image.open(self.img_path)
#                 self.pic_with_win_auto_size()
#                 return
#             if m1 and m2:
#                 self.img_updata(m1, m2)
#                 return
#             elif m1 and m3:
#                 self.img_updata(m1, m3)
#                 return
#             elif m2 and m3:
#                 self.img_updata(m2, m3)
#                 return
#             if m1:
#                 self.img_updata(m1)
#                 return
#             elif m2:
#                 self.img_updata(m2)
#                 return
#             elif m3:
#                 self.img_updata(m3)
#                 return
#         elif self.obstacle == "combination_abc":
#             m1, m2, m3, m4, m5 = self.com_info.values()
#             m1, m2, m3, m4, m5 = int(m1), int(m2), int(m3), int(m4), int(m5)
#             # if m1 and m2 and m3 and m4 and m5:
#             #     self.img_path = com_abc(m1, m2, m3, m4, m5)
#             #     self.img = Image.open(self.img_path)
#             #     self.pic_with_win_auto_size()
#             #     return
#             # if m1 and
#             self.img_path = com_abc(m1, m2, m3, m4, m5)
#             self.img = Image.open(self.img_path)
#             self.pic_with_win_auto_size()
#
#     def img_updata(self, m1, m2=0):
#         self.img_path = merge(m1, m1=m2)
#         self.img = Image.open(self.img_path)
#         self.pic_with_win_auto_size()
#
#     def rotate_bound(self, angle):
#         """
#         旋转图片
#         :param angle: 旋转角度 正为逆时针旋转，反之
#         :return: 返回图对象
#         """
#         temp_path = self.img_path
#         img = Image.open(self.img_path)
#         img2 = img.convert('RGBA')
#         img2 = img2.rotate(angle)
#         fff = Image.new('RGBA', img2.size, (236, 236, 236, 236))
#         img2 = Image.composite(img2, fff, img2)
#         self.img_path = temp_path
#         return img2
#
#     def run(self):
#         """
#         开始函数
#         :return:
#         """
#         self.pic_with_win_auto_size()
#         self.obj.place(x=1000, y=100)
#         self.obj.widget.bind("<Key>", self.rotate)
#         self.obj.bind("<FocusIn>", self.update)
#         self.obj.widget.bind("<Key-BackSpace>", self.pop)
#
#         # self.game_loop()
#         self.win.protocol('WM_DELETE_WINDOW', self.close_win)


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
        # self.app.focus_set()
        if what.get() == 0:
            self.startx = event.x
            self.starty = event.y
            self.tag = tag
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
        self.app.tag_bind(tag, "<Button-3>", partial(self.pop, self.tag))


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
            m1, m2, m3 = self.com_info.values()
            m1, m2, m3 = int(m1), int(m2), int(m3)
            if m1 and m2 and m3:
                self.img_path = combination(m1, m2, m3)
                self.img = Image.open(self.img_path)
                self.temp_path = ImageTk.PhotoImage(self.img)
                self.app.itemconfig(self.tag, image=self.temp_path)
                return
            if m1 and m2:
                self.img_updata(m1, m2)
                return
            elif m1 and m3:
                self.img_updata(m1, m3)
                return
            elif m2 and m3:
                self.img_updata(m2, m3)
                return
            if m1:
                self.img_updata(m1)
                return
            elif m2:
                self.img_updata(m2)
                return
            elif m3:
                self.img_updata(m3)
                return
        elif self.obstacle == "combination_abc":
            m1, m2, m3, m4, m5 = self.com_info.values()
            m1, m2, m3, m4, m5 = int(m1), int(m2), int(m3), int(m4), int(m5)
            # if m1 and m2 and m3 and m4 and m5:
            #     self.img_path = com_abc(m1, m2, m3, m4, m5)
            #     self.img = Image.open(self.img_path)
            #     self.pic_with_win_auto_size()
            #     return
            # if m1 and
            self.img_path = com_abc(m1, m2, m3, m4, m5)
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
        # b1 = tk.Button(self.app, text="逆时针", command=partial(self.rotate, self.tag, state=1))
        # b2 = tk.Button(self.app, text="顺时针", command=partial(self.rotate, self.tag, state=0))
        # self.app.create_window(1100, 10, window=b1)
        # self.app.create_window(1100, 50, window=b2)
        # tk.Button(win, text="逆时针", command=partial(self.rotate, self.tag, state=1)).place(x=1100, y=10)
        # tk.Button(win, text="顺时针", command=partial(self.rotate, self.tag, state=0)).place(x=1100, y=50)
        tk.Label(win, text="旋转:", font=FONT).place(x=1000, y=20)
        var = tk.StringVar()
        tk.Entry(win, textvariable=var).place(x=1050, y=20, width=50)
        tk.Button(win, text="确认", command=partial(self.rotate, self.tag, var)).place(x=1030, y=50)

    def rotate(self, id, angle):
        """
        旋转
        :param id:
        :param state:
        :return:
        """
        # if state:
        #     self.angle += 30
        #     self.img = self.rotate_bound(self.angle)
        #     temp_img = ImageTk.PhotoImage(self.img)
        #     self.app.itemconfig(id, image=temp_img)
        # else:
        #     self.angle -= 30
        #     self.img = self.rotate_bound(self.angle)
        #     temp_img = ImageTk.PhotoImage(self.img)
        #     self.app.itemconfig(id, image=temp_img)
        # self.angle += int(angle.get())
        self.img = self.rotate_bound(int(angle.get()))
        self.temp_path = ImageTk.PhotoImage(self.img)
        self.app.itemconfig(id, image=self.temp_path)

    def rotate_bound(self, angle):
        """
        旋转图片
        :param angle: 旋转角度 正为逆时针旋转，反之
        :return: 返回图对象
        """
        img = Image.open(self.img_path)
        img2 = img.convert('RGBA')
        img2 = img2.rotate(angle, expand=True)
        # fff = Image.new('RGBA', img2.size, (0, 0, 0, 0))
        # img2 = Image.composite(img2, fff, img2)
        return img2
