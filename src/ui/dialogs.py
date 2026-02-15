"""
对话框模块
包含应用程序的各种对话框
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any

from ..config import Settings, APP_NAME, APP_VERSION, APP_AUTHOR


class AboutDialog:
    """关于对话框"""
    
    def __init__(self, parent: tk.Tk, settings: Settings):
        """
        初始化关于对话框
        
        Args:
            parent: 父窗口
            settings: 设置对象
        """
        self.parent = parent
        self.settings = settings
        self.dialog = None
    
    def show(self) -> None:
        """显示对话框"""
        # 创建对话框
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title(f"关于 {APP_NAME}")
        self.dialog.geometry("400x300")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        # 创建内容
        self._create_widgets()
        
        # 等待对话框关闭
        self.parent.wait_window(self.dialog)
    
    def _create_widgets(self) -> None:
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(
            main_frame, 
            text=APP_NAME,
            font=("Arial", 16, "bold")
        )
        title_label.pack(pady=(0, 10))
        
        # 版本信息
        version_label = ttk.Label(
            main_frame,
            text=f"版本: {APP_VERSION}",
            font=("Arial", 10)
        )
        version_label.pack(pady=(0, 5))
        
        # 作者信息
        author_label = ttk.Label(
            main_frame,
            text=f"作者: {APP_AUTHOR}",
            font=("Arial", 10)
        )
        author_label.pack(pady=(0, 20))
        
        # 描述
        description_text = """
马术路线设计软件

这是一个专业的马术路线设计工具，
帮助用户创建和编辑马术比赛路线图。

