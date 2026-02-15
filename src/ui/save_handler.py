"""
保存处理模块
处理路线图的保存功能
"""

import os
import time
import subprocess
from tkinter import filedialog, messagebox
from PIL import Image, EpsImagePlugin

# 使用统一的日志模块
from src.core.logger import get_logger


def create_save_functions(canvas, sys_name, temp_txt, messagebox):
    """
    创建保存相关函数
    :param canvas: tkinter canvas
    :param sys_name: 系统名称
    :param temp_txt: 临时文本
    :param messagebox: 消息框
    :return: save_1, save_0, save, open_file
    """
    logger = get_logger()

    def save_1():
        checkvar = "1"
        return save(checkvar)

    def save_0():
        checkvar = "0"
        return save(checkvar)

    def save(checkvar):
        """保存路线图"""
        current_time = time.strftime("%Y%m%d-%H%M%S")
        txt = temp_txt if temp_txt else "路线设计_" + current_time
        if not os.path.exists("./ms_download"):
            os.mkdir("./ms_download")
        path = filedialog.asksaveasfilename(
            title="保存为图片",
            filetypes=[("PNG", ".png")],
            initialdir=os.getcwd() + "/ms_download",
            initialfile=txt,
        )
        if path:
            path = path.split(".")[0]
            eps_path = path + ".eps"
            png_path = path + ".png"
            canvas.postscript(file=eps_path, colormode="color", font=("微软雅黑", 15))

            # Windows
            if sys_name == "Windows":
                EpsImagePlugin.gs_windows_binary = (
                    os.getcwd() + r"\gs10.01.1-32bit\bin\gswin32.exe"
                )
                startupinfo = subprocess.STARTUPINFO()
                startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
                cmd = (
                    f"{EpsImagePlugin.gs_windows_binary} -dSAFER -dBATCH -dNOPAUSE -sDEVICE=jpeg -r600 "
                    f"-dTextAlphaBits=4 -dGraphicsAlphaBits=4 -dEPSCrop -sOutputFile={png_path} {eps_path} "
                )
                subprocess.call(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    startupinfo=startupinfo,
                )
            else:
                img = Image.open(eps_path)
                img.save(png_path)

            os.remove(eps_path)
            messagebox.showinfo("成功", f"保存成功,\n路径:{png_path}")

    def open_file():
        """打开文件保存路径"""
        if not os.path.exists("./ms_download"):
            os.mkdir("./ms_download")
        path = os.getcwd() + f"/ms_download"
        if sys_name == "Windows":
            subprocess.Popen(["explorer", path])
        else:
            subprocess.call(["open", path])

    return save_1, save_0, save, open_file
