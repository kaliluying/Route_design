import tkinter as tk
from PIL import Image, ImageTk


class Scale:
    """
    组件缩放，旋转
    """

    def __init__(self, win, img_path, obj):
        """
        初始化项目
        :param win: 窗口
        :param img_path: 图片路径
        :param obj: SelectedCanvas对象
        """
        self.tk_image = None
        self.win = win
        self.win_size = []
        self.img = Image.open(img_path)
        self.img_path = img_path
        self.w_box = 40
        self.h_box = 40
        self.obj = obj
        self.loop = None
        self.flash = True
        self.start = 1
        self.angle = 0

    def pic_with_win_auto_size(self):
        """
        创建标签，放入图片
        :return:
        """
        w, h = self.img.size
        self.obj.create_widget(tk.Label, width=self.w_box + 3, height=self.h_box)
        pil_image_resized = self.resize(w, h)
        self.tk_image = ImageTk.PhotoImage(pil_image_resized)
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
        else:
            f1 = self.w_box / w
            f2 = self.h_box / h
            factor = min(f1, f2)
        self.start = 0
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
        # if self.flash: self.img_path = self.img_path.replace('.', '5.')
        # self.flash = False
        # img2.save(self.img_path)
        self.img_path = temp_path
        return img2

    def run(self):
        """
        开始函数
        :return:
        """
        self.pic_with_win_auto_size()
        self.obj.place(x=1000, y=100)
        self.obj.remove()
        self.obj.widget.bind("<Key>", self.rotate)
        self.game_loop()
        self.win.protocol('WM_DELETE_WINDOW', self.close_win)
