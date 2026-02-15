"""
工具栏模块
负责创建和管理应用程序工具栏
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Dict, Any

from ..config import Settings, OBSTACLE_TYPES, OPERATION_MODES


class Toolbar:
    """工具栏类"""
    
    def __init__(self, parent, obstacle_manager, canvas_manager):
        self.parent = parent
        self.obstacle_manager = obstacle_manager
        self.canvas_manager = canvas_manager
        self.settings = obstacle_manager.settings
        
        self._create_toolbar()
    
    def _create_toolbar(self):
        """创建工具栏"""
        # 创建工具栏容器
        self.toolbar_frame = ttk.Frame(self.parent)
        self.toolbar_frame.pack(side='top', fill='x', padx=5, pady=2)
        
        # 工具栏标题
        toolbar_label = ttk.Label(self.toolbar_frame, text="工具栏", font=("微软雅黑", 10, "bold"))
        toolbar_label.pack(anchor='w', pady=(0, 5))
        
        # 工具栏按钮容器
        button_frame = ttk.Frame(self.toolbar_frame)
        button_frame.pack(fill='x')
        
        # 工具栏按钮
        tools = [
            ("新建", self._new_project),
            ("打开", self._open_project),
            ("保存", self._save_project),
            ("导出", self._export_image),
            ("撤销", self._undo),
            ("重做", self._redo),
            ("删除", self._delete_selected)
        ]
        
        for i, (text, command) in enumerate(tools):
            btn = ttk.Button(
                button_frame,
                text=text,
                command=command,
                width=10
            )
            btn.pack(side='left', padx=2, pady=2)
    
    def _new_project(self):
        """新建项目"""
        try:
            # 这里可以调用主窗口的新建项目方法
            messagebox.showinfo("提示", "新建项目功能")
        except Exception as e:
            logging.error(f"新建项目失败: {e}")
            messagebox.showerror("错误", f"新建项目失败: {e}")
    
    def _open_project(self):
        """打开项目"""
        try:
            messagebox.showinfo("提示", "打开项目功能")
        except Exception as e:
            logging.error(f"打开项目失败: {e}")
            messagebox.showerror("错误", f"打开项目失败: {e}")
    
    def _save_project(self):
        """保存项目"""
        try:
            messagebox.showinfo("提示", "保存项目功能")
        except Exception as e:
            logging.error(f"保存项目失败: {e}")
            messagebox.showerror("错误", f"保存项目失败: {e}")
    
    def _export_image(self):
        """导出图片"""
        try:
            messagebox.showinfo("提示", "导出图片功能")
        except Exception as e:
            logging.error(f"导出图片失败: {e}")
            messagebox.showerror("错误", f"导出图片失败: {e}")
    
    def _undo(self):
        """撤销"""
        try:
            messagebox.showinfo("提示", "撤销功能")
        except Exception as e:
            logging.error(f"撤销失败: {e}")
            messagebox.showerror("错误", f"撤销失败: {e}")
    
    def _redo(self):
        """重做"""
        try:
            messagebox.showinfo("提示", "重做功能")
        except Exception as e:
            logging.error(f"重做失败: {e}")
            messagebox.showerror("错误", f"重做失败: {e}")
    
    def _delete_selected(self):
        """删除选中项"""
        try:
            self.obstacle_manager.delete_selected()
            messagebox.showinfo("成功", "已删除选中项")
        except Exception as e:
            logging.error(f"删除失败: {e}")
            messagebox.showerror("错误", f"删除失败: {e}")
    
    def hide_toolbar(self):
        """隐藏工具栏"""
        self.toolbar_frame.pack_forget()
    
    def show_toolbar(self):
        """显示工具栏"""
        self.toolbar_frame.pack(side='top', fill='x', padx=5, pady=2)
