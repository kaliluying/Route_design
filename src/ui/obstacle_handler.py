"""
障碍物操作模块
处理障碍物的移动、旋转、删除、置底等操作
"""

from typing import Optional, Callable, Tuple, Any

# 使用统一的日志模块
from src.core.logger import get_logger


class ObstacleHandler:
    """障碍物操作处理器"""

    def __init__(
        self,
        canvas,
        app_state,
        set_cur_func: Callable,
        set_line_func: Callable,
        get_cur_func: Callable,
        get_frame_stare_func: Callable,
        set_frame_stare_func: Callable,
        remove_from_not_com_func: Callable,
        create_line_func: Callable,
    ):
        self.canvas = canvas
        self.app_state = app_state
        self.set_cur = set_cur_func
        self.set_line = set_line_func
        self.get_cur = get_cur_func
        self.get_frame_stare = get_frame_stare_func
        self.set_frame_stare = set_frame_stare_func
        self.remove_from_not_com = remove_from_not_com_func
        self.create_line = create_line_func

    def on_mousedown(
        self,
        tag: str,
        event,
        current_obj: Any,
        set_frame_stare: Optional[Callable] = None,
    ):
        """鼠标按下事件"""
        self.set_frame_stare(False)
        choice_tup = self.app_state.choice_tuple

        try:
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
        except Exception as e:
            logging.warning("障碍物mousedown处理异常", e)

        if self.app_state.what.get() == 0:
            try:
                current_obj.startx = event.x
                current_obj.starty = event.y
            except Exception:
                current_obj.startx = event[0]
                current_obj.starty = event[1]

            current_obj.tag = tag
            self.set_cur(current_obj.id)
            self.canvas.lift(current_obj.tag)

    def on_drag(
        self,
        tag: str,
        event,
        current_obj: Any,
        choice_tup: Optional[list] = None,
    ):
        """拖动事件"""
        if self.app_state.what.get() == 0 and not choice_tup:
            self.set_frame_stare(False)
            self.canvas.move(
                tag, event.x - current_obj.startx, event.y - current_obj.starty
            )

            if current_obj.line_tag:
                self.canvas.move(
                    current_obj.line_tag,
                    event.x - current_obj.startx,
                    event.y - current_obj.starty,
                )

            current_obj.current_x += event.x - current_obj.startx
            current_obj.current_y += event.y - current_obj.starty
            current_obj.startx = event.x
            current_obj.starty = event.y

    def on_mouseup(
        self,
        event,
        current_obj: Any,
        move_x: Any,
        move_y: Any,
        dx: int,
        dy: int,
    ):
        """鼠标释放事件"""
        if dx or dy:
            self.app_state.stack.append(("移动", (current_obj.id,), (dx, dy)))

        if (
            self.app_state.what.get() == 3
            and current_obj.temp_angle != current_obj.angle
        ):
            self.app_state.rotate_.append(current_obj.angle)
            self.app_state.stack.append(("旋转", current_obj))

    def delete_obstacle(self, id: Optional[int] = None, obj: Any = None) -> Tuple:
        """删除障碍物"""
        if id:
            cur, line = self.get_cur()
            self.canvas.delete(id)
            if id == cur:
                self.remove_from_not_com()
            return (id,)

        items = self.canvas.find_withtag("choice_start")[:-1]
        if items:
            self.canvas.itemconfig("choice_start", state="hidden")
            self.app_state.choice_tuple.clear()
            self.app_state.stack.append(("删除", items))
            return items

        cur, line = self.get_cur()
        if cur:
            self.canvas.itemconfig(cur, state="hidden")
            self.canvas.itemconfig(line, state="hidden")
            self.app_state.stack.append(("删除", (cur, line)))

        self.remove_from_not_com()
        return (cur, line) if cur else ()

    def set_to_bottom(self):
        """将选中障碍物置底"""
        cur, line = self.get_cur()
        if cur:
            self.canvas.lower(cur)
            self.canvas.lower("watermark")

    def rotate_obstacle(
        self,
        obj: Any,
        angle: int,
        itemconfig_func: Callable,
        set_cur_func: Callable,
        var: Any,
    ):
        """旋转障碍物"""
        rotated_img = obj.rotate_bound(angle)
        temp_path = rotated_img  # ImageTk.PhotoImage(rotated_img)
        itemconfig_func(obj.id, image=temp_path)
        var.set(str(int(angle)))
        set_cur_func(obj.id)
        obj.angle = angle

        if (
            obj.obstacle
            in ["oxer", "tirail", "combination_ab", "combination_abc", "monorail"]
            and obj.state_line
        ):
            self.canvas.delete(obj.line_tag)
            obj.guide(self.create_line)
            obj.line_tag = self.canvas.create_line(0, 0, 0, 0, dash=(5, 3))

    def create_guide_line(self, obj: Any) -> int:
        """创建辅助线（用于旋转）"""
        return obj.guide(self.create_line)


def create_obstacle_handler(
    canvas,
    app_state,
    set_cur_func: Callable,
    set_line_func: Callable,
    get_cur_func: Callable,
    get_frame_stare_func: Callable,
    set_frame_stare_func: Callable,
    remove_from_not_com_func: Callable,
    create_line_func: Callable,
) -> ObstacleHandler:
    """
    创建障碍物操作处理器
    :return: ObstacleHandler实例
    """
    return ObstacleHandler(
        canvas,
        app_state,
        set_cur_func,
        set_line_func,
        get_cur_func,
        get_frame_stare_func,
        set_frame_stare_func,
        remove_from_not_com_func,
        create_line_func,
    )
