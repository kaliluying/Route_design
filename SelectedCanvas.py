from tkinter import Canvas
from functools import partial


class SelectedCanvas(Canvas):
    """
    可调整组件大小、可移动的画布
    """

    def __init__(self, master=None, cnf={}, **kw):
        Canvas.__init__(self, master, cnf, **kw)
        self.height = 80
        self.width = 5
        self.config(bd=0, highlightthickness=0)
        self.is_sizing = False
        self.old_width = 0
        self.old_height = 0
        self.old_pos_x = 0
        self.old_pos_y = 0
        self.start_x = 0
        self.start_y = 0
        self.start_root_x = 0
        self.start_root_y = 0
        self.on_resize_complete = None
        self.have_child = False  # 用以辨别是否有组件创建

    def _mousedown(self, event):
        self.startx = event.x
        self.starty = event.y

    def _drag(self, event):
        try:
            self.place(x=self.winfo_x() + (event.x - self.startx), y=self.winfo_y() + (event.y - self.starty))
        except AttributeError:
            raise ValueError("The widget %s is not draggable" % self.widget)

    def set_on_resize_complete(self, on_resize_complete):
        self.on_resize_complete = on_resize_complete

    def on_update(self):
        """
        初始化后会被调用，在这里绘制矩形
        :return: None
        """
        self.create_rectangle(-1, -1, -2, -2, tag='side', dash=3, outline='grey')
        self.tag_bind('side', "<Button-1>", self._mousedown, add='+')
        self.tag_bind('side', "<B1-Motion>", self._drag, add='+')
        self.tag_bind('side', '<Enter>', lambda event: self.config(cursor='fleur'))
        self.tag_bind('side', '<Leave>', lambda event: self.config(cursor='arrow'))
        for name in ('nw', 'w', 'sw', 'n', 's', 'ne', 'e', 'se'):
            self.create_rectangle(-1, -1, -2, -2, tag=name, outline='blue')
            self.tag_bind(name, "<Enter>", partial(self.on_mouse_enter, name))
            self.tag_bind(name, "<Leave>", partial(self.on_mouse_leave, name))
            self.tag_bind(name, "<Button-1>", partial(self.on_mouse_click, name))
            self.tag_bind(name, "<B1-Motion>", partial(self.on_mouse_move, name))
            self.tag_bind(name, "<ButtonRelease-1>", partial(self.on_mouse_release, name))

    def show(self, is_fill=False):
        """
        显示
        :param is_fill: 是否填充
        :return: None
        """
        width = self.winfo_width()
        height = self.winfo_height()
        self.coords('side', 6, 6, width - 6, height - 6)
        self.coords('nw', 0, 0, 7, 7)
        self.coords('sw', 0, height - 8, 7, height - 1)
        self.coords('w', 0, (height - 7) / 2, 7, (height - 7) / 2 + 7)
        self.coords('n', (width - 7) / 2, 0, (width - 7) / 2 + 7, 7)
        self.coords('s', (width - 7) / 2, height - 8, (width - 7) / 2 + 7, height - 1)
        self.coords('ne', width - 8, 0, width - 1, 7)
        self.coords('se', width - 8, height - 8, width - 1, height - 1)
        self.coords('e', width - 8, (height - 7) / 2, width - 1, (height - 7) / 2 + 7)
        if is_fill:
            for name in ('nw', 'w', 'sw', 'n', 's', 'ne', 'e', 'se'):
                self.itemconfig(name, fill='blue')

    def hide(self):
        """
        隐藏
        :return: None
        """
        self.coords('side', -1, -1, -2, -2, )
        for name in ('nw', 'w', 'sw', 'n', 's', 'ne', 'e', 'se'):
            self.coords(name, -1, -1, -2, -2)

    def on_mouse_enter(self, tag_name, event):
        """
        鼠标进入事件
        :param tag_name: 标签名字
        :param event: event
        :return: None
        """
        if tag_name in ("nw", "sw", "ne", "se"):
            self["cursor"] = "sizing"
        elif tag_name in ("w", "e"):
            self["cursor"] = "sb_h_double_arrow"
        else:
            self["cursor"] = "sb_v_double_arrow"

    def on_mouse_leave(self, tag_name, event):
        """
        鼠标离开事件
        :param tag_name: 标签名字
        :param event: event
        :return: None
        """
        if self.is_sizing:
            return
        self["cursor"] = "arrow"

    def on_mouse_click(self, tag_name, event):
        """
        鼠标点击事件
        :param tag_name: 标签名字
        :param event: event
        :return: None
        """
        self.is_sizing = True
        self.start_x = event.x
        self.start_y = event.y
        self.start_root_x = event.x_root
        self.start_root_y = event.y_root
        self.old_width = self.winfo_width()
        self.old_height = self.winfo_height()
        self.old_pos_x = int(self.place_info()['x'])
        self.old_pos_y = int(self.place_info()['y'])

    def on_mouse_move(self, tag_name, event):
        """
        鼠标移动事件
        :param tag_name: 标签名字
        :param event: event
        :return: None
        """
        if not self.is_sizing:
            return
        if 'e' in tag_name:
            width = max(0, self.old_width + (event.x - self.start_x))
            self.place_configure(width=width)
            self.getwidth(width)
        if 'w' in tag_name:
            width = max(0, self.old_width + (self.start_root_x - event.x_root))
            to_x = event.x - self.start_x + int(self.place_info()['x'])
            self.place_configure(width=width, x=to_x)
            self.getwidth(width)
        if 's' in tag_name:
            height = max(0, self.old_height + (event.y - self.start_y))
            self.place_configure(height=height)
            self.getheight(height)
        if 'n' in tag_name:
            height = max(0, self.old_height + (self.start_root_y - event.y_root))
            to_y = event.y - self.start_y + int(self.place_info()['y'])
            self.place_configure(height=height, y=to_y)
            self.getheight(height)
        self.after_idle(self.show)

    def on_mouse_release(self, tag_name, event):
        """
        鼠标松开事件
        :param tag_name: 标签名字
        :param event: event
        :return: None
        """
        self.is_sizing = False
        if self.on_resize_complete is not None:
            self.on_resize_complete()
        self["cursor"] = "arrow"

    def create_widget(self, widget_class, cnf={}, **kw):
        """
        创建组件
        :param widget_class:
        :param cnf:
        :param kw:
        :return:
        """
        if self.have_child:  # 如果已经创建，则忽略
            return
        self.have_child = True
        self.widget = widget_class(self, cnf, **kw)
        self.widget.pack(fill='both', expand=True, pady=9, padx=9)
        # 即使拖动组件，也可以移动
        self.widget.bind("<Button-1>", self.mousedown, add='+')
        self.widget.bind("<B1-Motion>", self.drag, add='+')
        self.widget.bind('<FocusOut>', lambda event: self.delete('all'))
        self.widget.bind('<FocusIn>', lambda event: (self.on_update(), self.show()))

    def mousedown(self, event):
        """
        鼠标左键按下
        :param event:
        :return:
        """
        self.widget.focus_set()
        self.__startx = event.x
        self.__starty = event.y

    def drag(self, event):
        """
        鼠标左键滚动
        :param event:
        :return:
        """
        self.place(x=self.winfo_x() + (event.x - self.__startx), y=self.winfo_y() + (event.y - self.__starty))

    def getwidth(self, width):
        """
        获取宽
        :param width:
        :return:
        """
        self.width = width

    def getheight(self, height):
        """
        获取高
        :param height:
        :return:
        """
        self.height = height

    def remove(self):
        """
        增加键盘监听删除键的事件
        :return:
        """
        self.widget.bind("<Key-BackSpace>", self.pop)

    def pop(self, event):
        """
        按下删除键后执行的方法
        :param event:
        :return:
        """
        self.destroy()
