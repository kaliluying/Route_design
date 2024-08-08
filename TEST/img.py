import tkinter as tk


class App:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=300)
        self.canvas.pack()

        # 在 Canvas 上添加一些图形项
        self.canvas.create_rectangle(50, 50, 150, 150, fill="blue", tags=("rectangle", "shape"))
        self.canvas.create_oval(200, 100, 300, 200, fill="red", tags=("oval", "shape"))

        # 绑定点击事件
        self.canvas.tag_bind("rectangle", "<Button-1>", self.on_rectangle_click)
        self.canvas.tag_bind("oval", "<Button-1>", self.on_oval_click)

        # 绑定鼠标滚动事件
        self.mouse_wheel_bound = True
        self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)

    def on_rectangle_click(self, event):
        print("矩形被点击")
        self.toggle_mouse_wheel_binding()

    def on_oval_click(self, event):
        print("椭圆被点击")
        self.toggle_mouse_wheel_binding()

    def on_mouse_wheel(self, event):
        if self.mouse_wheel_bound:
            print("鼠标滚动事件触发")

    def toggle_mouse_wheel_binding(self):
        self.mouse_wheel_bound = not self.mouse_wheel_bound
        if self.mouse_wheel_bound:
            self.canvas.bind("<MouseWheel>", self.on_mouse_wheel)
        else:
            self.canvas.unbind("<MouseWheel>")


# 创建主窗口并运行应用
root = tk.Tk()
app = App(root)
root.mainloop()