功能特点:
• 多种障碍物类型
• 灵活的路线绘制
• 参数化设计
• 实时预览
• 文件保存和导出
        """
        
        desc_label = ttk.Label(
            main_frame,
            text=description_text,
            font=("Arial", 9),
            justify=tk.LEFT
        )
        desc_label.pack(pady=(0, 20))
        
        # 版权信息
        copyright_label = ttk.Label(
            main_frame,
            text="© 2024 山东体育学院. 保留所有权利.",
            font=("Arial", 8),
            foreground="gray"
        )
        copyright_label.pack(side=tk.BOTTOM, pady=(10, 0))
        
        # 确定按钮
        ok_button = ttk.Button(
            main_frame,
            text="确定",
            command=self.dialog.destroy
        )
        ok_button.pack(side=tk.BOTTOM, pady=(10, 0))


class SettingsDialog:
    """设置对话框"""
    
    def __init__(self, parent: tk.Tk, settings: Settings):
        """
        初始化设置对话框
        
        Args:
            parent: 父窗口
            settings: 设置对象
        """
        self.parent = parent
        self.settings = settings
        self.dialog = None
        self.temp_settings = {}  # 临时存储设置更改
    
    def show(self) -> None:
        """显示对话框"""
        # 创建对话框
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("设置")
        self.dialog.geometry("500x600")
        self.dialog.resizable(False, False)
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.geometry("+%d+%d" % (
            self.parent.winfo_rootx() + 50,
            self.parent.winfo_rooty() + 50
        ))
        
        # 创建内容
        self._create_widgets()
        
        # 等待对话框关闭
        self.parent.wait_window(self.dialog)
    
    def _create_widgets(self) -> None:
        """创建界面组件"""
        # 主框架
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建Notebook用于分页
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # 常规设置页
        general_frame = self._create_general_page(notebook)
        notebook.add(general_frame, text="常规")
        
        # 显示设置页
        display_frame = self._create_display_page(notebook)
        notebook.add(display_frame, text="显示")
        
        # 障碍物设置页
        obstacle_frame = self._create_obstacle_page(notebook)
        notebook.add(obstacle_frame, text="障碍物")
        
        # 文件设置页
        file_frame = self._create_file_page(notebook)
        notebook.add(file_frame, text="文件")
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # 确定按钮
        ok_button = ttk.Button(
            button_frame,
            text="确定",
            command=self._apply_settings
        )
        ok_button.pack(side=tk.RIGHT, padx=(5, 0))
        
        # 取消按钮
        cancel_button = ttk.Button(
            button_frame,
            text="取消",
            command=self.dialog.destroy
        )
        cancel_button.pack(side=tk.RIGHT)
        
        # 应用按钮
        apply_button = ttk.Button(
            button_frame,
            text="应用",
            command=self._apply_settings
        )
        apply_button.pack(side=tk.RIGHT, padx=(0, 5))
    
    def _create_general_page(self, parent) -> ttk.Frame:
        """创建常规设置页"""
        frame = ttk.Frame(parent, padding="10")
        
        # 画布设置
        canvas_group = ttk.LabelFrame(frame, text="画布设置", padding="10")
        canvas_group.pack(fill=tk.X, pady=(0, 10))
        
        # 画布宽度
        ttk.Label(canvas_group, text="画布宽度:").grid(row=0, column=0, sticky=tk.W, pady=2)
        width_var = tk.StringVar(value=str(self.settings.canvas_width))
        width_entry = ttk.Entry(canvas_group, textvariable=width_var, width=10)
        width_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        self.temp_settings['canvas_width'] = width_var
        
        # 画布高度
        ttk.Label(canvas_group, text="画布高度:").grid(row=1, column=0, sticky=tk.W, pady=2)
        height_var = tk.StringVar(value=str(self.settings.canvas_height))
        height_entry = ttk.Entry(canvas_group, textvariable=height_var, width=10)
        height_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        self.temp_settings['canvas_height'] = height_var
        
        # 操作设置
        operation_group = ttk.LabelFrame(frame, text="操作设置", padding="10")
        operation_group.pack(fill=tk.X, pady=(0, 10))
        
        # 默认操作模式
        ttk.Label(operation_group, text="默认操作模式:").grid(row=0, column=0, sticky=tk.W, pady=2)
        mode_var = tk.StringVar(value=self.settings.operation_mode)
        mode_combo = ttk.Combobox(operation_group, textvariable=mode_var, 
                                 values=['drag', 'draw', 'rotate', 'erase'], 
                                 state='readonly', width=10)
        mode_combo.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        self.temp_settings['operation_mode'] = mode_var
        
        return frame
    
    def _create_display_page(self, parent) -> ttk.Frame:
        """创建显示设置页"""
        frame = ttk.Frame(parent, padding="10")
        
        # 显示选项
        display_group = ttk.LabelFrame(frame, text="显示选项", padding="10")
        display_group.pack(fill=tk.X, pady=(0, 10))
        
        # 网格显示
        grid_var = tk.BooleanVar(value=self.settings.show_grid)
        grid_check = ttk.Checkbutton(display_group, text="显示网格", variable=grid_var)
        grid_check.pack(anchor=tk.W, pady=2)
        self.temp_settings['show_grid'] = grid_var
        
        # 辅助信息显示
        aux_var = tk.BooleanVar(value=self.settings.show_aux_info)
        aux_check = ttk.Checkbutton(display_group, text="显示辅助信息", variable=aux_var)
        aux_check.pack(anchor=tk.W, pady=2)
        self.temp_settings['show_aux_info'] = aux_var
        
        # 水印显示
        watermark_var = tk.BooleanVar(value=self.settings.show_watermark)
        watermark_check = ttk.Checkbutton(display_group, text="显示水印", variable=watermark_var)
        watermark_check.pack(anchor=tk.W, pady=2)
        self.temp_settings['show_watermark'] = watermark_var
        
        # 背景图像显示
        bg_image_var = tk.BooleanVar(value=self.settings.show_background_image)
        bg_image_check = ttk.Checkbutton(display_group, text="显示背景图像", variable=bg_image_var)
        bg_image_check.pack(anchor=tk.W, pady=2)
        self.temp_settings['show_background_image'] = bg_image_var
        
        # 事件信息显示
        event_info_var = tk.BooleanVar(value=self.settings.show_event_info)
        event_info_check = ttk.Checkbutton(display_group, text="显示事件信息", variable=event_info_var)
        event_info_check.pack(anchor=tk.W, pady=2)
        self.temp_settings['show_event_info'] = event_info_var
        
        return frame
    
    def _create_obstacle_page(self, parent) -> ttk.Frame:
        """创建障碍物设置页"""
        frame = ttk.Frame(parent, padding="10")
        
        # 障碍物默认设置
        obstacle_group = ttk.LabelFrame(frame, text="障碍物默认设置", padding="10")
        obstacle_group.pack(fill=tk.X, pady=(0, 10))
        
        # 默认长度
        ttk.Label(obstacle_group, text="默认长度:").grid(row=0, column=0, sticky=tk.W, pady=2)
        length_var = tk.StringVar(value=str(self.settings.obstacle_length))
        length_entry = ttk.Entry(obstacle_group, textvariable=length_var, width=10)
        length_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        self.temp_settings['obstacle_length'] = length_var
        
        # 默认大小
        ttk.Label(obstacle_group, text="默认大小:").grid(row=1, column=0, sticky=tk.W, pady=2)
        size_var = tk.StringVar(value=str(self.settings.obstacle_size))
        size_entry = ttk.Entry(obstacle_group, textvariable=size_var, width=10)
        size_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        self.temp_settings['obstacle_size'] = size_var
        
        return frame
    
    def _create_file_page(self, parent) -> ttk.Frame:
        """创建文件设置页"""
        frame = ttk.Frame(parent, padding="10")
        
        # 自动保存设置
        autosave_group = ttk.LabelFrame(frame, text="自动保存设置", padding="10")
        autosave_group.pack(fill=tk.X, pady=(0, 10))
        
        # 启用自动保存
        autosave_var = tk.BooleanVar(value=self.settings.auto_save_enabled)
        autosave_check = ttk.Checkbutton(autosave_group, text="启用自动保存", variable=autosave_var)
        autosave_check.pack(anchor=tk.W, pady=2)
        self.temp_settings['auto_save_enabled'] = autosave_var
        
        # 自动保存间隔
        ttk.Label(autosave_group, text="保存间隔(秒):").grid(row=1, column=0, sticky=tk.W, pady=2)
        interval_var = tk.StringVar(value=str(self.settings.auto_save_interval))
        interval_entry = ttk.Entry(autosave_group, textvariable=interval_var, width=10)
        interval_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=2)
        self.temp_settings['auto_save_interval'] = interval_var
        
        return frame
    
    def _apply_settings(self) -> None:
        """应用设置"""
        try:
            # 应用常规设置
            if 'canvas_width' in self.temp_settings:
                width = int(self.temp_settings['canvas_width'].get())
                self.settings.canvas_width = width
            
            if 'canvas_height' in self.temp_settings:
                height = int(self.temp_settings['canvas_height'].get())
                self.settings.canvas_height = height
            
            if 'operation_mode' in self.temp_settings:
                mode = self.temp_settings['operation_mode'].get()
                self.settings.operation_mode = mode
            
            # 应用显示设置
            if 'show_grid' in self.temp_settings:
                self.settings.show_grid = self.temp_settings['show_grid'].get()
            
            if 'show_aux_info' in self.temp_settings:
                self.settings.show_aux_info = self.temp_settings['show_aux_info'].get()
            
            if 'show_watermark' in self.temp_settings:
                self.settings.show_watermark = self.temp_settings['show_watermark'].get()
            
            if 'show_background_image' in self.temp_settings:
                self.settings.show_background_image = self.temp_settings['show_background_image'].get()
            
            if 'show_event_info' in self.temp_settings:
                self.settings.show_event_info = self.temp_settings['show_event_info'].get()
            
            # 应用障碍物设置
            if 'obstacle_length' in self.temp_settings:
                length = float(self.temp_settings['obstacle_length'].get())
                self.settings.obstacle_length = length
            
            if 'obstacle_size' in self.temp_settings:
                size = float(self.temp_settings['obstacle_size'].get())
                self.settings.obstacle_size = size
            
            # 应用文件设置
            if 'auto_save_enabled' in self.temp_settings:
                self.settings.auto_save_enabled = self.temp_settings['auto_save_enabled'].get()
            
            if 'auto_save_interval' in self.temp_settings:
                interval = int(self.temp_settings['auto_save_interval'].get())
                self.settings.auto_save_interval = interval
            
            # 保存设置到文件
            self.settings.save_to_file()
            
            messagebox.showinfo("成功", "设置已保存")
            self.dialog.destroy()
            
        except ValueError as e:
            messagebox.showerror("错误", f"设置值无效: {e}")
        except Exception as e:
            messagebox.showerror("错误", f"保存设置失败: {e}")
