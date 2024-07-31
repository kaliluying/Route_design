import tkinter as tk


def find_tags_at_position(canvas, x, y):
    # 查找与指定坐标重叠的图形项
    items = canvas.find_overlapping(x, y, x, y)
    tags = []
    for item in items:
        # 获取每个图形项的 tags
        item_tags = canvas.gettags(item)
        tags.extend(item_tags)
    return tags


# 创建主窗口
root = tk.Tk()

# 创建 Canvas 组件
canvas = tk.Canvas(root, width=400, height=300)
canvas.pack()

# 在 Canvas 上添加一些图形项，并为其添加 tags
canvas.create_rectangle(50, 50, 150, 150, fill="blue", tags=("rectangle", "shape"))
canvas.create_oval(200, 100, 300, 200, fill="red", tags=("oval", "shape"))


# 定义一个函数，在点击 Canvas 时查找并打印 tags
def on_canvas_click(event):
    x, y = event.x, event.y
    tags = find_tags_at_position(canvas, x, y)
    print(f"点击位置 ({x}, {y}) 的 tags: {tags}")


# 绑定点击事件
canvas.bind("<Button-1>", on_canvas_click)

# 运行主循环
root.mainloop()
