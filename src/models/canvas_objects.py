"""
Canvas 对象模块
封装所有画布对象类，替代 scale.py
"""

import math
from functools import partial
from typing import Optional, TYPE_CHECKING
from PIL import Image, ImageTk

# 使用统一的日志模块
from src.core.logger import get_logger

if TYPE_CHECKING:
    from src.models.edit_panel import Focus


class CanvasObject:
    """所有画布对象的基类"""

    all_instances = []

    def __init__(self, app, index: int):
        self.__class__.all_instances.append(self)
        self.tag: Optional[str] = None
        self.startx = 160
        self.starty = 25
        self.current_x = 160
        self.current_y = 25
        self.angle = 0
        self.temp_angle = 0
        self.app = app
        self.index = str(index)
        self.line_tag = None
        self.id = None

    @classmethod
    def get_instance_by_tag(cls, tag: str) -> Optional["CanvasObject"]:
        """通过 tag 查找实例"""
        for instance in cls.all_instances:
            if instance.tag == tag:
                return instance
        return None

    def mousedown(self, tag, event, set_frame_stare, set_cur, what, choice_tup):
        """
        鼠标左键按下
        """
        set_frame_stare(False)
        try:
            if choice_tup and not (
                min(choice_tup[0], choice_tup[2])
                < event.x
                < max(choice_tup[0], choice_tup[2])
                and min(choice_tup[1], choice_tup[3])
                < event.y
                < max(choice_tup[1], choice_tup[3])
            ):
                self.app.delete("choice")
                choice_tup.clear()
                self.app.dtag("choice_start", "choice_start")
        except Exception as e:
            get_logger().warning(f"mousedown处理异常: {e}", exc_info=True)
        if what.get() == 0:
            try:
                self.startx = event.x
                self.starty = event.y
            except (TypeError, AttributeError, IndexError):
                self.startx = event[0]
                self.starty = event[1]
            self.tag = tag
            set_cur(self.id)
            self.app.lift(self.tag)

    def drag(self, tag, event, what, choice_tup, set_frame_stare):
        """
        鼠标拖动
        """
        if what.get() == 0 and not choice_tup:
            set_frame_stare(False)
            self.app.move(tag, event.x - self.startx, event.y - self.starty)
            if self.line_tag:
                self.app.move(
                    self.line_tag, event.x - self.startx, event.y - self.starty
                )
            self.current_x += event.x - self.startx
            self.current_y += event.y - self.starty
            self.startx = event.x
            self.starty = event.y

    def mouseup(self, event, move_x, move_y, what, stack, rotate_, angle, dx, dy):
        """
        鼠标释放
        """
        if dx or dy:
            stack.append(("移动", (self.id,), (dx, dy)))
        if what.get() == 3 and self.temp_angle != angle:
            rotate_.append(angle)
            stack.append(("旋转", self))


class CreateTxt(CanvasObject):
    """创建文本标签"""

    def __init__(self, app, index: int):
        super().__init__(app, index)

    def create(self, txt: str, mousedown_handler, drag_handler, mouseup_handler, stack):
        """
        创建文本
        :param txt: 文本内容
        """
        self.tag = "txt-" + self.index
        text = self.app.create_text(self.startx, self.starty, text=txt, tags=self.tag)
        self.id = text
        stack.append(("创建", text))
        self.app.tag_bind(self.tag, "<Button-1>", partial(mousedown_handler, self.tag))
        self.app.tag_bind(self.tag, "<B1-Motion>", partial(drag_handler, text))
        self.app.tag_bind(self.tag, "<ButtonRelease-1>", mouseup_handler)
        self.mousedown(
            self.tag,
            [200, 100],
            lambda x: None,
            lambda x: None,
            type("Obj", (), {"get": lambda self: 0})(),
            [],
        )


class CreateParameter(CanvasObject):
    """创建参数标签"""

    def __init__(self, app, index: int):
        super().__init__(app, index)

    def create(self, txt: str, mousedown_handler, drag_handler, mouseup_handler, stack):
        """
        创建参数文本
        """
        self.tag = "parameter-" + self.index
        text = self.app.create_text(
            self.startx, self.starty, text=txt, tags=("parameter", self.tag)
        )
        self.id = text
        stack.append(("创建", text))
        self.app.tag_bind(self.tag, "<Button-1>", partial(mousedown_handler, self.tag))
        self.app.tag_bind(self.tag, "<B1-Motion>", partial(drag_handler, text))
        self.app.tag_bind(self.tag, "<ButtonRelease-1>", mouseup_handler)
        self.mousedown(
            self.tag,
            [200, 100],
            lambda x: None,
            lambda x: None,
            type("Obj", (), {"get": lambda self: 0})(),
            [],
        )


