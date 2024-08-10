import tkinter as tk


def first_function(event):
    print("First function called!")


def second_function(event):
    print("Second function called!")


root = tk.Tk()
canvas = tk.Canvas(root, width=400, height=400)
canvas.pack()

rect = canvas.create_rectangle(50, 50, 150, 150, fill="blue", tags="mytag")

# 绑定第一个方法
canvas.tag_bind("mytag", "<Button-1>", first_function)
# 绑定第二个方法（注意：这会覆盖之前的绑定）
canvas.tag_bind("mytag", "<Button-1>", second_function)

root.mainloop()
