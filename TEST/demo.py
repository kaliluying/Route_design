import tkinter as tk
from math import cos, sin, radians, atan2, degrees


class DraggableRectangles:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        # 定义初始参数
        self.rect_width = 100
        self.rect_height = 60
        self.small_rect_size = 20
        self.center_x = 400
        self.center_y = 300
        self.angle = 0

        # 绘制主矩形和小矩形
        self.draw_rectangles()

        # Bind mouse events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

        self.drag_data = {"x": 0, "y": 0, "item": None}

    def draw_rectangles(self):
        """
        绘制主矩形和小矩形
        :return:
        """
        self.canvas.delete("all")
        angle_rad = radians(self.angle)
        cos_angle = cos(angle_rad)
        sin_angle = sin(angle_rad)

        # 计算主矩形坐标
        half_w = self.rect_width / 2
        half_h = self.rect_height / 2

        p1 = self.rotate_point(-half_w, -half_h, cos_angle, sin_angle)
        p2 = self.rotate_point(half_w, -half_h, cos_angle, sin_angle)
        p3 = self.rotate_point(half_w, half_h, cos_angle, sin_angle)
        p4 = self.rotate_point(-half_w, half_h, cos_angle, sin_angle)

        self.main_rect = self.canvas.create_polygon(
            p1[0] + self.center_x, p1[1] + self.center_y,
            p2[0] + self.center_x, p2[1] + self.center_y,
            p3[0] + self.center_x, p3[1] + self.center_y,
            p4[0] + self.center_x, p4[1] + self.center_y,
            fill="blue"
        )

        # 计算小矩形坐标
        small_half = self.small_rect_size / 2
        small_offset = half_w + small_half + 10  # 增加保证金

        left_center_x = self.center_x - small_offset * cos_angle
        left_center_y = self.center_y - small_offset * sin_angle

        right_center_x = self.center_x + small_offset * cos_angle
        right_center_y = self.center_y + small_offset * sin_angle

        self.left_rect = self.create_rotated_rect(left_center_x, left_center_y, small_half, angle_rad, "red")
        self.right_rect = self.create_rotated_rect(right_center_x, right_center_y, small_half, angle_rad, "green")

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
        cos_angle = cos(angle_rad)
        sin_angle = sin(angle_rad)

        p1 = self.rotate_point(-half_size, -half_size, cos_angle, sin_angle)
        p2 = self.rotate_point(half_size, -half_size, cos_angle, sin_angle)
        p3 = self.rotate_point(half_size, half_size, cos_angle, sin_angle)
        p4 = self.rotate_point(-half_size, half_size, cos_angle, sin_angle)

        return self.canvas.create_polygon(
            p1[0] + center_x, p1[1] + center_y,
            p2[0] + center_x, p2[1] + center_y,
            p3[0] + center_x, p3[1] + center_y,
            p4[0] + center_x, p4[1] + center_y,
            fill=color
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

    def on_click(self, event):
        """
        鼠标点击事件
        :param event:
        :return:
        """
        self.drag_data["item"] = self.canvas.find_closest(event.x, event.y)
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

    def on_drag(self, event):
        """
        鼠标拖动事件
        :param event:
        :return:
        """
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y

        if self.drag_data["item"]:
            item = self.drag_data["item"][0]
            if item == self.main_rect:
                self.center_x += dx
                self.center_y += dy
                self.draw_rectangles()
            else:
                center_x_diff = event.x - self.center_x
                center_y_diff = event.y - self.center_y
                self.angle = degrees(atan2(center_y_diff, center_x_diff))
                self.draw_rectangles()

    def on_release(self, event):
        """
        鼠标释放事件
        :param event:
        :return:
        """
        self.drag_data["item"] = None


root = tk.Tk()
app = DraggableRectangles(root)
root.mainloop()
