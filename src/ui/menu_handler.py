"""
菜单处理模块
将 main.py 中的菜单相关代码分离到这里
"""

import tkinter as tk


def create_menu(
    win,
    what,
    drag_func,
    rotate_func,
    pen_func,
    clear_func,
    remove_f_func,
    open_file_func,
    save_1_func,
    del_fg_func,
    currency_pen_func,
    about_func,
    open_web_func,
):
    """
    创建菜单栏
    :param win: 主窗口
    :param what: tk.IntVar，工具选择
    :param drag_func: 拖动函数
    :param rotate_func: 旋转函数
    :param pen_func: 铅笔函数
    :param clear_func: 清屏函数
    :param remove_f_func: 清除水印函数
    :param open_file_func: 打开文件函数
    :param save_1_func: 保存函数
    :param del_fg_func: 删除背景函数
    :param currency_pen_func: 铅笔字号函数
    :param about_func: 关于函数
    :param open_web_func: 打开网页函数
    """
    menu = tk.Menu(win)

    # 工具栏
    menuType = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="工具栏", menu=menuType)
    menuType.add_radiobutton(
        label="指针拖动", command=drag_func, variable=what, value=0
    )
    menuType.add_radiobutton(label="旋转", command=rotate_func, variable=what, value=3)
    menuType.add_radiobutton(label="长度测量", command=pen_func, variable=what, value=1)

    # 功能
    function_menuType = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="功能", menu=function_menuType)
    function_menuType.add_command(label="清屏", command=clear_func)
    function_menuType.add_command(label="清除水印", command=remove_f_func)
    function_menuType.add_command(label="打开文件下载位置", command=open_file_func)
    function_menuType.add_command(label="下载", command=save_1_func)
    function_menuType.add_command(label="删除背景", command=del_fg_func)

    # 字号
    font_menuType = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="字号", menu=font_menuType)
    font_menuType.add_command(label="长度测量", command=currency_pen_func)

    # 帮助
    app_help = tk.Menu(menu, tearoff=0)
    menu.add_cascade(label="帮助", menu=app_help)
    app_help.add_command(label="关于软件", command=about_func)
    app_help.add_command(label="帮助文档", command=open_web_func)

    win.config(menu=menu)
    return menu