class CreateImg(CanvasObject):
    """创建图像对象"""

    def __init__(self, app, index: int, img_path: str, obstacle: Optional[str] = None):
        super().__init__(app, index)
        self.var = None
        self.img = None
        self.frame_button = None
        self.frame_input = None
        self.img_path = img_path
        self.img_obj = Image.open(self.img_path)
        self.temp_path = None
        self.img_file = None
        self.obstacle = obstacle
        self.focus: Optional["Focus"] = None
        self.info = []
        self.com_info = {}
        self.state = {}
        self.name = ""
        self.state_line = 0

    def create(
        self, mousedown_handler, drag_handler, mouseup_handler, set_frame_stare, stack
    ):
        """
        创建图像
        """
        self.tag = "img-" + self.index
        self.img_file = ImageTk.PhotoImage(self.img_obj)
        img_id = self.app.create_image(
            self.startx, self.starty, image=self.img_file, tag=self.tag
        )
        self.id = img_id
        stack.append(("创建", img_id))
        self.app.tag_bind(self.tag, "<Button-1>", partial(mousedown_handler, self.tag))
        self.app.tag_bind(self.tag, "<B1-Motion>", partial(drag_handler, img_id))
        self.mousedown(
            self.tag,
            [200, 100],
            lambda x: None,
            lambda x: None,
            type("Obj", (), {"get": lambda self: 0})(),
            [],
        )
        set_frame_stare(True)
        self.app.tag_bind(self.tag, "<ButtonRelease-1>", mouseup_handler)

    def guide(self, create_line):
        """
        创建辅助线（用于旋转）
        """
        if 90 < self.angle < 180 or 270 < self.angle <= 359:
            ang = 90 - self.angle % 90
        elif 180 < self.angle < 270:
            ang = self.angle % 180
        else:
            ang = self.angle

        if self.angle == 90:
            x1 = x2 = self.current_x
            y1 = self.current_y - 150
            y2 = self.current_y + 150
            self.line_tag = create_line(x1, y1, x2, y2)
            return
        elif self.angle == 180:
            y1 = y2 = self.current_y
            x1 = self.current_x - 150
            x2 = self.current_x + 150
            self.line_tag = create_line(x1, y1, x2, y2)
            return

        k = math.tan(self.angle * math.pi / 180)
        b = -self.current_y - k * self.current_x
        if ang <= 45:
            x1 = self.current_x - 150
            y1 = -(((self.current_x - 150) * k) + b)
            x2 = self.current_x + 150
            y2 = -(((self.current_x + 150) * k) + b)
        elif ang > 45:
            y1 = self.current_y - 150
            y2 = self.current_y + 150
            m1 = (y2 - b) / k
            m2 = (y1 - b) / k
            m = (m1 + m2) / 2
            n = m - self.current_x
            x1 = m1 - n
            x2 = m2 - n

        self.line_tag = create_line(x1, y1, x2, y2)

    def rotate_bound(self, angle: int) -> Image.Image:
        """
        旋转图片
        :param angle: 旋转角度
        :return: 旋转后的图像对象
        """
        img = Image.open(self.img_path)
        img2 = img.convert("RGBA")
        img2 = img2.rotate(angle, expand=True)
        return img2

    def rotate(self, id: int, angle: int, itemconfig, set_cur, var):
        """
        执行旋转
        """
        self.img = self.rotate_bound(angle)
        self.temp_path = ImageTk.PhotoImage(self.img)
        itemconfig(id, image=self.temp_path)
        var.set(str(int(angle)))
        set_cur(self.id)
        self.angle = angle

        if (
            self.obstacle
            in ["oxer", "tirail", "combination_ab", "combination_abc", "monorail"]
            and self.state_line
        ):
            self.app.delete(self.line_tag)
            self.guide(
                lambda x1, y1, x2, y2: self.app.create_line(x1, y1, x2, y2, dash=(5, 3))
            )
            self.line_tag = self.app.create_line(0, 0, 0, 0, dash=(5, 3))  # Placeholder
