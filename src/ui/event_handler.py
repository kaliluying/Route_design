"""
事件处理模块
封装所有鼠标事件和交互逻辑，替代 main.py 中的事件处理函数
"""

import math
from typing import Callable, Optional

# 使用统一的日志模块
from src.core.logger import get_logger


class EventHandler:
    """事件处理器"""

    def __init__(
        self,
        canvas,
        win,
        app_state,
        set_frame_stare,
        get_frame_stare,
        set_cur,
        set_line,
        create_line: Callable,
    ):
        self.canvas = canvas
        self.win = win
        self.app_state = app_state
        self.set_frame_stare = set_frame_stare
        self.get_frame_stare = get_frame_stare
        self.set_cur = set_cur
        self.set_line = set_line
        self.create_line = create_line
        self._setup_event_bindings()

    def _setup_event_bindings(self):
        """设置事件绑定"""
        # 鼠标移动 - 坐标更新
        self.canvas.bind("<Motion>", self.on_mouse_move)

        # 鼠标左键按下
        self.canvas.bind("<Button-1>", self.on_left_button_down)

        # 鼠标左键拖动
        self.canvas.bind("<B1-Motion>", self.on_left_button_move)

        # 松开左键
        self.canvas.bind("<ButtonRelease-1>", self.on_left_button_up)

        # 点击取消焦点
        self.win.bind("<Button-1>", self.on_unfocus_click)

    def on_mouse_move(self, event):
        """鼠标移动事件"""
        x = event.x / 10 - 1.5
        y = event.y / 10 - 5
        self.canvas.itemconfig("鼠标x", text=f"x:{x:.2f}")
        self.canvas.itemconfig("鼠标y", text=f"y:{y:.2f}")

    def on_left_button_down(self, event):
        """鼠标左键按下"""
        self.app_state.X.set(event.x)
        self.app_state.Y.set(event.y)
        self.app_state.move_x.set(event.x)
        self.app_state.move_y.set(event.y)

        # 清除选择框
        choice_tup = self.app_state.choice_tuple
        if choice_tup and not (
            min(choice_tup[0], choice_tup[2])
            < event.x
            < max(choice_tup[0], choice_tup[2])
            and min(choice_tup[1], choice_tup[3])
            < event.y
            < max(choice_tup[1], choice_tup[3])
        ):
            self.canvas.delete("choice")
            choice_tup.clear()
            self.canvas.dtag("choice_start", "choice_start")

    def on_left_button_move(self, event):
        """鼠标左键拖动"""
        what = self.app_state.what.get()
        X = self.app_state.X.get()
        Y = self.app_state.Y.get()

        # 长度测量模式
        if what == 1:
            self._handle_measurement(event, X, Y)
        # 多选框移动
        elif what == 0 and self.app_state.choice_tuple:
            self._handle_selection_move(event, X, Y)
        # 创建选择框
        else:
            if self.get_frame_stare():
                self.canvas.delete("choice")
                self.canvas.create_rectangle(
                    X, Y, event.x, event.y, tags="choice", dash=(3, 5)
                )

        self.app_state.X.set(event.x)
        self.app_state.Y.set(event.y)

    def on_left_button_up(self, event):
        """鼠标松开"""
        self.app_state.end.append(self.app_state.lastDraw)

        what = self.app_state.what.get()
        choice_start = self.get_frame_stare()

        if what == 1:
            self._handle_measurement_end(event)
        elif choice_start:
            self.canvas.addtag_overlapping(
                "choice_start",
                self.app_state.X.get(),
                self.app_state.Y.get(),
                event.x,
                event.y,
            )
            self.canvas.dtag("不框选", "choice_start")
            choice_tup = self.app_state.choice_tuple
            choice_tup.extend(
                [self.app_state.X.get(), self.app_state.Y.get(), event.x, event.y]
            )
        else:
            self.set_frame_stare(True)

        # 处理移动撤销
        if self.canvas.find_withtag("choice"):
            items = self.canvas.find_withtag("choice_start")
            dx = event.x - self.app_state.move_x.get()
            dy = event.y - self.app_state.move_y.get()
            self.app_state.stack.append(("移动", items, (dx, dy)))

    def on_unfocus_click(self, event):
        """点击取消焦点"""
        if "ent" not in str(event.widget):
            self.win.focus_set()

    def _handle_measurement(self, event, X, Y):
        """处理测量模式"""
        lastDraw = self.canvas.create_line(
            X,
            Y,
            event.x,
            event.y,
            fill="#000000",
            width=self.app_state.font_size,
            tags=("line", "不框选"),
            smooth=True,
        )

        x1, y1, x2, y2 = self.canvas.coords(lastDraw)
        distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / 10
        self.app_state.px += distance
        self.app_state.remove_px[lastDraw] = distance

        self.canvas.itemconfig("实时路线", text="%.2fm" % self.app_state.px)

    def _handle_measurement_end(self, event):
        """处理测量结束"""
        if self.app_state.click_num == 1:
            if (
                self.app_state.move_x.get() != event.x
                or self.app_state.move_y.get() != event.y
            ):
                ids = list(self.app_state.remove_px.keys())
                total = sum(self.app_state.remove_px.values())
                self.app_state.route_clicks.append(
                    (self.app_state.start_x.get(), self.app_state.start_y.get())
                )
                self.app_state.stack.append(("长度测量", (ids, total)))
                self.app_state.remove_px = {}
            self.app_state.start_x.set(event.x)
            self.app_state.start_y.set(event.y)
            self.app_state.click_num = 2
        elif self.app_state.click_num == 2:
            self.app_state.end_x.set(event.x)
            self.app_state.end_y.set(event.y)

            line_id = self.create_line(
                self.app_state.start_x.get(),
                self.app_state.start_y.get(),
                self.app_state.end_x.get(),
                self.app_state.end_y.get(),
            )

            x1, y1, x2, y2 = self.canvas.coords(line_id)
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / 10
            self.app_state.px += distance
            self.app_state.route_clicks.append(
                (self.app_state.start_x.get(), self.app_state.start_y.get())
            )
            self.app_state.stack.append(("长度测量", ([line_id], distance)))
            self.canvas.itemconfig("实时路线", text="%.2fm" % self.app_state.px)

            self.app_state.start_x.set(self.app_state.end_x.get())
            self.app_state.start_y.set(self.app_state.end_y.get())

    def _handle_selection_move(self, event, X, Y):
        """处理选择框移动"""
        choice_tup = self.app_state.choice_tuple
        if min(choice_tup[0], choice_tup[2]) < event.x < max(
            choice_tup[0], choice_tup[2]
        ) and min(choice_tup[1], choice_tup[3]) < event.y < max(
            choice_tup[1], choice_tup[3]
        ):
            bbox = self.canvas.bbox("choice")
            self.canvas.move("choice_start", event.x - X, event.y - Y)
            self.app_state.X.set(event.x)
            self.app_state.Y.set(event.y)
            try:
                choice_tup.clear()
                choice_tup.extend(list(bbox))
            except TypeError:
                logging.warning("多选框移动出错")


def create_event_handler(
    canvas,
    win,
    app_state,
    set_frame_stare,
    get_frame_stare,
    set_cur,
    set_line,
    create_line: Callable,
) -> EventHandler:
    """创建事件处理器"""
    return EventHandler(
        canvas,
        win,
        app_state,
        set_frame_stare,
        get_frame_stare,
        set_cur,
        set_line,
        create_line,
    )
