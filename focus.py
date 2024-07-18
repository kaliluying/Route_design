import sys
from functools import partial

from Common import *
from Tools import *


class Focus:
    """
    组件聚焦后
    """
    instance = None

    def __init__(self, win):
        self.win = win
        self.frame = None
        self.create_frame()  # 初始化生成frame容器

    def __new__(cls, *args, **kwargs):
        """
        单例模式
        :param args:
        :param kwargs:
        """
        if cls.instance is None:
            cls.instance = super().__new__(cls)  # super().__new__(cls)这一步操作就可以去实现给对象分配内存地址
        return cls.instance

    def create_frame(self):
        """
        初始化生成frame容器
        :return:
        """
        self.frame = ttk.Frame(self.win, name='障碍编辑容器')
        self.frame.pack()

    def update(self, obj, obstacle, info=None, state=None, com_info=None):
        """
        点击组件后生成信息框
        :param obj: scale类对象
        :param obstacle: 标识
        :param info: 输入框中的内容
        :param com_info:
        :param state:
        :return: 返回input和button容器
        """
        self.create_frame()
        self.remove()
        if obstacle == "oxer":
            ttk.Label(self.frame, text='A-->B(m):').grid(row=0, column=0, sticky='e', padx=5, pady=5)
            var_a_b = ttk.StringVar(value=info[0] if info else '')
            a_b = Entry(self.frame, textvariable=var_a_b, width=5)
            a_b.grid(row=0, column=1, sticky='w', padx=5, pady=5)
            ttk.Button(self.frame, bootstyle=CONFIRM_STYLE, text="确认").grid(row=1, column=1, sticky='w', padx=5,
                                                                              pady=5)

        elif obstacle == "tirail" or obstacle == "four":
            ttk.Label(self.frame, text='障碍长度(m):').grid(row=0, column=0, sticky='e', padx=5, pady=5)
            var = ttk.StringVar(value=info[0] if info else '')
            a_b = Entry(self.frame, textvariable=var, width=5, )
            a_b.grid(row=0, column=1, sticky='w', padx=5, pady=5)
            ttk.Button(self.frame, bootstyle=CONFIRM_STYLE, text="确认").grid(row=2, column=1, sticky='w', padx=5,
                                                                              pady=5)

        elif obstacle == "combination_ab" or obstacle == "combination_abc":
            self.combination(obj, com_info, obstacle, state)
        elif obstacle == "water":
            self.water(info)
        elif obstacle == "live":
            self.live(info, obj)

        buttons = [child for child in self.frame.winfo_children() if isinstance(child, ttk.Button)][0]
        entrys = [child for child in self.frame.winfo_children() if isinstance(child, Entry)]
        return entrys, buttons

    def live(self, info, obj):
        """
        利物浦聚焦输入框
        :param obj:
        :param info:
        :return:
        """
        check = ttk.StringVar(value='0')
        ttk.Label(self.frame, text='宽(m)：').grid(row=0, column=0, sticky='e', padx=5, pady=5)
        water_width_var = ttk.StringVar(value=info[0] if info else '2')
        water_width_ent = Entry(self.frame, textvariable=water_width_var, width=5, name='water_w_ent')
        water_width_ent.grid(row=0, column=1, sticky='w', padx=5, pady=5)
        ttk.Label(self.frame, text='长(m)：').grid(row=1, column=0, sticky='e', padx=5, pady=5)
        water_height_var = ttk.StringVar(value=info[0] if info else '4')
        water_height_ent = Entry(self.frame, textvariable=water_height_var, width=5, name='water_h_ent')
        water_height_ent.grid(row=1, column=1, sticky='w', padx=5, pady=5)
        water_height_ent.bind("<Command-KeyPress-z>", water_width_ent.undo)

        ttk.Button(self.frame, bootstyle=CONFIRM_STYLE, text="确认").grid(row=2, column=1, sticky='w', padx=5, pady=5)
        ttk.Checkbutton(self.frame, text='双横木', variable=check, onvalue=1, offvalue=0,
                        command=partial(self.live_two, obj, check)).grid(row=2, column=0, sticky="w", padx=5, pady=5)

    @staticmethod
    def live_two(obj, check):
        """
        根据传入的检查状态，切换图片以实现两种不同的现场显示。

        参数:
        - obj: 包含应用界面元素的对象，需要有img_path, img, temp_path, app, 和 tag属性。
        - check: 一个可以获取状态的对象，预期为'1'或'0'，决定显示哪张图片。

        返回值:
        - 无
        """
        check = check.get()  # 获取检查状态
        set_live(check)  # 设置现场状态
        if check == '1':
            # 如果检查状态为'1'，则使用第二种现场图片
            obj.img_path = live_two_tool()  # 获取第二现场图片路径
            obj.img = Image.open(obj.img_path)  # 打开图片
            obj.temp_path = ImageTk.PhotoImage(obj.img)  # 将图片转换为可以在GUI中使用的格式
            obj.app.itemconfig(obj.tag, image=obj.temp_path)  # 更新界面元素显示图片
            obj.to_rotate(obj.tag, obj.angle)
        elif check == '0':
            # 如果检查状态为'0'，则使用第一种现场图片
            obj.img_path = live_one_tool()  # 获取第一现场图片路径
            obj.img = Image.open(obj.img_path)  # 打开图片
            obj.temp_path = ImageTk.PhotoImage(obj.img)  # 将图片转换为可以在GUI中使用的格式
            obj.app.itemconfig(obj.tag, image=obj.temp_path)  # 更新界面元素显示图片
            obj.to_rotate(obj.tag, obj.angle)

    def water(self, info):
        """
        水障聚焦框
        :param info:
        :return:
        """
        ttk.Label(self.frame, text='宽(m)：').grid(row=0, column=0, sticky="w", padx=5, pady=5)
        water_width_var = ttk.StringVar(value=info[0] if info else '3')
        water_width_ent = Entry(self.frame, textvariable=water_width_var, width=5)
        water_width_ent.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Label(self.frame, text='长(m)：').grid(row=1, column=0, sticky="w", padx=5, pady=5)
        water_height_var = ttk.StringVar(value=info[0] if info else '4')
        water_height_ent = Entry(self.frame, textvariable=water_height_var, width=5)
        water_height_ent.grid(row=1, column=1, sticky="w", padx=5, pady=5)
        ttk.Button(self.frame, bootstyle=CONFIRM_STYLE, text="确认").grid(row=2, column=1, sticky="w", padx=5, pady=5)

    def combination(self, obj, info, obstacle, state):
        """
        组合障碍聚焦输入框
        :param obj:
        :param info:
        :param obstacle:
        :param state:
        :return:
        """
        a = b = c = '0'
        if state:
            a = '1' if state['ent_a'].__str__() == 'normal' else '0'
            b = '1' if state['ent_b'].__str__() == 'normal' else '0'
            try:
                c = '1' if state['ent_c'].__str__() == 'normal' else '0'
            except KeyError:
                pass
        checkvar_a = ttk.StringVar(value=a, name="checkvar_a")
        checkvar_b = ttk.StringVar(value=b, name="checkvar_b")
        checkvar_c = ttk.StringVar(value=c, name="checkvar_c")

        var_a = ttk.StringVar(value=info['ent_a'] if info else '')
        ent_a = Entry(self.frame, textvariable=var_a, width=5,
                      state=state["ent_a"] if state else "disabled",
                      name="ent_a")
        # ent_a.pack()

        ent_a.grid(row=0, column=1, sticky="w", padx=5, pady=5)
        ttk.Checkbutton(self.frame, text="A双横木(cm)", variable=checkvar_a, onvalue=1, offvalue=0,
                        command=partial(self.oxer_a, checkvar_a, checkvar_b, checkvar_c, ent_a, obj, obstacle,
                                        var_a)).grid(row=0, column=0, sticky='e', padx=5, pady=5)

        ttk.Label(self.frame, text='A-->B(m):').grid(row=1, column=0, sticky="e", padx=5, pady=5)
        var_a_b = ttk.StringVar(value=info['ent_a_b'] if info else '3')
        ent_a_b = Entry(self.frame, textvariable=var_a_b, width=5, name="ent_a_b")
        ent_a_b.grid(row=1, column=1, sticky='w', padx=5, pady=5)

        var_b = ttk.StringVar(value=info['ent_b'] if info else '')
        ent_b = Entry(self.frame, textvariable=var_b, width=5,
                      state=state["ent_b"] if state else "disabled",
                      name='ent_b')
        ent_b.grid(row=2, column=1, sticky='w', padx=5, pady=5)

        ttk.Checkbutton(self.frame, text="B双横木(cm)", variable=checkvar_b, onvalue=1, offvalue=0,
                        command=partial(self.oxer_b, checkvar_a, checkvar_b, checkvar_c, ent_b, obj, obstacle,
                                        var_b)).grid(row=2, column=0, sticky='e', padx=5, pady=5)
        if obstacle == "combination_ab":
            ttk.Button(self.frame, bootstyle=CONFIRM_STYLE, text="确认").grid(row=3, column=1, sticky='e', padx=5,
                                                                              pady=5)
        if obstacle == "combination_abc":
            ttk.Label(self.frame, text='B-->C(m):').grid(row=3, column=0, sticky="e", padx=5, pady=5)
            var_b_c = ttk.StringVar(value=info['ent_b_c'] if info else '3')
            ent_b_c = Entry(self.frame, textvariable=var_b_c, width=5, name="ent_b_c")
            ent_b_c.grid(row=3, column=1, sticky='w', padx=5, pady=5)
            var_c = ttk.StringVar(value=info['ent_c'] if info else '')
            ent_c = Entry(self.frame, textvariable=var_c, width=5,
                          state=state["ent_c"] if state else "disabled",
                          name="ent_c")
            ent_c.grid(row=4, column=1, sticky='w', padx=5, pady=5)
            ttk.Checkbutton(self.frame, text="C双横木(cm)", variable=checkvar_c, onvalue=1, offvalue=0,
                            command=partial(self.oxer_c, checkvar_a, checkvar_b, checkvar_c, ent_c, obj, var_c)).grid(
                row=4, column=0, sticky='e', padx=5, pady=5)
            ttk.Button(self.frame, bootstyle=CONFIRM_STYLE, text="确认").grid(row=5, column=1, sticky='e', padx=5,
                                                                              pady=5)

        return checkvar_a, checkvar_b

    def remove(self):
        """
        删除容器中的内容
        :return:
        """
        for i in self.frame.winfo_children():
            i.destroy()

    @staticmethod
    def oxer(x1, ent, var):
        """
        设置输入框状态
        :param x1:
        :param ent:
        :param var:
        :return:
        """
        if x1.get() == '1':
            ent.enable()
            # ent.config(state='normal')
            # print(var.get(), 'normal')
            # if not var.get():
            #     var.set('50')

        elif x1.get() == '0':
            ent.disable()
            # ent.config(state='disabled', textvariable="light gray")
            # print(var.get(), 'disable')

    def oxer_a(self, x1, x2, x3, ent_a, obj, obstacle, var_a):
        """
        选中A障碍是否为双横木
        :param x1: a障碍是否为双横木
        :param x2: b障碍是否为双横木
        :param x3: c障碍是否为双横木
        :param ent_a: 输入框
        :param obj: 组件对像
        :param obstacle: ab组合还是abc
        :param var_a: 输入框值
        :return:
        """
        self.oxer(x1, ent_a, var_a)
        if obstacle == "combination_abc":
            self.judge_abc(x1, x2, x3, obj)
            return
        if x1.get() == '1':
            try:
                if x2.get() == '1':
                    self.com(obj)
                    return
                elif x2.get() == '0':
                    pass
            except Exception as e:
                print(f"{os.path.basename(__file__)}, line {sys._getframe().f_lineno}, {e}", e)
                logging.warning(e)

            obj.img_path = oxer_obs_ab(stare_a=x1.get(), state_b=x2.get())
            # obj.img_path = merge(5, m1=20)
            obj.img = Image.open(obj.img_path)
            obj.temp_path = ImageTk.PhotoImage(obj.img)
            obj.app.itemconfig(obj.tag, image=obj.temp_path)
            obj.to_rotate(obj.tag, obj.angle)
        elif x1.get() == '0':
            try:
                if x2.get() == '1':
                    obj.img_path = oxer_obs_ab(stare_a=x1.get(), state_b=x2.get())
                    obj.img = Image.open(obj.img_path)
                    obj.temp_path = ImageTk.PhotoImage(obj.img)
                    obj.app.itemconfig(obj.tag, image=obj.temp_path)
                    obj.to_rotate(obj.tag, obj.angle)
                    return
                elif x2.get() == '0':
                    obj.img_path = merge_ab(state=1, m1=30)
                    obj.img = Image.open(obj.img_path)
                    obj.temp_path = ImageTk.PhotoImage(obj.img)
                    obj.app.itemconfig(obj.tag, image=obj.temp_path)
                    obj.to_rotate(obj.tag, obj.angle)
                    return
            except Exception as e:
                print(f"{os.path.basename(__file__)}, line {sys._getframe().f_lineno}, {e}", 'a障碍', e)
                logging.warning('a障碍', e)

    def oxer_b(self, x1, x2, x3, ent_b, obj, obstacle, var_b):
        """
        选中B障碍是否为双横木
        :param x1: a障碍是否为双横木
        :param x2: b障碍是否为双横木
        :param x3: c障碍是否为双横木
        :param ent_b: 输入框
        :param obj: 组件对像
        :param obstacle: ab组合还是abc
        :param var_b: 输入框值
        :return:
        """
        self.oxer(x2, ent_b, var_b)
        if obstacle == "combination_abc":
            self.judge_abc(x1, x2, x3, obj)
            return

        if x2.get() == '1':
            try:
                if x1.get() == '1':
                    self.com(obj)
                    return
                elif x1.get() == '0':
                    pass
            except:
                pass
            obj.img_path = oxer_obs_ab(stare_a=x1.get(), state_b=x2.get())
            obj.img = Image.open(obj.img_path)
            obj.temp_path = ImageTk.PhotoImage(obj.img)
            obj.app.itemconfig(obj.tag, image=obj.temp_path)
            obj.to_rotate(obj.tag, obj.angle)
        elif x2.get() == '0':
            try:
                if x1.get() == '1':
                    obj.img_path = oxer_obs_ab(stare_a=x1.get(), state_b=x2.get())
                    obj.img = Image.open(obj.img_path)
                    obj.temp_path = ImageTk.PhotoImage(obj.img)
                    obj.app.itemconfig(obj.tag, image=obj.temp_path)
                    obj.to_rotate(obj.tag, obj.angle)
                    return
                elif x1.get() == '0':
                    obj.img_path = merge_ab(state=1, m1=30)
                    obj.img = Image.open(obj.img_path)
                    obj.temp_path = ImageTk.PhotoImage(obj.img)
                    obj.app.itemconfig(obj.tag, image=obj.temp_path)
                    obj.to_rotate(obj.tag, obj.angle)
                    return
            except Exception as e:
                print(f"{os.path.basename(__file__)}, line {sys._getframe().f_lineno}, {e}", 'b障碍', e)
                logging.warning('b障碍', e)

    def oxer_c(self, x1, x2, x3, ent_c, obj, var_c):
        """
        障碍C是否为双横木
        :param x1:障碍A是否为双横木
        :param x2:障碍B是否为双横木
        :param x3:障碍C是否为双横木
        :param ent_c:障碍C输入框
        :param obj:障碍对象
        :param var_c:输入框值
        :return:
        """
        self.oxer(x3, ent_c, var_c)
        self.judge_abc(x1, x2, x3, obj)

    @staticmethod
    def com(obj):
        """
        当两个都是双横木
        :param obj:
        :return:
        """

        obj.img_path = merge_ab(state=2, m1=30)
        obj.img = Image.open(obj.img_path)
        obj.temp_path = ImageTk.PhotoImage(obj.img)
        obj.app.itemconfig(obj.tag, image=obj.temp_path)
        obj.to_rotate(obj.tag, obj.angle)

    @staticmethod
    def combination_abc(obj, x1, x2, x3):
        obj.img_path = oxer_obs_ab(stare_a=x1.get(), state_b=x2.get(), state_c=x3.get(), b_c=30)
        obj.img = Image.open(obj.img_path)
        obj.temp_path = ImageTk.PhotoImage(obj.img)
        obj.app.itemconfig(obj.tag, image=obj.temp_path)
        obj.to_rotate(obj.tag, obj.angle)

    def judge_abc(self, x1, x2, x3, obj):
        """
        ABC组合障碍双横木判断
        :param x1:
        :param x2:
        :param x3:
        :param obj:
        :return:
        """
        try:
            if ((x1.get() == x2.get() == x3.get() == '0') or
                    (x1.get() == x2.get() == x3.get() == '1')):
                state = int(x1.get()) + 1
                obj.img_path = merge_ab(state=state, m1=30, m2=30)
                obj.img = Image.open(obj.img_path)
                obj.temp_path = ImageTk.PhotoImage(obj.img)
                obj.app.itemconfig(obj.tag, image=obj.temp_path)
                obj.to_rotate(obj.tag, obj.angle)
                return
            else:
                self.combination_abc(obj, x1, x2, x3)
        except Exception as e:
            print(f"{os.path.basename(__file__)}, line {sys._getframe().f_lineno}, {e}",'abc障碍', e)
            logging.warning('abc障碍', e)
