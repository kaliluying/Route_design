import base64
import io
from functools import partial

import data_url

from Common import *
from Tools import is_number, merge, oxer_obs_abc, obs_ab, remove_from_edit, water_wh, live_edit, Entry


class T:
    all_instances = []

    def __init__(self, app, index):
        self.__class__.all_instances.append(self)  # 添加实例
        self.tag = None  # 标签
        self.startx = 160  # 鼠标开始x位置
        self.starty = 25  # 鼠标开始y位置
        self.current_x = 160  # 障碍当前x位置
        self.current_y = 25  # 障碍当前y位置
        self.angle = 0  # 障碍当前角度
        self.temp_angle = 0  # 障碍临时角度
        self.lest_angle = 0  # 障碍临时角度
        self.app = app  # 画布
        self.index = str(index)  # 障碍索引
        self.line_tag = None  # 障碍线标签
        self.id = None  # 障碍id
        self.txt = None  # 障碍文字标签
        self.ui_state = True

    def load(self, **kwargs):
        self.startx = kwargs.get('startx', 160)
        self.starty = kwargs.get('starty', 25)
        self.current_x = kwargs.get('current_x', 160)
        self.current_y = kwargs.get('current_y', 25)
        self.angle = kwargs.get('angle', 0)
        self.temp_angle = kwargs.get('temp_angle', 0)
        self.lest_angle = kwargs.get('lest_angle', 0)
        self.index = kwargs.get('index', str(index))

    def save(self):
        """
        保存障碍
        :return:
        """
        save_dict = {'startx': self.startx, 'starty': self.starty, 'current_x': self.current_x,
                     'current_y': self.current_y, 'angle': self.angle, 'temp_angle': self.temp_angle,
                     'lest_angle': self.lest_angle, 'txt': self.txt, 'index': self.index}
        return save_dict

    def mousedown(self, tag, event):
        """
        鼠标左键按下
        :param tag:
        :param event:
        :return:
        """
        global choice_tup
        set_frame_stare(False)
        set_obstacle(self)
        try:
            if choice_tup and not (min(choice_tup[0], choice_tup[2]) < event.x < max(choice_tup[0], choice_tup[2])
                                   and min(choice_tup[1], choice_tup[3]) < event.y < max(choice_tup[1], choice_tup[3])):
                self.app.delete('choice')
                choice_tup.clear()
                self.app.dtag('choice_start', 'choice_start')
        except Exception as e:
            print(e)
            logging.warning(e)
        # if what.get() == 0:
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
            # self.app.move('point', event.x - self.startx, event.y - self.starty)
            # if self.line_tag:
            #     self.app.move(self.line_tag, event.x - self.startx, event.y - self.starty)
            self.current_x += event.x - self.startx
            self.current_y += event.y - self.starty

            self.startx = event.x
            self.starty = event.y
            self.app.itemconfig('障碍x', text=f'x:{self.current_x / 10 - 1.5:.2f}')
            self.app.itemconfig('障碍y', text=f'y:{self.current_y / 10 - 5:.2f}')

    def mouseup(self, event):
        # set_frame_stare(True)
        dx = event.x - move_x.get()
        dy = event.y - move_y.get()
        self.lest_angle = self.angle
        if dx or dy:
            stack.append(('移动', (self.id,), (dx, dy)))
        if what.get() == 3 and self.temp_angle != self.angle:
            rotate_.append(self.angle)
            stack.append(("旋转", self))


