import base64
import datetime
import io
import sys
from functools import partial

import data_url

from Common import *
from Tools import is_number, merge, oxer_obs_abc, obs_ab, remove_from_edit, water_wh, live_edit, Entry, update_arc_px, \
    update_px, compute_arc_length


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
        self.app.itemconfig('障碍x', text=f'x:{self.current_x / 10 - 1.5:.2f}')
        self.app.itemconfig('障碍y', text=f'y:{self.current_y / 10 - 5:.2f}')
        try:
            if choice_tup and not (min(choice_tup[0], choice_tup[2]) < event.x < max(choice_tup[0], choice_tup[2])
                                   and min(choice_tup[1], choice_tup[3]) < event.y < max(choice_tup[1], choice_tup[3])):
                self.app.delete('choice')
                choice_tup.clear()
                self.app.dtag('choice_start', 'choice_start')
        except Exception as e:
            print(f"{os.path.basename(__file__)}, line {sys._getframe().f_lineno}, {e}", e)
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
        set_cur(self.tag)
        self.app.lift(self.tag)

    def drag(self, tag, event):
        """
        鼠标拖动
        :param tag:
        :param event:
        :return:
        """
        # global choice_tup

        try:
            # 获取点击位置的 item id
            item_id = event.widget.find_closest(event.x, event.y)[0]
            # 获取该 item 的 tag
            tags = event.widget.gettags(item_id)
            if 'rect_arc' in tags:
                return
        except:
            pass

        if what.get() == 0 and not choice_tup:
            set_frame_stare(False)
            self.app.move(tag, event.x - self.startx, event.y - self.starty)
            # self.app.move(tag, event.x - self.startx, event.y - self.starty)
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
        """
        鼠标左键释放
        :param event:
        :return:
        """
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
        self.selected_rects = []
        self.small_rect_size = 10
        self.var = None  # 旋转输入框
        self.img = None  # 原始图片
        self.frame_input = None  # 输入框列表
        self.img_path = None  # 图片路径
        self.img_obj = None  # 操作图片对象
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
        self.arcs = []  # 弧线
        self.scale_ratio = 1.0  # 缩放比例

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
                     'state_line': self.state_line, 'info': self.info, 'com_info': self.com_info,
                     'scale_ratio': self.scale_ratio}
        return {self.__str__(): {**t_dict, **save_dict}}

    def load(self, **kwargs):
        T.load(self, **kwargs)

        img_url = kwargs.get('img_obj')
        self.info = kwargs.get('info')
        self.com_info = kwargs.get('com_info')
        self.state_line = kwargs.get('state_line')
        self.obstacle = kwargs.get('obstacle')
        self.name = kwargs.get('name')
        self.scale_ratio = kwargs.get('scale_ratio')
        # self.state = kwargs.get('state')

        image_data = base64.b64decode(img_url.split(",")[1])
        image = Image.open(io.BytesIO(image_data))
        self.create(kwargs.get('img_path'), img_obj=image)
        self.load_arc()
        self.to_rotate(self.tag, self.angle)

    def get_current_info(self):
        """
        获取当前障碍位置信息
        :return:
        """
        # bbox = self.app.bbox(self.tag)
        # print(self.app.coords(self.tag))
        # self.current_x = bbox[0] + ((bbox[2] - bbox[0]) / 2)
        # self.current_y = bbox[1] + ((bbox[3] - bbox[1]) / 2)
        self.current_x, self.current_y = self.app.coords(self.tag)
        # print(f"当前坐标:({self.current_x}, {self.current_y})")

    def create(self, img_path, img_obj=None):
        self.tag = "img-" + self.index
        self.img_path = img_path
        # self.img_obj = img_obj if img_obj else Image.open(self.img_path)
        # self.width, self.height = self.img_obj.size
        # self.img_file = ImageTk.PhotoImage(self.img_obj)
        self.img = Image.open(self.img_path)
        self.img_obj = img_obj if img_obj else Image.open(self.img_path)
        self.width, self.height = self.img.size
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

        if check_var.get():
            self.draw_rectangles()

        if self.obstacle == 'diy':
            self.zoom(event=None, load=True)

    def zoom(self, event, load=False):
        """
        放大缩小图片
        :param event:
        :return:
        """
        print(f"缩放比例:{self.scale_ratio}")
        if not load:
            if event.delta > 0:
                self.scale_ratio *= 1.1
            else:
                self.scale_ratio /= 1.1
        else:
            pass
        new_width = int(self.width * self.scale_ratio)
        new_height = int(self.height * self.scale_ratio)
        img_obj = Image.open(self.img_path)
        resized_image = img_obj.resize((new_width, new_height), Image.Resampling.LANCZOS)
        img2 = resized_image.convert('RGBA')
        self.img_obj = img2.rotate(self.angle, expand=True, resample=Image.BICUBIC)
        self.temp_path = ImageTk.PhotoImage(self.img_obj)
        canvas.itemconfig(self.id, image=self.temp_path)

    def mousedown(self, tag, event):
        """
        鼠标左键点击事件
        :param tag: tag
        :param event:
        :return:
        """
        try:
            # 获取点击位置的 item id
            item_id = event.widget.find_closest(event.x, event.y)[0]
            # 获取该 item 的 tag
            tags = event.widget.gettags(item_id)
            if 'rect_arc' in tags:
                return
        except:
            pass

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

    def drag(self, tag, event):
        """
        鼠标拖动
        :param tag:
        :param event:
        :return:
        """
        T.drag(self, tag, event)

        # 旋转图片
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
            if check_var.get():
                self.draw_rectangles()
                for arc, rect1, rect2, control_point in arc_list:
                    rect1_center = self._get_center(rect1)
                    rect2_center = self._get_center(rect2)

                    self._update_arc(arc, rect1_center, rect2_center, control_point, rect1, rect2)

        # 移动图片
        if what.get() == 0:
            for arc, rect1, rect2, control_point in arc_list:
                rect1_center = self._get_center(rect1)
                rect2_center = self._get_center(rect2)
                self._update_arc(arc, rect1_center, rect2_center, control_point, rect1, rect2)

    def load_arc(self):
        center_list = get_rect_center()
        for arc, rect1, rect2, control_point in arc_list:
            self.app.delete(arc)
        arc_list.clear()
        for arc, rect1, rect2, rect1_center, rect2_center, control_point in center_list:
            arc, control_point = self.create_arc(rect1_center, rect2_center, control_point)
            # new_arc = self.create_arc(rect1_center, rect2_center)
            arc_list.append((arc, rect1, rect2, control_point))
            # calculate_bezier_length(new_arc)

    def _get_center(self, rect):
        try:
            x1, y1, c_x, c_y, c_x2, c_y2, x2, y2 = self.app.coords(rect)
            return (x1 + x2) / 2, (y1 + y2) / 2
        except ValueError as e:
            print(f"{os.path.basename(__file__)}, line {sys._getframe().f_lineno}, {e}")

    def draw_rectangles(self):
        """
        绘制小矩形
        :return:
        """
        self.app.delete(self.tag + 'point')

        angle_rad = math.radians(-self.angle)
        cos_angle = math.cos(angle_rad)
        sin_angle = math.sin(angle_rad)

        half_w = self.width / 2

        # 计算小矩形坐标
        small_half = self.small_rect_size / 2

        # small_offset = half_w + small_half - 130  # 偏移量
        left_small_offset = half_w + small_half + 130  # 偏移量

        right_small_offset = half_w + small_half + 50  # 偏移量

        self.get_current_info()

        left_center_x = self.current_x - left_small_offset * cos_angle
        left_center_y = self.current_y - left_small_offset * sin_angle

        right_center_x = self.current_x + right_small_offset * cos_angle
        right_center_y = self.current_y + right_small_offset * sin_angle

        self.left_rect = self.create_rotated_rect(left_center_x, left_center_y, small_half, angle_rad, "red",
                                                  tag=self.tag + 'left_rect')
        self.right_rect = self.create_rotated_rect(right_center_x, right_center_y, small_half, angle_rad, "green",
                                                   tag=self.tag + 'right_rect')

        self.app.tag_bind(self.left_rect, '<ButtonRelease-1>',
                          partial(self.on_rect_click, self.left_rect, self.tag + 'left_rect'))
        self.app.tag_bind(self.right_rect, '<ButtonRelease-1>',
                          partial(self.on_rect_click, self.right_rect, self.tag + 'right_rect'))

    def on_rect_click(self, id, tag, event):
        global arc_click
        x1, y1, x2, y2, x3, y3, x4, y4 = self.app.coords(id)
        points = [(x1, y1), (x2, y2), (x3, y3), (x4, y4)]
        x_coords = [p[0] for p in points]
        y_coords = [p[1] for p in points]

        cx = sum(x_coords) / 4
        cy = sum(y_coords) / 4
        if what.get() == 0:
            if arc_click:
                start = get_arc_start()
                set_arc_end_obj(tag)
                arc_click = 0
                arc, control_points = self.create_arc(start, (cx, cy))
                # calculate_bezier_length(arc)
                rect1, rect2 = get_arc_start_obj(), tag
                arc_list.append((arc, rect1, rect2, control_points))

            else:
                set_arc_start((cx, cy))
                set_arc_start_obj(tag)
                arc_click = 1

    def create_arc(self, start, end, control_point=None):
        x1, y1 = start
        x2, y2 = end

        start_obj = get_arc_start_obj()
        end_obj = get_arc_end_obj()

        # TODO
        try:
            self.set_tangent_line(x1, y1, x2, y2, start_obj, end_obj)
        except:
            pass

        if control_point is None:
            ctrl1_x = x1 + (x2 - x1) / 3
            ctrl1_y = y1
            ctrl2_x = x1 + 2 * (x2 - x1) / 3
            ctrl2_y = y2
        else:
            ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y = control_point
        # if control_point is None:
        #     if y1 < y2:
        #         ctrl_x, ctrl_y = cx + dy / 2, cy - dx / 2
        #     else:
        #         ctrl_x, ctrl_y = cx - dy / 2, cy + dx / 2
        # else:
        #     print(sys._getframe().f_lineno)
        #     ctrl_x, ctrl_y = control_point

        # ctrl_x, ctrl_y = cx + dy / 2, cy - dx / 2

        # arc = self.app.create_line(x1, y1, ctrl_x, ctrl_y, x2, y2, smooth=True, width=2, dash=(5, 3), tags='arc')
        arc = self.app.create_line(x1, y1, ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y, x2, y2, smooth=True, width=1,
                                   dash=(5, 3), tags='arc')

        self.app.tag_bind(arc, '<ButtonPress-1>', lambda event, arc=arc: self.on_arc_click(event, arc))
        self.app.tag_bind(arc, '<B1-Motion>', lambda event, arc=arc: self.on_arc_drag(event, arc))

        length = compute_arc_length(arc)
        update_px(length / 10)

        return arc, (ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y)

    def _update_arc(self, arc, start, end, control_point, rect1, rect2):

        pre_length = compute_arc_length(arc)
        self.app.coords(arc, *self._calculate_arc_coords(start, end, rect1, rect2, control_point=control_point))
        current_length = compute_arc_length(arc)
        update_arc_px(current_length, pre_length)

    def _calculate_arc_coords(self, start, end, rect1, rect2, control_point=None):
        x1, y1 = start
        x2, y2 = end

        # TODO
        try:
            self.set_tangent_line(x1, y1, x2, y2, rect1, rect2, tangent_start=True)
        except:
            pass

        if control_point is None:
            ctrl1_x = x1 + (x2 - x1) / 3
            ctrl1_y = y1
            ctrl2_x = x1 + 2 * (x2 - x1) / 3
            ctrl2_y = y2

            # ctrl1_x = x1 + 100
            # ctrl1_y = y1
            # ctrl2_x = x2 - 100
            # ctrl2_y = y2
        else:
            ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y = control_point

        return x1, y1, ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y, x2, y2

    def set_tangent_line(self, x1, y1, x2, y2, start_obj, end_obj, tangent_start=None):
        if 'left' in start_obj:
            left_obj = start_obj.split('left')[0]
            left_x, left_y = x1, y1
        elif 'left' in end_obj:
            left_obj = end_obj.split('left')[0]
            left_x, left_y = x2, y2
        if 'right' in start_obj:
            right_x, right_y = x1, y1
            right_obj = start_obj.split('right')[0]
        elif 'right' in end_obj:
            right_x, right_y = x2, y2
            right_obj = end_obj.split('right')[0]

        right_angle = self.app.image_data[self.app.find_withtag(right_obj)[0]].angle
        right_center_x = right_x - 50 * math.cos(math.radians(-right_angle))
        right_center_y = right_y - 50 * math.sin(math.radians(-right_angle))

        left_angle = self.app.image_data[self.app.find_withtag(left_obj)[0]].angle
        left_center_x = left_x + 130 * math.cos(math.radians(-left_angle))
        left_center_y = left_y + 130 * math.sin(math.radians(-left_angle))
        if tangent_start:
            self.app.coords('left_tangent_line' + self.index, left_center_x, left_center_y, left_x, left_y)
            self.app.coords('right_tangent_line' + self.index, right_x, right_y, right_center_x, right_center_y)
        else:
            left = self.app.create_line(left_center_x, left_center_y, left_x, left_y, dash=(5, 3),
                                        # tags=(self.tag, self.tag + 'point', 'rect_arc', self.tag + 'left_rect')
                                        tags=(left_obj, 'tangent_line', 'left_tangent_line' + self.index)
                                        )

            right = self.app.create_line(right_x, right_y, right_center_x, right_center_y, dash=(5, 3),
                                         # tags=(self.tag, self.tag + 'point', 'rect_arc', self.tag + 'right_rect')
                                         tags=(right_obj, 'tangent_line', 'right_tangent_line' + self.index)
                                         )
            cut_point_list.append((left, right))

    def on_arc_click(self, event, arc):
        """
        点击弧线
        :param event:
        :param arc:
        :return:
        """
        self.current_arc = arc
        self.drag_start = event.x, event.y

    def on_arc_drag(self, event, arc):
        """
        拖动弧线
        :param event:
        :param arc:
        :return:
        """
        global px
        if arc == self.current_arc and check_var.get():
            set_frame_stare(False)
            x, y = event.x, event.y
            dx, dy = x - self.drag_start[0], y - self.drag_start[1]

            coords = self.app.coords(arc)

            x1, y1, ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y, x2, y2 = coords

            ctrl1_x += dx / 3
            ctrl1_y += dy / 3
            ctrl2_x += dx / 3
            ctrl2_y += dy / 3

            # ctrl1_x = (2 * x1 + x2) / 3
            # ctrl1_y = (2 * y1 + y2) / 3
            # ctrl2_x = (x1 + 2 * x2) / 3
            # ctrl2_y = (y1 + 2 * y2) / 3

            pre_length = compute_arc_length(arc)
            self.app.coords(arc, x1, y1, ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y, x2, y2)
            current_length = compute_arc_length(arc)
            update_arc_px(current_length, pre_length)
            for i, (a, rect1, rect2, _) in enumerate(arc_list):
                if a == arc:
                    arc_list[i] = (arc, rect1, rect2, (ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y))
                    rect1_center = self._get_center(rect1)
                    rect2_center = self._get_center(rect2)
                    self._update_arc(arc, rect1_center, rect2_center, (ctrl1_x, ctrl1_y, ctrl2_x, ctrl2_y), rect1,
                                     rect2)
                    break
            self.drag_start = x, y

    def create_rotated_rect(self, center_x, center_y, half_size, angle_rad, color, tag):
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
            fill=color, tags=(self.tag, self.tag + 'point', 'rect_arc', tag)
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
        if self.obstacle == "tirail" or self.obstacle == "four":
            val = float(self.info[0]) * 10
            self.img_update(val, oxer=self.obstacle)
        elif self.obstacle == "oxer":
            val = float(self.info[0]) / 10
            self.img_update(val, oxer=self.obstacle)
        elif self.obstacle == "combination_ab":
            temp = {}
            for key, val in self.com_info.items():
                if key.count('_') == 2 and val != '0':
                    temp[key] = float(val) * 10
                elif key.count('_') == 1 and val != '0' and self.state[key].__str__() == "normal":
                    temp[key] = float(val) / 10
                else:
                    temp[key] = 0
            a, a_b, b = temp.values()
            a, a_b, b = round(a), round(a_b), round(b)
            self.img_path = obs_ab(a, b, a_b)
            self.img_obj = Image.open(self.img_path)
            self.img = self.img_obj
            self.temp_path = ImageTk.PhotoImage(self.img_obj)
            self.app.itemconfig(self.tag, image=self.temp_path)
        elif self.obstacle == "combination_abc":
            temp = {}
            for key, val in self.com_info.items():
                if key.count('_') == 2 and val != '0':
                    temp[key] = float(val) * 10
                elif key.count('_') == 1 and val != '0' and self.state[key].__str__() == "normal":
                    temp[key] = float(val) / 10
                else:
                    temp[key] = 0
            a, a_b, b, b_c, c = temp.values()
            a, a_b, b, b_c, c = (round(a),
                                 round(a_b),
                                 round(b),
                                 round(b_c),
                                 round(c))
            self.img_path = oxer_obs_abc(a, b, c, a_b, b_c)
            self.img_obj = Image.open(self.img_path)
            self.img = self.img_obj
            self.temp_path = ImageTk.PhotoImage(self.img_obj)
            self.app.itemconfig(self.tag, image=self.temp_path)
        elif self.obstacle == 'water':
            w = int(float(self.info[0]) * 10)
            h = int(float(self.info[1]) * 10)
            self.img_path = water_wh(w, h)
            self.img_obj = Image.open(self.img_path)
            self.img = self.img_obj
            self.temp_path = ImageTk.PhotoImage(self.img_obj)
            self.app.itemconfig(self.tag, image=self.temp_path)
        elif self.obstacle == 'live':
            w = int(float(self.com_info['water_w_ent']) * 10)
            h = int(float(self.com_info['water_h_ent']) * 10)
            self.img_path = live_edit(w, h)
            self.img_obj = Image.open(self.img_path)
            self.img = self.img_obj
            self.temp_path = ImageTk.PhotoImage(self.img_obj)
            self.app.itemconfig(self.tag, image=self.temp_path)
        self.to_rotate(self.tag, self.angle)

    def img_update(self, m, oxer=None):
        self.img_path = merge(int(m), oxer=oxer)
        print(self.img_path)
        self.img_obj = Image.open(self.img_path)
        self.img = self.img_obj
        self.temp_path = ImageTk.PhotoImage(self.img_obj)
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

    def bar_aux(self):
        # if self.obstacle in ["oxer", "tirail", "combination_ab", "combination_abc", 'monorail']:
        if self.state_line:
            self.state_line = 0
            self.app.delete(self.line_tag)
        else:
            self.state_line = 1

            # 辅助线
            self.get_current_info()
            self.guide()
            set_line(self.line_tag)

    def set_state(self):
        self.app.lower(self.tag)
        self.app.lower("watermark")

    def set_name(self, name):
        self.name = name.get()

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
        self.img_obj = self.rotate_bound(angle)
        self.temp_path = ImageTk.PhotoImage(self.img_obj)
        canvas.itemconfig(self.id, image=self.temp_path)
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
        img = self.img

        if self.obstacle == 'diy':
            new_width = int(self.width * self.scale_ratio)
            new_height = int(self.height * self.scale_ratio)
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        img2 = img.convert('RGBA')
        img2 = img2.rotate(angle, expand=True, resample=Image.BICUBIC)
        # 更强的平滑滤镜
        # img2 = img2.filter(ImageFilter.SMOOTH_MORE)
        # 锐化
        # img2 = img2.filter(ImageFilter.SHARPEN)
        # 细节增强
        # img2 = img2.filter(ImageFilter.DETAIL)
        return img2
