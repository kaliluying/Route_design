import tkinter as tk
import math


class ConnectNodesApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=600, bg='white')
        self.canvas.pack()

        # 画两个矩形
        self.rect1 = self.canvas.create_rectangle(100, 200, 200, 300, outline='black', fill='white')
        self.rect2 = self.canvas.create_rectangle(500, 300, 600, 400, outline='black', fill='white')

        # 获取矩形中心点
        self.rect1_center = self._get_center(self.rect1)
        self.rect2_center = self._get_center(self.rect2)

        # 绘制初始弧线
        self.arc = self._create_arc(self.rect1_center, self.rect2_center)

        # 绑定事件
        self.canvas.tag_bind(self.rect1, '<ButtonPress-1>', self.on_rect_click)
        self.canvas.tag_bind(self.rect2, '<ButtonPress-1>', self.on_rect_click)
        self.canvas.tag_bind(self.rect1, '<B1-Motion>', self.on_rect_drag)
        self.canvas.tag_bind(self.rect2, '<B1-Motion>', self.on_rect_drag)

    def _get_center(self, rect):
        # 获取矩形的中心点
        x1, y1, x2, y2 = self.canvas.coords(rect)
        return (x1 + x2) / 2, (y1 + y2) / 2

    def _create_arc(self, start, end):
        # 创建连接两个点的弧线
        x1, y1 = start
        x2, y2 = end

        # 计算两个点之间的中点
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

        # 计算控制点，使弧线在任意角度都能正确连接
        dx, dy = x2 - x1, y2 - y1
        if y1 < y2:
            ctrl_x, ctrl_y = cx - dy / 2, cy + dx / 2
        else:
            ctrl_x, ctrl_y = cx + dy / 2, cy - dx / 2

        return self.canvas.create_line(x1, y1, ctrl_x, ctrl_y, x2, y2, smooth=True, width=2)

    def _update_arc(self, start, end):
        # 更新弧线
        self.canvas.delete(self.arc)
        self.arc = self._create_arc(start, end)

    def on_rect_click(self, event):
        # 处理矩形点击事件
        self.drag_data = {'x': event.x, 'y': event.y}
        print(self.drag_data)

    def on_rect_drag(self, event):
        # 处理矩形拖动事件
        rect = self.canvas.find_withtag(tk.CURRENT)[0]
        x, y = event.x, event.y
        dx, dy = x - self.drag_data['x'], y - self.drag_data['y']

        # 移动矩形
        self.canvas.move(rect, dx, dy)
        self.drag_data = {'x': x, 'y': y}

        # 更新矩形中心点
        if rect == self.rect1:
            self.rect1_center = self._get_center(self.rect1)
        else:
            self.rect2_center = self._get_center(self.rect2)

        # 更新弧线
        self._update_arc(self.rect1_center, self.rect2_center)


if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectNodesApp(root)
    root.mainloop()