class CreateTxt(T):

    def __str__(self):
        return f"障碍号:{self.txt}"

    def save(self):
        return {self.__str__(): T.save(self)}

    def load(self, **kwargs):
        T.load(self, **kwargs)
        self.create(kwargs.get('txt'))

    def create(self, txt):
        """
        创建障碍号
        :param txt: 要创建的字符串
        :return:
        """
        self.tag = "txt-" + self.index
        self.txt = txt
        # 字符串外圆圈的位置
        length = 7 + 2 * len(txt)
        circle = canvas.create_oval(self.current_x - length, self.current_y - length, self.current_x + length,
                                    self.current_y + length, tags=self.tag, fill='white')
        text = self.app.create_text(self.current_x, self.current_y, text=txt, tags=self.tag)

        self.id = text
        self.app.image_data.update({self.id: self})
        # 撤销记录
        stack.append(('创建', (text, circle), self))

        self.app.tag_bind(self.tag, "<Button-1>", partial(self.mousedown, self.tag))
        self.app.tag_bind(self.tag, "<B1-Motion>", partial(self.drag, self.tag))
        # self.app.tag_bind(tag, "<Button-2>", partial(self.pop, tag))
        self.app.tag_bind(self.tag, "<ButtonRelease-1>", self.mouseup)
        # self.mousedown(self.tag, [200, 100])


class CreateParameter(T):

    def __str__(self):
        return f'障碍备注:{self.txt}'

    def save(self):
        return {self.__str__(): T.save(self)}

    def load(self, **kwargs):
        T.load(self, **kwargs)
        self.create(kwargs.get('txt'))

    def create(self, txt):
        """
        创建障碍备注
        :param txt: 备注字符串
        :return:
        """
        self.txt = txt
        self.tag = "parameter-" + self.index
        text = self.app.create_text(self.current_x, self.current_y, text=txt, tags=('parameter', self.tag))
        self.id = text
        self.app.image_data.update({self.id: self})
        stack.append(('创建', text, self))
        self.app.tag_bind(self.tag, "<Button-1>", partial(self.mousedown, self.tag))
        self.app.tag_bind(self.tag, "<B1-Motion>", partial(self.drag, text))
        # self.app.tag_bind(tag, "<Button-2>", partial(self.pop, tag))
        self.app.tag_bind(self.tag, "<ButtonRelease-1>", self.mouseup)
        # self.mousedown(self.tag, [200, 100])


