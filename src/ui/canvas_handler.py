"""
画布事件处理模块
处理鼠标事件、拖拽、测量等画布交互
"""
import math


def bind_canvas_events(canvas, win, shu, leftButtonDown, leftButtonMove,
                       leftButtonUp, undo):
    """
    绑定画布事件
    """
    # 鼠标移动 - 实时坐标
    canvas.bind('<Motion>', shu)

    # 鼠标左键点击
    canvas.bind('<Button-1>', leftButtonDown)

    # 鼠标左键拖动
    canvas.bind('<B1-Motion>', leftButtonMove)

    # 松开左键
    canvas.bind('<ButtonRelease-1>', leftButtonUp)

    # 撤销快捷键
    win.bind("<Command-KeyPress-z>", undo)
    win.bind("<Control-KeyPress-z>", undo)

    # 点击取消焦点
    def unfocus_click(event):
        if 'ent' not in str(event.widget):
            win.focus_set()

    win.bind('<Button-1>', unfocus_click)


def create_line(canvas, x1, y1, x2, y2):
    """创建线段"""
    return canvas.create_line(x1, y1, x2, y2, tags=("line", '不框选'))


def calculate_distance(x1, y1, x2, y2):
    """计算两点间距离（米）"""
    return (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) / 10


def update_mouse_coordinates(canvas, event):
    """更新鼠标坐标显示"""
    x = event.x / 10 - 1.5
    y = event.y / 10 - 5
    canvas.itemconfig('鼠标x', text=f'x:{x:.2f}')
    canvas.itemconfig('鼠标y', text=f'y:{y:.2f}')
