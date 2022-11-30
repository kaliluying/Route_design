from Commom import *
from Tools import *


class Entry(tk.Entry):
    def __init__(self, master=None, cnf={}, **kw):
        tk.Entry.__init__(self, master, cnf, **kw)
        self.con = None
        self.kw = kw

    def config(self, cnf=None, **kw):
        tk.Entry.configure(self, cnf, **kw)
        self.con = kw

    def getname(self):
        return self.kw['name']

    def getstate(self):
        try:
            try:
                return self.con['state']
            except:
                return self.kw['state']
        except:
            return ''


class Focus:
    """
    组件聚焦后
    """
    instance = None

    def __init__(self, win):
        self.win = win
        self.frame = None
        self.frame_input = None
        self.frame_label = None
        self.frame_button = None
        self.frame_select = None
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
        self.frame = tk.Frame(self.win)
        self.frame.pack()
        self.frame_button = tk.Frame(self.frame)
        self.frame_button.pack(side="bottom")
        self.frame_label = tk.Frame(self.frame)
        self.frame_label.pack(side="left")
        self.frame_select = tk.Frame(self.frame)
        self.frame_select.pack(side="right")
        self.frame_input = tk.Frame(self.frame)
        self.frame_input.pack(side="right")

    def update(self, obj, obstacle, info=None, state=None, com_info=None):
        """
        点击组件后生成信息框
        :param obj: scale类对像
        :param obstacle: 标识
        :param info: 输入框中的内容
        :return: 返回input和button容器
        :param com_info:
        :param state:
        """
        self.remove()
        if obstacle == "oxer":
            tk.Label(self.frame_label, text='A-->B(m):').pack()
            var_a_b = tk.StringVar(value=info[0] if info else '')
            a_b = tk.Entry(self.frame_input, textvariable=var_a_b, width=5)
            a_b.pack()
            tk.Button(self.frame_button, text="确认").pack()

        elif obstacle == "tirail":
            tk.Label(self.frame_label, text='A-->B(m):').pack()
            var_a_b = tk.StringVar(value=info[0] if info else '')
            a_b = tk.Entry(self.frame_input, textvariable=var_a_b, width=5)
            a_b.pack()
            tk.Label(self.frame_label, text='B-->C(m):').pack()
            var_b_c = tk.StringVar(value=info[1] if info else '')
            b_c = tk.Entry(self.frame_input, textvariable=var_b_c, width=5)
            b_c.pack()
            tk.Button(self.frame_button, text="确认").pack()

        elif obstacle == "combination_ab" or obstacle == "combination_abc":
            self.combination(obj, com_info, obstacle, state)
        return self.frame_input, self.frame_button

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
            a = '1' if state['ent_a'] == 'normal' else '0'
            b = '1' if state['ent_b'] == 'normal' else '0'
            try:
                c = '1' if state['ent_c'] == 'normal' else '0'
            except KeyError:
                pass

        checkvar_a = tk.StringVar(value=a, name="checkvar_a")
        checkvar_b = tk.StringVar(value=b, name="checkvar_b")
        checkvar_c = tk.StringVar(value=c, name="checkvar_c")

        var_a = tk.StringVar(value=info['ent_a'] if info else '')
        ent_a = Entry(self.frame_input, textvariable=var_a, width=5,
                      state=state["ent_a"] if state else "disabled",
                      name="ent_a")
        ent_a.pack()

        Checkbutton(self.frame_label, text="A双横木(cm)", variable=checkvar_a, onvalue=1, offvalue=0,
                    command=partial(self.oxer_a, checkvar_a, checkvar_b, checkvar_c, ent_a, obj, obstacle,
                                    var_a)).pack()

        tk.Label(self.frame_label, text='A-->B(m):').pack()
        var_a_b = tk.StringVar(value=info['ent_a_b'] if info else '3')
        ent_a_b = Entry(self.frame_input, textvariable=var_a_b, width=5, name="ent_a_b")
        ent_a_b.pack()

        var_b = tk.StringVar(value=info['ent_b'] if info else '')
        ent_b = Entry(self.frame_input, textvariable=var_b, width=5,
                      state=state["ent_b"] if state else "disabled",
                      name='ent_b')
        ent_b.pack()

        Checkbutton(self.frame_label, text="B双横木(cm)", variable=checkvar_b, onvalue=1, offvalue=0,
                    command=partial(self.oxer_b, checkvar_a, checkvar_b, checkvar_c, ent_b, obj, obstacle,
                                    var_b)).pack()
        if obstacle == "combination_abc":
            tk.Label(self.frame_label, text='B-->C(m):').pack()
            var_b_c = tk.StringVar(value=info['ent_b_c'] if info else '3')
            ent_b_c = Entry(self.frame_input, textvariable=var_b_c, width=5, name="ent_b_c")
            ent_b_c.pack()
            var_c = tk.StringVar(value=info['ent_c'] if info else '')
            ent_c = Entry(self.frame_input, textvariable=var_c, width=5,
                          state=state["ent_c"] if state else "disabled",
                          name="ent_c")
            ent_c.pack()
            Checkbutton(self.frame_label, text="C双横木(cm)", variable=checkvar_c, onvalue=1, offvalue=0,
                        command=partial(self.oxer_c, checkvar_a, checkvar_b, checkvar_c, ent_c, obj, var_c)).pack()

        tk.Button(self.frame_button, text="确认").pack()
        return checkvar_a, checkvar_b

    def remove(self):
        """
        删除容器中的内容
        :return:
        """
        for i in self.frame_label.winfo_children():
            i.destroy()
        for i in self.frame_input.winfo_children():
            i.destroy()
        for i in self.frame_button.winfo_children():
            i.destroy()
        for i in self.frame_select.winfo_children():
            i.destroy()

    def oxer(self, x1, ent, var):
        """
        :param x1:
        :param ent:
        :param obj:
        :return:
        """
        if x1.get() == '1':
            ent.config(state='normal', )
            # if not var.get():
            #     print(var.get())
            #     var.set('1')
        elif x1.get() == '0':
            ent.config(state='disabled')

    def oxer_a(self, x1, x2, x3, ent_a, obj, obstacle, var_a):
        """
        选中A障碍是否为双横木
        :param x1: a障碍是否为双横木
        :param x2: b障碍是否为双横木
        :param x3: c障碍是否为双横木
        :param ent_a: 输入框
        :param obj: 组件对像
        :param obstacle: ab组合还是abc
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
                print(e)
            obj.img_path = oxer_obs_ab(stare_a=x1.get(), state_b=x2.get())
            # obj.img_path = merge(5, m1=20)
            obj.img = Image.open(obj.img_path)
            obj.temp_path = ImageTk.PhotoImage(obj.img)
            obj.app.itemconfig(obj.tag, image=obj.temp_path)
        elif x1.get() == '0':
            try:
                if x2.get() == '1':
                    obj.img_path = oxer_obs_ab(stare_a=x1.get(), state_b=x2.get())
                    obj.img = Image.open(obj.img_path)
                    obj.temp_path = ImageTk.PhotoImage(obj.img)
                    obj.app.itemconfig(obj.tag, image=obj.temp_path)
                    return
                elif x2.get() == '0':
                    obj.img_path = merge_ab(state=1, m1=30)
                    obj.img = Image.open(obj.img_path)
                    obj.temp_path = ImageTk.PhotoImage(obj.img)
                    obj.app.itemconfig(obj.tag, image=obj.temp_path)
                    return
            except Exception as e:
                print('a障碍', e)

    def oxer_b(self, x1, x2, x3, ent_b, obj, obstacle, var_b):
        """
        选中B障碍是否为双横木
        :param x1:
        :param x2:
        :param x3:
        :param ent_b:
        :param obj:
        :param obstacle:
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
        elif x2.get() == '0':
            try:
                if x1.get() == '1':
                    obj.img_path = oxer_obs_ab(stare_a=x1.get(), state_b=x2.get())
                    obj.img = Image.open(obj.img_path)
                    obj.temp_path = ImageTk.PhotoImage(obj.img)
                    obj.app.itemconfig(obj.tag, image=obj.temp_path)
                    return
                elif x1.get() == '0':
                    obj.img_path = merge_ab(state=1, m1=30)
                    obj.img = Image.open(obj.img_path)
                    obj.temp_path = ImageTk.PhotoImage(obj.img)
                    obj.app.itemconfig(obj.tag, image=obj.temp_path)
                    return
            except Exception as e:
                print('b障碍', e)

    def oxer_c(self, x1, x2, x3, ent_c, obj, var_c):
        self.oxer(x3, ent_c, var_c)
        self.judge_abc(x1, x2, x3, obj)

    def com(self, obj):
        """
        当两个都是双横木
        :param obj:
        :return:
        """
        obj.img_path = merge_ab(state=2, m1=30)
        obj.img = Image.open(obj.img_path)
        obj.temp_path = ImageTk.PhotoImage(obj.img)
        obj.app.itemconfig(obj.tag, image=obj.temp_path)

    def combination_abc(self, obj, x1, x2, x3):
        obj.img_path = oxer_obs_ab(stare_a=x1.get(), state_b=x2.get(), state_c=x3.get(), b_c=30)
        obj.img = Image.open(obj.img_path)
        obj.temp_path = ImageTk.PhotoImage(obj.img)
        obj.app.itemconfig(obj.tag, image=obj.temp_path)

    def judge_abc(self, x1, x2, x3, obj):
        try:
            if x1.get() == '1':
                if x2.get() == '1':
                    if x3.get() == '1':
                        obj.img_path = merge_ab(state=2, m1=30, m2=30)
                        obj.img = Image.open(obj.img_path)
                        obj.temp_path = ImageTk.PhotoImage(obj.img)
                        obj.app.itemconfig(obj.tag, image=obj.temp_path)
                        return
                    elif x3.get() == '0':
                        self.combination_abc(obj, x1, x2, x3)
                        return
                elif x2.get() == '0':
                    if x3.get() == '1':
                        self.combination_abc(obj, x1, x2, x3)
                        return
                    elif x3.get() == '0':
                        self.combination_abc(obj, x1, x2, x3)
                        return
            elif x1.get() == '0':
                if x2.get() == '1':
                    if x3.get() == '1':
                        self.combination_abc(obj, x1, x2, x3)
                        return
                    elif x3.get() == '0':
                        self.combination_abc(obj, x1, x2, x3)
                        return
                elif x2.get() == '0':
                    if x3.get() == '1':
                        self.combination_abc(obj, x1, x2, x3)
                        return
                    elif x3.get() == '0':
                        obj.img_path = merge_ab(state=1, m1=30, m2=30)
                        obj.img = Image.open(obj.img_path)
                        obj.temp_path = ImageTk.PhotoImage(obj.img)
                        obj.app.itemconfig(obj.tag, image=obj.temp_path)
                        return
        except Exception as e:
            print('abc障碍', e)
