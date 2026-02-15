"""
测量功能模块
处理长度测量、路线计算等功能
"""

import math
from typing import Callable, Optional, Tuple


class MeasurementHandler:
    """测量处理器"""

    def __init__(
        self,
        canvas,
        app_state,
        create_line_func: Callable,
        update_display_func: Callable,
    ):
        self.canvas = canvas
        self.app_state = app_state
        self.create_line = create_line_func
        self.update_display = update_display_func
        self._setup_measurement_state()

    def _setup_measurement_state(self):
        """初始化测量状态"""
        if not hasattr(self.app_state, "px"):
            self.app_state.px = 0.0
        if not hasattr(self.app_state, "click_num"):
            self.app_state.click_num = 1
        if not hasattr(self.app_state, "remove_px"):
            self.app_state.remove_px = {}
        if not hasattr(self.app_state, "route_clicks"):
            self.app_state.route_clicks = []
        if not hasattr(self.app_state, "lastDraw"):
            self.app_state.lastDraw = 0
        if not hasattr(self.app_state, "end"):
            self.app_state.end = [0]

    def calculate_distance(self, x1: float, y1: float, x2: float, y2: float) -> float:
        """
        计算两点间距离（米）
        :param x1, y1: 起点坐标
        :param x2, y2: 终点坐标
        :return: 距离（米）
        """
        return (math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)) / 10

    def start_measurement(self, event) -> Optional[int]:
        """
        开始测量
        :param event: 鼠标事件
        :return: 线段ID或None
        """
        what = self.app_state.what.get()
        if what != 1:  # 非测量模式
            return None

        X = self.app_state.X.get()
        Y = self.app_state.Y.get()

        # 创建新线段
        line_id = self.canvas.create_line(
            X,
            Y,
            event.x,
            event.y,
            fill="#000000",
            width=self.app_state.font_size,
            tags=("line", "不框选"),
            smooth=True,
        )

        # 计算距离
        x1, y1, x2, y2 = self.canvas.coords(line_id)
        distance = self.calculate_distance(x1, y1, x2, y2)

        # 更新状态
        self.app_state.px += distance
        self.app_state.remove_px[line_id] = distance
        self.app_state.lastDraw = line_id

        # 更新显示
        self.update_display(f"{self.app_state.px:.2f}m")

        self.app_state.click_num = 1
        return line_id

    def continue_measurement(self, event) -> Optional[int]:
        """
        继续测量（第二段）
        :param event: 鼠标事件
        :return: 线段ID或None
        """
        what = self.app_state.what.get()
        if what != 1 or self.app_state.click_num != 2:
            return None

        # 创建新线段
        line_id = self.create_line(
            self.app_state.start_x.get(),
            self.app_state.start_y.get(),
            event.x,
            event.y,
        )

        # 计算距离
        x1, y1, x2, y2 = self.canvas.coords(line_id)
        distance = self.calculate_distance(x1, y1, x2, y2)

        # 更新状态
        self.app_state.px += distance
        self.app_state.route_clicks.append(
            (self.app_state.start_x.get(), self.app_state.start_y.get())
        )
        self.app_state.stack.append(("长度测量", ([line_id], distance)))

        # 更新显示
        self.update_display(f"{self.app_state.px:.2f}m")

        # 重置起点
        self.app_state.start_x.set(event.x)
        self.app_state.start_y.set(event.y)

        return line_id

    def end_measurement_segment(self, event) -> Tuple[Optional[int], float]:
        """
        结束一段测量
        :param event: 鼠标事件
        :return: (线段ID, 本段距离)
        """
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

        return None, 0.0

    def clear_measurement(self):
        """清除所有测量"""
        self.canvas.delete("line")
        self.canvas.delete("rubber")
        self.app_state.px = 0
        self.update_display("0.00m")
        self.app_state.click_num = 1
        self.app_state.remove_px = {}

        # 从撤销栈中移除测量记录
        to_be_deleted = []
        for i in range(len(self.app_state.stack)):
            if self.app_state.stack[i][0] == "长度测量":
                to_be_deleted.append(i)
        for idx in reversed(to_be_deleted):
            self.app_state.stack.pop(idx)

    def undo_last_measurement(self):
        """撤销上一次的测量"""
        if not self.app_state.stack:
            return

        item = self.app_state.stack.pop()
        if item[0] == "长度测量":
            ids, temp_px = item[1]
            for i in ids:
                self.canvas.delete(i)
            self.app_state.px -= temp_px
            self.update_display(f"{self.app_state.px:.2f}m")

            # 恢复起点
            if self.app_state.route_clicks:
                x, y = self.app_state.route_clicks.pop()
                self.app_state.start_x.set(x)
                self.app_state.start_y.set(y)


def create_measurement_handler(
    canvas,
    app_state,
    create_line_func: Callable,
    update_display_func: Callable,
) -> MeasurementHandler:
    """
    创建测量处理器
    :param canvas: tkinter canvas
    :param app_state: 应用状态
    :param create_line_func: 创建线段函数
    :param update_display_func: 更新显示函数
    :return: MeasurementHandler实例
    """
    return MeasurementHandler(canvas, app_state, create_line_func, update_display_func)
