import tkinter as tk


class App:
    def __init__(self, root):
        self.canvas = tk.Canvas(root, width=400, height=400)
        self.canvas.pack()

        # 创建两个矩形并分别赋予不同的标签
        self.left_rect = self.canvas.create_rectangle(50, 50, 150, 150, fill="blue", tags="left_rect_tag")
        self.right_rect = self.canvas.create_rectangle(250, 50, 350, 150, fill="green", tags="right_rect_tag")

        # 为两个矩形绑定拖动事件
        self.canvas.tag_bind("left_rect_tag", '<B1-Motion>', self.rect_move)
        self.canvas.tag_bind("right_rect_tag", '<B1-Motion>', self.rect_move)

    def rect_move(self, event):
        # 获取触发事件的标签
        tags = self.canvas.gettags("current")

        if "left_rect_tag" in tags:
            print("Moving left rectangle")
        elif "right_rect_tag" in tags:
            print("Moving right rectangle")

        # 获取当前对象的坐标
        x, y = event.x, event.y
        self.canvas.coords("current", x - 50, y - 50, x + 50, y + 50)


# 创建主窗口
root = tk.Tk()
app = App(root)

# 运行主循环
root.mainloop()
