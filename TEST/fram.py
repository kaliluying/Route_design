import tkinter as tk


def draw_bezier_quadratic(canvas, p0, p1, p2, steps=100):
    for i in range(steps):
        t = i / steps
        x = (1 - t) * (1 - t) * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0]
        y = (1 - t) * (1 - t) * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]
        canvas.create_oval(x, y, x + 1, y + 1, fill='black')


def draw_bezier_cubic(canvas, p0, p1, p2, p3, steps=100):
    for i in range(steps):
        t = i / steps
        x = (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 * p3[0]
        y = (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 * p3[1]
        canvas.create_oval(x, y, x + 1, y + 1, fill='black')


root = tk.Tk()
root.title("贝塞尔曲线")

canvas = tk.Canvas(root, width=400, height=400, bg='white')
canvas.pack()

# 绘制二次贝塞尔曲线
p0 = (50, 300)
p1 = (200, 50)
p2 = (350, 300)
draw_bezier_quadratic(canvas, p0, p1, p2)

# 绘制三次贝塞尔曲线
p0 = (50, 150)
p1 = (150, 50)
p2 = (250, 250)
p3 = (350, 150)
draw_bezier_cubic(canvas, p0, p1, p2, p3)

root.mainloop()
