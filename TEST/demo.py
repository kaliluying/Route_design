import tkinter as tk
import math

# 创建主窗口
root = tk.Tk()

# 创建Canvas
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

# 创建矩形，初始位置为 (50, 50, 100, 100)，并给定一个标签 "rect"
rect = canvas.create_rectangle(50, 50, 100, 100, fill="blue", tags="rect")

# 固定的移动角度（以度为单位）
fixed_angle = 45  # 45度角


# 获取固定角度的单位方向向量
def get_unit_vector(angle):
    radians = math.radians(angle)
    dx = math.cos(radians)
    dy = math.sin(radians)
    return dx, dy


# 计算鼠标位置到矩形中心的距离，并按固定角度移动矩形
def move_rectangle(event):
    # 获取矩形的当前坐标
    coords = canvas.coords(rect)
    x1, y1, x2, y2 = coords
    rect_center_x = (x1 + x2) / 2
    rect_center_y = (y1 + y2) / 2

    # 计算鼠标位置与矩形中心的差值
    dx_mouse = event.x - rect_center_x
    dy_mouse = event.y - rect_center_y

    # 获取固定角度的单位方向向量
    unit_dx, unit_dy = get_unit_vector(fixed_angle)

    # 计算在固定角度上的投影距离
    projection_length = dx_mouse * unit_dx + dy_mouse * unit_dy

    # 按照投影距离移动矩形
    canvas.move("rect", unit_dx * projection_length, unit_dy * projection_length)


# 绑定鼠标拖动事件
canvas.bind("<B1-Motion>", move_rectangle)

# 运行主循环
root.mainloop()
