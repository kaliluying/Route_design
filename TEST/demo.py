import tkinter as tk


def create_grid(canvas, grid_size, line_distance):
    # 创建水平线
    for y in range(0, grid_size, line_distance):
        canvas.create_line(0, y, grid_size, y, fill="black")

    # 创建垂直线
    for x in range(0, grid_size, line_distance):
        canvas.create_line(x, 0, x, grid_size, fill="black")


# 创建主窗口
root = tk.Tk()
root.title("Canvas Grid")

# 创建Canvas组件
canvas = tk.Canvas(root, width=400, height=400, bg="white")
canvas.pack()

# 创建网格
create_grid(canvas, 400, 20)

# 运行主循环
root.mainloop()
