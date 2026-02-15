"""
赛事信息处理模块
处理比赛信息的编辑、显示和验证
"""
import tkinter as tk
from tkinter import messagebox
from functools import partial


# 默认赛事信息字段
DEFAULT_INFO_FIELDS = [
    '比赛名称', '级别赛制', '比赛日期', '路线查看时间', '开赛时间', '判罚表',
    '障碍高度', '行进速度', '路线长度', '允许时间', '限制时间',
    '障碍数量', '跳跃数量', '附加赛', '路线设计师',
]


def create_info_panel(win, frame_info, frame_tit, frame_inp, frame_por, sys_name):
    """
    创建赛事信息面板
    :param win: 主窗口
    :param frame_info: 主容器
    :param frame_tit: 标题容器
    :param frame_inp: 输入容器
    :param frame_por: 建议容器
    :param sys_name: 系统名称
    """
    frame_info.place(x=900 + 200, y=150)
    frame_tit.pack(side='left')
    frame_por.pack(side='right')
    frame_inp.pack(side='right')


def create_info_edit_functions(frame_tit, frame_inp, frame_por, info_var, pro_var,
                                info_fields, sys_name, allow_func):
    """
    创建赛事信息编辑相关函数
    """
    def dle(temp_txt_var, canvas, messagebox):
        """确认赛事信息"""
        try:
            temp = {}
            for i in frame_tit.winfo_children():
                i.destroy()
            for i in frame_inp.winfo_children():
                i.destroy()
            for i in frame_por.winfo_children():
                i.destroy()

            for i in range(len(info_var)):
                if info_var[i].get():
                    temp[info_fields[i]] = info_var[i]

            for key, value in temp.items():
                if key == '比赛名称':
                    temp_txt_var['text'] = value.get()
                    canvas.itemconfig('比赛名称', text=value.get())
                    continue
                font = 21 if sys_name == 'Darwin' else 15
                tk.Label(frame_tit, text=key + ': ', font=("微软雅黑", font)).pack(padx=1, pady=4)
                tk.Label(frame_inp, text=value.get(), font=("微软雅黑", font)).pack(padx=1, pady=4)
                tk.Label(frame_por, text='').pack(padx=1, pady=7)

        except Exception as e:
            print("Error: " + str(e))
            messagebox.showerror("Error", "出错了")

    def edit(temp_, frame_tit, frame_inp, frame_por, info_var, pro_var,
             info_fields, sys_name, allow_func):
        """编辑赛事信息"""
        info_var.clear()
        pro_var.clear()

        for i in frame_tit.winfo_children():
            i.destroy()
        for i in frame_inp.winfo_children():
            i.destroy()
        for i in frame_por.winfo_children():
            i.destroy()

        for i in info_fields:
            font = 20 if sys_name == 'Darwin' else 13
            tk.Label(frame_tit, text=i + ":", font=("微软雅黑", font)).pack(padx=1, pady=3)
            var = tk.StringVar()
            pro_value = tk.StringVar()
            if temp_:
                var.set(temp_.get(i, ''))
            info_var.append(var)
            pro_var.append(pro_value)
            y = 4 if sys_name == 'Darwin' else 7
            if i == '允许时间':
                Entry(frame_inp, textvariable=var, width=15, validate="focusin",
                      validatecommand=partial(allow_func, info_var, pro_value)).pack(padx=1, pady=y)
                tk.Label(frame_por, textvariable=pro_value).pack(padx=1, pady=7)
                continue
            Entry(frame_inp, textvariable=var, width=15).pack(padx=1, pady=y)
            tk.Label(frame_por, textvariable=pro_value).pack(padx=1, pady=7)

    return dle, edit


def create_allow_function(messagebox, logging):
    """创建允许时间计算函数"""
    def allow(info_var, pro_value):
        try:
            s = info_var[7].get()
            l = info_var[8].get()
            if s.isdigit():
                s = float(s)
            else:
                s = float(s.split('/')[0][:-1])
            if l.isdigit():
                l = float(l)
            else:
                l = float(l.split('m')[0])
            t = s / l * 60
            pro_value.set('%.2fs' % t)
            return True
        except Exception as e:
            print('赛事信息出错：', e)
            return False

    return allow
