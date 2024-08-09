import tkinter as tk

class App:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=400, height=300)
        self.canvas.pack()

        # 在 Canvas 上添加一些图形项
        self.canvas.create_rectangle(50, 50, 150, 150, fill="blue", tags=("shape", "rectangle1"))
        self.canvas.create_rectangle(200, 50, 300, 150, fill="green", tags=("shape", "rectangle2"))
        self.canvas.create_oval(50, 200, 150, 300, fill="red", tags=("shape", "oval1"))
        self.canvas.create_oval(200, 200, 300, 300, fill="yellow", tags=("shape", "oval2"))

        # 获取具有相同 tag 的多个图形项的坐标位置
        self.get_items_with_tag("shape")

    def get_items_with_tag(self, tag):
        # 获取所有具有指定 tag 的图形项
        items = self.canvas.find_withtag(tag)
        if items:
            for item in items:
                # 获取每个图形项的边界框
                bbox = self.canvas.bbox(item)
                x1, y1, x2, y2 = bbox
                print(f"图形项 {item} 的坐标位置: 左上角 ({x1}, {y1}), 右下角 ({x2}, {y2})")
        else:
            print(f"没有找到具有 tag '{tag}' 的图形项")

# 创建主窗口并运行应用
root = tk.Tk()
app = App(root)
root.mainloop()