class CreateImg(T):

    def __str__(self):
        return f"障碍组件:{self.obstacle}-{self.index}"

    def __init__(self, app, index, obstacle=None):
        super(CreateImg, self).__init__(app, index)
        self.small_rect_size = 10
        self.var = None  # 旋转输入框
        self.img = None  # 图片
        self.frame_input = None  # 输入框列表
        self.img_path = None  # 图片路径
        self.img_obj = None  # 图片对象
        self.temp_path = None  # 临时路径
        self.img_file = None
        self.obstacle = obstacle  # 障碍类别
        self.focus = focus  # 聚焦对象
        self.info = []  # 输入框信息
        self.com_info = {}  # 组合障碍输入框内容
        self.state = {}  # 输入框状态
        self.name = ''  # 备注
        self.state_line = 0  # 辅助线状态
        self.width = 100
        self.height = 50
        self.rectangle = None  # 矩形
        self.drag_data = {"x": 0, "y": 0, "item": None}

    def save(self):
        """
        保存障碍信息
        :return:
        """
        t_dict = T.save(self)

        with open(self.img_path, 'rb') as image:
            data = image.read()
        img_obj = data_url.construct_data_url(
            mime_type='image/jpeg',
            base64_encode=True,
            data=data,
        )
        save_dict = {'img_path': self.img_path, 'img_obj': img_obj, 'obstacle': self.obstacle, 'name': self.name,
                     'state_line': self.state_line, 'info': self.info, 'com_info': self.com_info}
        return {self.__str__(): {**t_dict, **save_dict}}

    def load(self, **kwargs):
        T.load(self, **kwargs)

        img_url = kwargs.get('img_obj')
        self.info = kwargs.get('info')
        self.com_info = kwargs.get('com_info')
        self.state_line = kwargs.get('state_line')
        self.obstacle = kwargs.get('obstacle')
        self.name = kwargs.get('name')
        # self.state = kwargs.get('state')

        image_data = base64.b64decode(img_url.split(",")[1])
        image = Image.open(io.BytesIO(image_data))
        self.create(kwargs.get('img_path'), img_obj=image)
        self.to_rotate(self.tag, self.angle)

    def create(self, img_path, img_obj=None):
        self.tag = "img-" + self.index
        self.img_path = img_path
        self.img_obj = img_obj if img_obj else Image.open(self.img_path)
        self.width, self.height = self.img_obj.size
        self.img_file = ImageTk.PhotoImage(self.img_obj)
        # self.create_rectangle_at_angle(self.angle)
        img_id = self.app.create_image(self.current_x, self.current_y, image=self.img_file, tag=self.tag)
        self.id = img_id
        self.app.image_data.update({self.id: self})

        stack.append(('创建', img_id, self))
        self.app.tag_bind(self.tag, "<Button-1>", partial(self.mousedown, self.tag))
        self.app.tag_bind(self.tag, "<B1-Motion>", partial(self.drag, self.tag))
        # self.app.tag_bind(self.tag, "<Button-2>", partial(self.pop, self.tag))
        self.mousedown(self.tag, [200, 100])
        set_frame_stare(True)
        self.app.tag_bind(self.tag, "<ButtonRelease-1>", self.mouseup)

        # no_what.set(0)
        # set_color()

    def on_update(self):
        """
        初始化后会被调用，在这里绘制矩形
        :return: None
        """
        self.app.create_rectangle(-1, -1, -2, -2, tag='side', dash=3, outline='grey')

        for name in ('nw', 'w', 'sw', 'n', 's', 'ne', 'e', 'se'):
            self.app.create_rectangle(-1, -1, -2, -2, tag=name, outline='blue')

    def show(self, is_fill=False):
        """
        显示
        :param is_fill: 是否填充
        :return: None
        """
        width = self.width
        height = self.height
        self.app.coords('nw', 0, 0, 7, 7)
        self.app.coords('sw', 0, height - 8, 7, height - 1)
        self.app.coords('w', 0, (height - 7) / 2, 7, (height - 7) / 2 + 7)
        self.app.coords('n', (width - 7) / 2, 0, (width - 7) / 2 + 7, 7)
        self.app.coords('s', (width - 7) / 2, height - 8, (width - 7) / 2 + 7, height - 1)
        self.app.coords('ne', width - 8, 0, width - 1, 7)
        self.app.coords('se', width - 8, height - 8, width - 1, height - 1)
        self.app.coords('e', width - 8, (height - 7) / 2, width - 1, (height - 7) / 2 + 7)

    def mousedown(self, tag, event):
        """
        鼠标左键点击事件
        :param tag: tag
        :param event:
        :return:
        """
        T.mousedown(self, tag, event)
        self.butt()
        if what.get() == '3':
            self.temp_angle = self.angle
        if self.obstacle in ["oxer", "tirail", "four", "combination_ab", "combination_abc", 'water', 'live']:
            self.frame_input, button = self.focus.update(self, self.obstacle, info=self.info,
                                                         state=self.state, com_info=self.com_info)
            button.config(command=self.update_img)
        else:
            if frame_function.winfo_children()[0].winfo_children()[1].winfo_name() == '障碍编辑容器':
                frame_function.winfo_children()[0].winfo_children()[1].destroy()
        # self.draw_rectangles()
        self.drag_data["item"] = self.app.find_closest(event.x, event.y)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def draw_rectangles(self):
        """
        绘制主矩形和小矩形
        :return:
        """
        self.app.delete(self.tag + 'point')
        angle_rad = math.radians(-self.angle)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)

        # 计算主矩形坐标
        half_w = self.width / 2
        half_h = self.height / 2

        p1 = self.rotate_point(-half_w, -half_h, cos_angle, sin_angle)
        p2 = self.rotate_point(half_w, -half_h, cos_angle, sin_angle)
        p3 = self.rotate_point(half_w, half_h, cos_angle, sin_angle)
        p4 = self.rotate_point(-half_w, half_h, cos_angle, sin_angle)

        self.main_rect = self.app.create_polygon(
            p1[0] + self.current_x, p1[1] + self.current_y,
            p2[0] + self.current_x, p2[1] + self.current_y,
            p3[0] + self.current_x, p3[1] + self.current_y,
            p4[0] + self.current_x, p4[1] + self.current_y,
            fill="", outline="black", tags=(self.tag, self.tag + 'point', 'arc')
        )
        canvas.tag_lower(self.main_rect, self.id)

        # 计算小矩形坐标
        small_half = self.small_rect_size / 2
        small_offset = half_w + small_half - 10  # 增加保证金

        left_center_x = self.current_x - small_offset * cos_angle
        left_center_y = self.current_y - small_offset * sin_angle

        right_center_x = self.current_x + small_offset * cos_angle
        right_center_y = self.current_y + small_offset * sin_angle

        self.left_rect = self.create_rotated_rect(left_center_x, left_center_y, small_half, angle_rad, "red")
        self.right_rect = self.create_rotated_rect(right_center_x, right_center_y, small_half, angle_rad, "green")
        canvas.tag_lower(self.left_rect, self.id)
        canvas.tag_lower(self.right_rect, self.id)
        # self.app.tag_bind(self.left_rect, '<B1-Motion>', self.on_rect_drag)
        # self.app.tag_bind(self.right_rect, '<B1-Motion>', self.on_rect_drag)

    def on_rect_drag(self, event):
        rect = self.app.find_withtag(ttk.CURRENT)[0]
        x, y = event.x, event.y
        dx, dy = x - self.drag_data['x'], y - self.drag_data['y']

        # 移动矩形
        self.app.move(rect, dx, dy)
        self.drag_data = {'x': x, 'y': y}

        # 更新矩形中心点
        if rect == self.rect1:
            self.rect1_center = self._get_center(self.rect1)
        else:
            self.rect2_center = self._get_center(self.rect2)

        # 更新弧线
        self._update_arc(self.rect1_center, self.rect2_center)

    def create_rotated_rect(self, center_x, center_y, half_size, angle_rad, color):
        """
        绘制旋转矩形
        :param center_x:
        :param center_y:
        :param half_size:
        :param angle_rad:
        :param color:
        :return:
        """
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)

        p1 = self.rotate_point(-half_size, -half_size, cos_angle, sin_angle)
        p2 = self.rotate_point(half_size, -half_size, cos_angle, sin_angle)
        p3 = self.rotate_point(half_size, half_size, cos_angle, sin_angle)
        p4 = self.rotate_point(-half_size, half_size, cos_angle, sin_angle)

        return self.app.create_polygon(
            p1[0] + center_x, p1[1] + center_y,
            p2[0] + center_x, p2[1] + center_y,
            p3[0] + center_x, p3[1] + center_y,
            p4[0] + center_x, p4[1] + center_y,
            fill=color, tags=(self.tag, self.tag + 'point', 'arc')
        )

    def rotate_point(self, x, y, cos_angle, sin_angle):
        """
        旋转坐标点
        :param x:
        :param y:
        :param cos_angle:
        :param sin_angle:
        :return:
        """
        return x * cos_angle - y * sin_angle, x * sin_angle + y * cos_angle

    # def create_rectangle_at_angle(self, angle):
    #     """
    #     根据给定的角度创建一个旋转后的矩形，并在画布上绘制该矩形
    #     :param angle: 矩形的旋转角度
    #     :return:
    #     """
    #
    #     radians = math.radians(angle)
    #     cos_val = math.cos(radians)
    #     sin_val = math.sin(radians)
    #
    #     half_width = self.width / 2
    #     half_height = self.height / 2
    #
    #     points = [
    #         (-half_width, -half_height),
    #         (half_width, -half_height),
    #         (half_width, half_height),
    #         (-half_width, half_height),
    #     ]
    #
    #     rotated_points = [
    #         (
    #             self.current_x + x * cos_val - y * sin_val,
    #             self.current_y + x * sin_val + y * cos_val
    #         )
    #         for x, y in points
    #     ]
    #
    #     for name in ('w', 'e',):
    #         self.app.create_rectangle(0, 0, 0, 0, tag=(name, 'point'), outline='blue')
    #         self.app.tag_bind(name, "<ButtonRelease-1>", self.mouseup)
    #
    #     # print(rotated_points, 'rotated_points')
    #
    #     self.app.coords('w', rotated_points[0][0],
    #                     ((rotated_points[2][1] - rotated_points[0][1]) / 2 + rotated_points[0][1]),
    #                     rotated_points[0][0] + 7,
    #                     (rotated_points[2][1] - rotated_points[0][1]) / 2 + 7 + rotated_points[0][1])
    #     self.app.coords('e', rotated_points[1][0],
    #                     (rotated_points[3][1] - rotated_points[1][1]) / 2 + rotated_points[1][1],
    #                     rotated_points[1][0] - 7,
    #                     (rotated_points[3][1] - rotated_points[1][1]) / 2 + 7 + rotated_points[1][1])
    #     if self.rectangle:
    #         flat_points = [coord for point in rotated_points for coord in point]
    #         # print(flat_points, 'flat_points')
    #         self.app.coords(self.rectangle, flat_points)
    #         return
    #     self.rectangle = self.app.create_polygon(rotated_points, fill='', outline="black", tags=self.tag)

    def arc(self):
        x1, y1, x2, y2 = self.app.coords('w')
        rect1_center = (x1 + x2) / 2, (y1 + y2) / 2
        x1, y1, x2, y2 = self.app.coords('e')
        rect2_center = (x1 + x2) / 2, (y1 + y2) / 2
        self.arc = self._create_arc(rect1_center, rect2_center)

    def _create_arc(self, start, end):
        """
        绘制弧线
        :param start: 矩形1的中心坐标
        :param end: 矩形2的中心坐标
        :return:
        """
        x1, y1 = start
        x2, y2 = end

        # 计算两个点之间的中点
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

        # 计算控制点，使弧线在任意角度都能正确连接
        dx, dy = x2 - x1, y2 - y1
        distance = math.sqrt(dx ** 2 + dy ** 2)
        offset = distance / 2

        if y1 < y2:
            ctrl_x, ctrl_y = cx - dy / 2, cy + dx / 2
        else:
            ctrl_x, ctrl_y = cx + dy / 2, cy - dx / 2

        return self.canvas.create_line(x1, y1, ctrl_x, ctrl_y, x2, y2, smooth=True)

    def guide(self):
        """
        辅助线
        :return:
        """

        # 计算两个点的坐标，这两个点分别位于当前点的角度方向上，距离当前点150个单位长度
        x1 = self.current_x + 150 * math.cos(math.radians(-self.angle))
        y1 = self.current_y + 150 * math.sin(math.radians(-self.angle))
        x2 = self.current_x - 150 * math.cos(math.radians(-self.angle))
        y2 = self.current_y - 150 * math.sin(math.radians(-self.angle))

        self.line_tag = self.app.create_line(x1, y1, x2, y2, dash=(5, 3), tags=self.tag)

    def update_img(self):
        """
        从输入框中获取值更新图片
        :return:
        """
        self.info.clear()
        for i in self.frame_input:
            if self.obstacle == "combination_ab" or self.obstacle == "combination_abc":
                if is_number(i.get()):
                    self.com_info[i.getname()] = i.get()
                    self.state[i.getname()] = i['state']
                    if self.state[i.getname()] == "disabled":
                        self.com_info[i.getname()] = "0"
                    continue
                elif i.get() == '':
                    self.com_info[i.getname()] = '0'
                    self.state[i.getname()] = i['state']
                    continue
                else:
                    messagebox.showerror("错误", "请输入数字")
                    i.delete(0, 'end')
                    return
            elif self.obstacle == 'live':
                if is_number(i.get()):
                    self.com_info[i.winfo_name()] = i.get()
                    self.state[i.winfo_name()] = i['state']
                    if self.state[i.winfo_name()] == "disabled":
                        self.com_info[i.winfo_name()] = "0"
                    continue
                elif i.get() == '':
                    self.com_info[i.winfo_name()] = '0'
                    self.state[i.winfo_name()] = i['state']
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
        if self.obstacle == "oxer" or self.obstacle == "tirail" or self.obstacle == "four":
            val = float(self.info[0]) * 10
            self.img_update(val, oxer=self.obstacle)
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
            a, a_b, b = round(a) + 5 if a else 0, round(a_b), round(b) + 5 if b else 0,
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
            a, a_b, b, b_c, c = (round(a) + 5 if a else 0,
                                 round(a_b),
                                 round(b) + 5 if b else 0,
                                 round(b_c),
                                 round(c) + 5 if c else 0)
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

    def img_update(self, m, oxer=None):
        self.img_path = merge(int(m), oxer=oxer)
        self.img = Image.open(self.img_path)
        self.temp_path = ImageTk.PhotoImage(self.img)
        self.app.itemconfig(self.tag, image=self.temp_path)

    @staticmethod
    def create_frame():
        # 旋转、备注编辑主容器
        frame_edit = ttk.Frame(frame_job, name='旋转、备注', bootstyle="info")
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

        ttk.Label(frame_focus_x_ladel, text="旋转：").pack()
        self.var = ttk.StringVar()
        self.var.set(str(int(self.angle)))
        Entry(frame_focus_x_ent, textvariable=self.var, width=5, undo=True).pack()

        ttk.Button(frame_focus_x_but, text="确认", command=partial(self.to_rotate, self.tag, self.var),
                   bootstyle=CONFIRM_STYLE).pack()
        ttk.Label(frame_focus_z_ladel, text="备注：").pack()
        var_name = ttk.StringVar(value=self.name if self.name else self.tag)
        Entry(frame_focus_z_ent, textvariable=var_name, width=5).pack()
        ttk.Button(frame_focus_z_but, text="确认", command=partial(self.set_name, var_name),
                   bootstyle=CONFIRM_STYLE).pack()
        w = 6 if sys_name == 'Darwin' else 10
        ttk.Button(frame_command, text='障碍辅助线', command=self.bar_aux, name='障碍辅助线', width=w,
                   bootstyle=BUTTON_STYLE).grid(row=3, column=0)
        ttk.Button(frame_mea_com, text='弧线', command=self.arc, name='弧线', width=w,
                   bootstyle=BUTTON_STYLE).grid(row=1, column=0)

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
            # 定义点的坐标
            origin = (self.current_x, self.current_y)
            start = (self.startx, self.starty)
            end = (event.x, event.y)

            origin_start = (start[0] - origin[0], start[1] - origin[1])
            origin_end = (end[0] - origin[0], end[1] - origin[1])

            # 计算向量 AB 和 AC 的角度
            angle_AB = math.atan2(origin_start[1], origin_start[0])
            angle_AC = math.atan2(origin_end[1], origin_end[0])

            # 计算夹角
            angle = self.lest_angle + math.degrees(angle_AB - angle_AC)

            # 确保角度在 0 到 360 度范围内
            if angle < 0:
                angle += 360

            self.to_rotate(self.id, angle, state=False)

            dx = event.x - self.drag_data["x"]
            dy = event.y - self.drag_data["y"]
            self.drag_data["x"] = event.x
            self.drag_data["y"] = event.y

            if self.drag_data["item"]:

                item = self.drag_data["item"][0]
                if item == self.main_rect:
                    self.current_x += dx
                    self.current_y += dy
                    self.draw_rectangles()
                else:
                    # center_x_diff = event.x - self.current_x
                    # center_y_diff = event.y - self.current_y
                    # self.angle = math.degrees(math.atan2(center_y_diff, center_x_diff))
                    self.draw_rectangles()

    def mouseup(self, event):
        """
        鼠标松开
        :param event:
        :return:
        """
        T.mouseup(self, event)
        if what.get() == 3:
            self.drag_data["item"] = None

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
        # self.app.delete(self.rectangle)
        # self.create_rectangle_at_angle(-angle)
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
        img2 = img2.rotate(angle, expand=True, resample=Image.BICUBIC)
        # 更强的平滑滤镜
        # img2 = img2.filter(ImageFilter.SMOOTH_MORE)
        # 锐化
        # img2 = img2.filter(ImageFilter.SHARPEN)
        # 细节增强
        # img2 = img2.filter(ImageFilter.DETAIL)
        return img2
