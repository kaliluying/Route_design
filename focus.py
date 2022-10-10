import tkinter as tk


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
        self.create_frame()  # 初始化生成frame容器

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = super().__new__(cls)  # super().__new__(cls)这一步操作就可以去实现给对象分配内存地址
        return cls.instance
        # return super().__new__(cls)

    def create_frame(self):
        """
        初始化生成frame容器
        :return:
        """
        self.frame = tk.Frame(self.win)
        self.frame.place(x=1250, y=15)
        self.frame_button = tk.Frame(self.frame)
        self.frame_button.pack(side="bottom")
        self.frame_label = tk.Frame(self.frame)
        self.frame_label.pack(side="left")
        self.frame_input = tk.Frame(self.frame)
        self.frame_input.pack(side="right")

    def update(self, obstacle):
        self.remove()
        if obstacle == "oxer":
            tk.Label(self.frame_label, text='A-->B:').pack()
            var_a_b = tk.StringVar()
            a_b = tk.Entry(self.frame_input, textvariable=var_a_b, width=5)
            a_b.pack()
            tk.Button(self.frame_button, text="确认").pack()
        elif obstacle == "tirail":
            tk.Label(self.frame_label, text='A-->B:').pack()
            var_a_b = tk.StringVar()
            a_b = tk.Entry(self.frame_input, textvariable=var_a_b, width=5)
            a_b.pack()
            tk.Label(self.frame_label, text='B-->C:').pack()
            var_b_c = tk.StringVar()
            b_c = tk.Entry(self.frame_input, textvariable=var_b_c, width=5)
            b_c.pack()
            tk.Button(self.frame_button, text="确认").pack()
        elif obstacle == "combination":
            return
        return self.frame_input, self.frame_button

    def remove(self):
        for i in self.frame_label.winfo_children():
            i.destroy()
        for i in self.frame_input.winfo_children():
            i.destroy()
        for i in self.frame_button.winfo_children():
            i.destroy()
