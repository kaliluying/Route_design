import tkinter as tk
from Tools import is_number, merge, com_image, start_direction, expand
from PIL import Image, ImageTk
from tkinter import messagebox


class Scale:
    """
    组件缩放，旋转
    """

    def __init__(self, win, img_path, obj, obstacle=None, focus=None):
        """
        初始化项目
        :param win: 窗口
        :param img_path: 图片路径
        :param obj: SelectedCanvas对象
        """
        self.frame_button = None
        self.frame_input = None
        self.obstacle = obstacle
        self.tk_image = None  # 储存变形后的图片对象
        self.win = win  # 主窗口
        self.win_size = []  # 储存窗口大小
        self.img = Image.open(img_path)  # 图片对象
        self.img_path = img_path  # 图片路径
        self.w_box = 40  # 组件宽度
        self.h_box = 40  # 组件高度
        self.obj = obj  # SelectedCanvas对象
        self.loop = None  # 循环
        self.flash = True  # 初始化是不改变图片尺寸
        self.start = 1  # 状态
        self.angle = 0  # 角度
        self.focus = focus  # 工具类

    def pic_with_win_auto_size(self):
        """
        创建标签，放入图片
        :return:
        """
        # w, h = self.img.size
        self.obj.create_widget(tk.Label, height=self.h_box)
        # pil_image_resized = self.resize(w, h)
        self.tk_image = ImageTk.PhotoImage(self.img)
        self.obj.widget.configure(image=self.tk_image)

    def resize(self, w, h):
        """
        对一个图片对象进行缩放，让它在一个矩形框内，还能保持比例
        :param w: 图片宽
        :param h: 图片高
        :return: 返回图片对象
        """
        if self.start:
            factor = 1
            self.start = 0
        else:
            f1 = self.w_box / w
            f2 = self.h_box / h
            factor = min(f1, f2)
        height = int(h * factor)
        # width = int(w * factor)
        if height <= 0:
            height = 1
        return self.img.resize((w, height), Image.Resampling.LANCZOS)

    def auto_size(self):
        """
        先记录窗口大小的数据，若数据发生变化，则变化图片的尺寸。
        :return:
        """
        self.w_box = self.obj.width
        self.h_box = self.obj.height
        temp = [self.w_box, self.h_box]
        self.win_size.append(temp)

        if len(self.win_size) > 2:
            del self.win_size[0]

        if len(self.win_size) == 2 and self.win_size[0] != self.win_size[1]:
            self.pic_with_win_auto_size()

    def game_loop(self):
        """
        监听标签宽高变化
        :return:
        """
        self.auto_size()
        self.loop = self.win.after(100, self.game_loop)

    def close_win(self):
        """
        结束监听，销毁窗口
        :return:
        """
        self.win.after_cancel(self.loop)
        self.win.destroy()

    def rotate(self, event):
        """
        键盘监听事件
        :param event:
        :return:
        """
        if event.char == 'd':
            self.angle += 30
            self.img = self.rotate_bound(self.angle)
            self.pic_with_win_auto_size()
        elif event.char == 'a':
            self.angle -= 30
            self.img = self.rotate_bound(self.angle)
            self.pic_with_win_auto_size()

    def pop(self, event):
        """
        按下删除键后执行的方法
        :param event:
        :return:
        """
        if self.obstacle in ["oxer", "tirail", "combination"]:
            self.focus.remove()
        self.obj.destroy()

    def update(self, event):
        """
        聚焦显示框
        :param event:
        :return:
        """
        if self.obstacle in ["oxer", "tirail", "combination"]:
            self.frame_input, self.frame_button = self.focus.update(self.obstacle)
            button = self.frame_button.winfo_children()[0]
            button.config(command=self.update_img)

    def update_img(self):
        """
        从聚焦生成的输入框中获取值更新图片
        :return:
        """
        temp = []
        for i in self.frame_input.winfo_children():
            if is_number(i.get()):
                temp.append(i.get())
            elif i.get() == '':
                pass
            else:
                messagebox.showerror("错误", "请输入数字")
                i.delete(0, 'end')
                return
        if self.obstacle == "oxer":
            val = temp[0]
            com_image = merge(int(val))
            image_path = expand(com_image)
            self.img_path = start_direction(image_path)
            self.img = Image.open(self.img_path)
            self.pic_with_win_auto_size()
        elif self.obstacle == "tirail":
            val_a = int(temp[0])
            val_b = int(temp[1])
            com_image = merge(val_a, m1=val_b)
            image_path = expand(com_image)
            self.img_path = start_direction(image_path)
            self.img = Image.open(self.img_path)
            self.pic_with_win_auto_size()

    def rotate_bound(self, angle):
        """
        旋转图片
        :param angle: 旋转角度 正为逆时针旋转，反之
        :return: 返回图对象
        """
        temp_path = self.img_path
        img = Image.open(self.img_path)
        img2 = img.convert('RGBA')
        img2 = img2.rotate(angle)
        fff = Image.new('RGBA', img2.size, (236, 236, 236, 236))
        img2 = Image.composite(img2, fff, img2)
        self.img_path = temp_path
        return img2

    def run(self):
        """
        开始函数
        :return:
        """
        self.pic_with_win_auto_size()
        self.obj.place(x=1000, y=100)
        self.obj.widget.bind("<Key>", self.rotate)
        self.obj.bind("<FocusIn>", self.update)
        self.obj.widget.bind("<Key-BackSpace>", self.pop)

        # self.game_loop()
        self.win.protocol('WM_DELETE_WINDOW', self.close_win)
