"""
编辑面板模块
封装障碍物编辑界面，替代 focus.py
"""

import tkinter as tk
from tkinter import Entry
from functools import partial
from typing import Optional, TYPE_CHECKING, Callable

if TYPE_CHECKING:
    from PIL import Image, ImageTk


class EditPanel:
    """障碍物编辑面板（单例）"""

    instance: Optional["EditPanel"] = None

    def __new__(cls, win):
        if cls.instance is None:
            cls.instance = super().__new__(cls)
            cls.instance._initialized = False
        return cls.instance

    def __init__(self, win):
        if self._initialized:
            return
        self._initialized = True
        self.win = win
        self.frame = None
        self.frame_input = None
        self.frame_label = None
        self.frame_button = None
        self.create_frame()

    def create_frame(self):
        """初始化生成frame容器"""
        self.frame = tk.Frame(self.win, name="障碍编辑容器")
        self.frame.pack()
        self.frame_button = tk.Frame(self.frame)
        self.frame_button.pack(side="bottom")
        self.frame_label = tk.Frame(self.frame)
        self.frame_label.pack(side="left")
        self.frame_input = tk.Frame(self.frame)
        self.frame_input.pack(side="right")

    def update(self, obj, obstacle: str, info=None, state=None, com_info=None):
        """
        点击组件后生成信息框
        """
        self.create_frame()
        self.remove()

        if obstacle == "oxer":
            return self._create_oxer_panel(info)
        elif obstacle == "tirail":
            return self._create_tirail_panel(info)
        elif obstacle in ("combination_ab", "combination_abc"):
            return self._create_combination_panel(obj, com_info, obstacle, state)
        elif obstacle == "water":
            return self._create_water_panel(info)
        elif obstacle == "live":
            return self._create_live_panel(info, obj)

        return self.frame_input, self.frame_button

    def _create_oxer_panel(self, info):
        """创建双横木编辑面板"""
        tk.Label(self.frame_label, text="A-->B(m):").pack()
        var_a_b = tk.StringVar(value=info[0] if info else "")
        a_b = Entry(self.frame_input, textvariable=var_a_b, width=5)
        a_b.pack()
        tk.Button(self.frame_button, text="确认").pack()
        return self.frame_input, self.frame_button

    def _create_tirail_panel(self, info):
        """创建三横木编辑面板"""
        tk.Label(self.frame_label, text="A-->B(m):").pack()
        var_a_b = tk.StringVar(value=info[0] if info else "")
        a_b = Entry(self.frame_input, textvariable=var_a_b, width=5)
        a_b.pack()
        tk.Label(self.frame_label, text="B-->C(m):").pack()
        var_b_c = tk.StringVar(value=info[1] if info else "")
        b_c = Entry(self.frame_input, textvariable=var_b_c, width=5)
        b_c.pack()
        tk.Button(self.frame_button, text="确认").pack()
        return self.frame_input, self.frame_button

    def _create_water_panel(self, info):
        """创建水障编辑面板"""
        tk.Label(self.frame_label, text="宽(m)：").pack()
        water_width_var = tk.StringVar(value=info[0] if info else "3")
        water_width_ent = Entry(self.frame_input, textvariable=water_width_var, width=5)
        water_width_ent.pack()
        tk.Label(self.frame_label, text="长(m)：").pack()
        water_height_var = tk.StringVar(value=info[0] if info else "4")
        water_height_ent = Entry(
            self.frame_input, textvariable=water_height_var, width=5
        )
        water_height_ent.pack()
        tk.Button(self.frame_button, text="确认").pack()
        return self.frame_input, self.frame_button

    def _create_live_panel(self, info, obj):
        """创建利物浦编辑面板"""
        check = tk.StringVar(value="0")
        tk.Label(self.frame_label, text="宽(m)：").pack()
        water_width_var = tk.StringVar(value=info[0] if info else "2")
        water_width_ent = Entry(
            self.frame_input, textvariable=water_width_var, width=5, name="water_w_ent"
        )
        water_width_ent.pack()
        tk.Label(self.frame_label, text="长(m)：").pack()
        water_height_var = tk.StringVar(value=info[0] if info else "4")
        water_height_ent = Entry(
            self.frame_input, textvariable=water_height_var, width=5, name="water_h_ent"
        )
        water_height_ent.pack()
        tk.Button(self.frame_button, text="确认").pack()
        tk.Checkbutton(
            self.frame_button,
            text="双横木",
            variable=check,
            onvalue=1,
            offvalue=0,
            command=partial(self._on_live_double_change, obj, check),
        ).pack()
        return self.frame_input, self.frame_button

    def _create_combination_panel(self, obj, info, obstacle: str, state):
        """创建组合障碍编辑面板"""
        a = b = c = "0"
        if state:
            a = "1" if state.get("ent_a") == "normal" else "0"
            b = "1" if state.get("ent_b") == "normal" else "0"
            c = "1" if state.get("ent_c") == "normal" else "0"

        checkvar_a = tk.StringVar(value=a, name="checkvar_a")
        checkvar_b = tk.StringVar(value=b, name="checkvar_b")
        checkvar_c = tk.StringVar(value=c, name="checkvar_c")

        var_a = tk.StringVar(value=info.get("ent_a") if info else "")
        ent_a = Entry(
            self.frame_input,
            textvariable=var_a,
            width=5,
            state=state.get("ent_a") if state else "disabled",
            name="ent_a",
        )
        ent_a.pack()

        tk.Checkbutton(
            self.frame_label,
            text="A双横木(cm)",
            variable=checkvar_a,
            onvalue=1,
            offvalue=0,
            command=partial(
                self._on_obstacle_double_change,
                checkvar_a,
                checkvar_b,
                checkvar_c,
                ent_a,
                obj,
                obstacle,
                var_a,
            ),
        ).pack()

        tk.Label(self.frame_label, text="A-->B(m):").pack()
        var_a_b = tk.StringVar(value=info.get("ent_a_b") if info else "3")
        ent_a_b = Entry(self.frame_input, textvariable=var_a_b, width=5, name="ent_a_b")
        ent_a_b.pack()

        var_b = tk.StringVar(value=info.get("ent_b") if info else "")
        ent_b = Entry(
            self.frame_input,
            textvariable=var_b,
            width=5,
            state=state.get("ent_b") if state else "disabled",
            name="ent_b",
        )
        ent_b.pack()

        tk.Checkbutton(
            self.frame_label,
            text="B双横木(cm)",
            variable=checkvar_b,
            onvalue=1,
            offvalue=0,
            command=partial(
                self._on_obstacle_double_change,
                checkvar_a,
                checkvar_b,
                checkvar_c,
                ent_b,
                obj,
                obstacle,
                var_b,
            ),
        ).pack()

        if obstacle == "combination_abc":
            tk.Label(self.frame_label, text="B-->C(m):").pack()
            var_b_c = tk.StringVar(value=info.get("ent_b_c") if info else "3")
            ent_b_c = Entry(
                self.frame_input, textvariable=var_b_c, width=5, name="ent_b_c"
            )
            ent_b_c.pack()
            var_c = tk.StringVar(value=info.get("ent_c") if info else "")
            ent_c = Entry(
                self.frame_input,
                textvariable=var_c,
                width=5,
                state=state.get("ent_c") if state else "disabled",
                name="ent_c",
            )
            ent_c.pack()
            tk.Checkbutton(
                self.frame_label,
                text="C双横木(cm)",
                variable=checkvar_c,
                onvalue=1,
                offvalue=0,
                command=partial(
                    self._on_obstacle_double_change,
                    checkvar_a,
                    checkvar_b,
                    checkvar_c,
                    ent_c,
                    obj,
                    "combination_abc",
                    var_c,
                ),
            ).pack()

        tk.Button(self.frame_button, text="确认").pack()
        return checkvar_a, checkvar_b

    def _on_obstacle_double_change(self, x1, x2, x3, ent, obj, obstacle, var):
        """处理障碍双横木状态变化"""
        self._toggle_entry_state(x1, ent, var)
        if obstacle == "combination_abc":
            self._update_abc_obstacle(obj, x1, x2, x3)
        else:
            self._update_ab_obstacle(obj, x1, x2, obstacle)

    def _toggle_entry_state(self, check, ent, var):
        """切换输入框状态"""
        if check.get() == "1":
            ent.config(state="normal")
        elif check.get() == "0":
            ent.config(state="disabled")

    def _update_ab_obstacle(self, obj, x1, x2, obstacle):
        """更新AB组合障碍图像"""
        from src.core.image_processor import get_image_processor

        ip = get_image_processor()
        if x1.get() == "1" and x2.get() == "1":
            obj.img_path = ip.merge_ab(state=2, m1=30)
        elif x1.get() == "1" and x2.get() == "0":
            obj.img_path = ip.oxer_obs_ab(stare_a="1", state_b="0")
        elif x1.get() == "0" and x2.get() == "1":
            obj.img_path = ip.oxer_obs_ab(stare_a="0", state_b="1")
        else:
            obj.img_path = ip.merge_ab(state=1, m1=30)

        obj.img = Image.open(obj.img_path)
        obj.temp_path = ImageTk.PhotoImage(obj.img)
        obj.app.itemconfig(obj.tag, image=obj.temp_path)

    def _update_abc_obstacle(self, obj, x1, x2, x3):
        """更新ABC组合障碍图像"""
        from src.core.image_processor import get_image_processor

        ip = get_image_processor()
        obj.img_path = ip.oxer_obs_ab(
            stare_a=x1.get(), state_b=x2.get(), state_c=x3.get(), b_c=30
        )
        obj.img = Image.open(obj.img_path)
        obj.temp_path = ImageTk.PhotoImage(obj.img)
        obj.app.itemconfig(obj.tag, image=obj.temp_path)

    def _on_live_double_change(self, obj, check):
        """处理利物浦双横木状态变化"""
        from src.core.image_processor import get_image_processor

        state = check.get()
        if state == "1":
            obj.img_path = get_image_processor().live_two_tool()
        elif state == "0":
            obj.img_path = get_image_processor().live_one_tool()

        obj.img = Image.open(obj.img_path)
        obj.temp_path = ImageTk.PhotoImage(obj.img)
        obj.app.itemconfig(obj.tag, image=obj.temp_path)

    def remove(self):
        """删除容器中的内容"""
        for i in self.frame_label.winfo_children():
            i.destroy()
        for i in self.frame_input.winfo_children():
            i.destroy()
        for i in self.frame_button.winfo_children():
            i.destroy()


def get_edit_panel(win) -> EditPanel:
    """获取编辑面板单例"""
    if EditPanel.instance is None:
        EditPanel.instance = EditPanel(win)
    return EditPanel.instance
