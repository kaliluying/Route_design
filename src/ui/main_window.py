"""
主窗口模块
负责创建和管理主应用程序窗口
"""

import tkinter as tk
from tkinter import ttk, messagebox
import logging
from typing import Optional

from ..config import Settings, UI_CONFIG, OBSTACLE_TYPES, EVENT_INFO_FIELDS
from .toolbar import Toolbar
from .dialogs import AboutDialog, SettingsDialog


class MainWindow:
    """主窗口类"""
    
    def __init__(self, window, canvas_manager, obstacle_manager, event_manager, file_manager, settings: Settings):
        self.window = window
        self.canvas_manager = canvas_manager
        self.obstacle_manager = obstacle_manager
        self.event_manager = event_manager
        self.file_manager = file_manager
        self.settings = settings
        
        self._setup_window()
        self._create_menu()
        self._create_layout()
        self._setup_events()
    
    def _setup_window(self):
        """设置窗口属性"""
        # 设置窗口标题和图标
        self.window.title("路线设计")
        try:
            self.window.iconphoto(True, tk.PhotoImage(file="img/ic.png"))
        except:
            pass
        
        # 设置窗口大小和位置
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{screen_width}x{screen_height}")
        self.window.state('zoomed')  # 最大化窗口
    
    def _create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.window)
        self.window.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="新建", command=self._new_project)
        file_menu.add_command(label="打开", command=self._open_project)
        file_menu.add_command(label="保存", command=self._save_project)
        file_menu.add_separator()
        file_menu.add_command(label="导出图片", command=self._export_image)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self.window.quit)
        
        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="撤销", command=self._undo)
        edit_menu.add_command(label="重做", command=self._redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="删除", command=self._delete_selected)
        
        # 视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="视图", menu=view_menu)
        view_menu.add_checkbutton(label="网格", command=self._toggle_grid)
        view_menu.add_checkbutton(label="辅助信息", command=self._toggle_aux_info)
        view_menu.add_checkbutton(label="水印", command=self._toggle_watermark)
        
        # 工具菜单
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="工具", menu=tools_menu)
        tools_menu.add_command(label="设置", command=self._show_settings)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self._show_about)
    
    def _create_layout(self):
        """创建主布局"""
        # 主容器
        main_container = ttk.Frame(self.window)
        main_container.pack(fill='both', expand=True, padx=5, pady=5)
        
        # 创建左侧功能栏
        self._create_left_panel(main_container)
        
        # 创建中央区域
        self._create_center_panel(main_container)
        
        # 创建右侧信息面板
        self._create_right_panel(main_container)
    
    def _create_left_panel(self, parent):
        """创建左侧功能栏"""
        left_frame = ttk.Frame(parent, width=200)
        left_frame.pack(side='left', fill='y', padx=(0, 5))
        left_frame.pack_propagate(False)
        
        # 工作模块
        work_frame = ttk.LabelFrame(left_frame, text="工作模块", padding=5)
        work_frame.pack(fill='x', pady=(0, 10))
        
        # 功能容器
        command_frame = ttk.Frame(work_frame)
        command_frame.pack(fill='x')
        
        # 操作模式按钮
        self.drag_btn = ttk.Button(command_frame, text="拖拽", command=self._set_drag_mode, width=8)
        self.drag_btn.pack(side='left', padx=2, pady=2)
        
        self.draw_btn = ttk.Button(command_frame, text="绘制", command=self._set_draw_mode, width=8)
        self.draw_btn.pack(side='left', padx=2, pady=2)
        
        self.rotate_btn = ttk.Button(command_frame, text="旋转", command=self._set_rotate_mode, width=8)
        self.rotate_btn.pack(side='left', padx=2, pady=2)
        
        self.erase_btn = ttk.Button(command_frame, text="擦除", command=self._set_erase_mode, width=8)
        self.erase_btn.pack(side='left', padx=2, pady=2)
        
        # 辅助模块
        aux_frame = ttk.LabelFrame(left_frame, text="辅助模块", padding=5)
        aux_frame.pack(fill='x', pady=(0, 10))
        
        # 辅助信息容器
        aux_info_frame = ttk.Frame(aux_frame)
        aux_info_frame.pack(fill='x')
        
        # 网格辅助线按钮
        grid_btn = ttk.Button(aux_info_frame, text="网格辅助线", command=self._toggle_grid, width=12)
        grid_btn.pack(side='left', padx=2, pady=2)
        
        # 辅助信息复选框
        self.aux_info_var = tk.BooleanVar(value=True)
        aux_info_check = ttk.Checkbutton(aux_info_frame, text="辅助信息", variable=self.aux_info_var, command=self._toggle_aux_info)
        aux_info_check.pack(side='left', padx=2, pady=2)
        
        # 弧线复选框
        self.arc_var = tk.BooleanVar(value=False)
        arc_check = ttk.Checkbutton(aux_info_frame, text="弧线", variable=self.arc_var, command=self._toggle_arc)
        arc_check.pack(side='left', padx=2, pady=2)
        
        # 测量模块
        measure_frame = ttk.LabelFrame(left_frame, text="测量模块", padding=5)
        measure_frame.pack(fill='x')
        
        # 测量功能容器
        measure_com_frame = ttk.Frame(measure_frame)
        measure_com_frame.pack(fill='x')
        
        # 画路线复选框
        self.draw_route_var = tk.BooleanVar(value=False)
        draw_route_check = ttk.Checkbutton(measure_com_frame, text="画路线", variable=self.draw_route_var, command=self._set_draw_mode)
        draw_route_check.pack(side='left', padx=2, pady=2)
        
        # 清空路线按钮
        clear_btn = ttk.Button(measure_com_frame, text="清空路线", command=self._clear_route, width=10)
        clear_btn.pack(side='left', padx=2, pady=2)
    
    def _create_center_panel(self, parent):
        """创建中央区域"""
        center_frame = ttk.Frame(parent)
        center_frame.pack(side='left', fill='both', expand=True)
        
        # 顶部工具栏
        self.toolbar = Toolbar(center_frame, self.obstacle_manager, self.canvas_manager)
        
        # 顶部障碍物按钮区域
        self._create_obstacle_buttons(center_frame)
        
        # 画布区域
        canvas_frame = ttk.LabelFrame(center_frame, text="路线设计区域", padding=5)
        canvas_frame.pack(fill='both', expand=True, pady=(10, 0))
        
        # 将画布添加到画布区域
        canvas = self.canvas_manager.get_canvas()
        canvas.pack(fill='both', expand=True)
    
    def _create_obstacle_buttons(self, parent):
        """创建障碍物按钮区域"""
        # 障碍物按钮容器
        obstacle_frame = ttk.Frame(parent)
        obstacle_frame.pack(fill='x', pady=(0, 10))
        
        # 障碍物按钮标题
        obstacle_label = ttk.Label(obstacle_frame, text="障碍物", font=("微软雅黑", 10, "bold"))
        obstacle_label.pack(anchor='w', pady=(0, 5))
        
        # 障碍物按钮网格
        obstacle_buttons = [
            ("进出口", "gate"),
            ("指北针", "compass"),
            ("水障", "water_barrier"),
            ("砖墙", "brick_wall"),
            ("起/终点线", "line"),
            ("强制通过点", "force"),
            ("利物浦", "live"),
            ("单横木", "monorail"),
            ("双横木", "oxer"),
            ("三横木", "tirail"),
            ("四横木", "four"),
            ("AB组合障碍", "combination_ab"),
            ("ABC组合障碍", "combination_abc"),
            ("树", "tree"),
            ("小丑", "joker"),
            ("圆", "circular"),
            ("自定义障碍", "diy"),
            ("导入背景图", "background")
        ]
        
        # 创建按钮网格（6列布局）
        for i, (text, obstacle_type) in enumerate(obstacle_buttons):
            btn = ttk.Button(
                obstacle_frame,
                text=text,
                command=lambda t=obstacle_type: self._create_obstacle(t),
                width=12
            )
            btn.pack(side='left', padx=2, pady=2)
        
        # 工具按钮区域
        tool_frame = ttk.Frame(obstacle_frame)
        tool_frame.pack(fill='x', pady=(10, 0))
        
        # 工具按钮
        tools = [
            ("清除路线", self._clear_route),
            ("网格", self._toggle_grid),
            ("辅助信息", self._toggle_aux_info),
            ("水印", self._toggle_watermark),
            ("背景图片", self._set_background)
        ]
        
        for i, (text, command) in enumerate(tools):
            btn = ttk.Button(
                tool_frame,
                text=text,
                command=command,
                width=12
            )
            btn.pack(side='left', padx=2, pady=2)
    
    def _create_right_panel(self, parent):
        """创建右侧信息面板"""
        right_frame = ttk.Frame(parent, width=250)
        right_frame.pack(side='right', fill='y', padx=(5, 0))
        right_frame.pack_propagate(False)
        
        # 赛事信息
        event_frame = ttk.LabelFrame(right_frame, text="赛事信息", padding=10)
        event_frame.pack(fill='x', pady=(0, 10))
        
        ttk.Label(event_frame, text="比赛名称:").pack(anchor='w')
        self.event_name_var = tk.StringVar()
        ttk.Entry(event_frame, textvariable=self.event_name_var).pack(fill='x', pady=(0, 10))
        
        ttk.Label(event_frame, text="级别赛制:").pack(anchor='w')
        self.event_level_var = tk.StringVar()
        ttk.Entry(event_frame, textvariable=self.event_level_var).pack(fill='x')
        
        # 统计信息
        stats_frame = ttk.LabelFrame(right_frame, text="统计信息", padding=10)
        stats_frame.pack(fill='x')
        
        self.route_length_label = ttk.Label(stats_frame, text="路线长度: 0.00m")
        self.route_length_label.pack(anchor='w')
        
        self.obstacle_count_label = ttk.Label(stats_frame, text="障碍数量: 0")
        self.obstacle_count_label.pack(anchor='w')
    
    def _setup_events(self):
        """设置事件绑定"""
        # 绑定键盘快捷键
        self.window.bind('<Control-n>', lambda e: self._new_project())
        self.window.bind('<Control-o>', lambda e: self._open_project())
        self.window.bind('<Control-s>', lambda e: self._save_project())
        self.window.bind('<Delete>', lambda e: self._delete_selected())
        self.window.bind('<Control-z>', lambda e: self._undo())
        self.window.bind('<Control-y>', lambda e: self._redo())
    
    # 菜单命令方法
    def _new_project(self):
        """新建项目"""
        try:
            self.file_manager.new_project()
            messagebox.showinfo("成功", "已创建新项目")
        except Exception as e:
            messagebox.showerror("错误", f"创建新项目失败: {e}")
    
    def _open_project(self):
        """打开项目"""
        try:
            self.file_manager.open_project()
            messagebox.showinfo("成功", "项目加载成功")
        except Exception as e:
            messagebox.showerror("错误", f"打开项目失败: {e}")
    
    def _save_project(self):
        """保存项目"""
        try:
            self.file_manager.save_project()
            messagebox.showinfo("成功", "项目保存成功")
        except Exception as e:
            messagebox.showerror("错误", f"保存项目失败: {e}")
    
    def _export_image(self):
        """导出图片"""
        try:
            self.file_manager.export_image()
            messagebox.showinfo("成功", "图片导出成功")
        except Exception as e:
            messagebox.showerror("错误", f"导出图片失败: {e}")
    
    def _undo(self):
        """撤销"""
        try:
            self.event_manager.undo()
        except Exception as e:
            logging.error(f"撤销失败: {e}")
    
    def _redo(self):
        """重做"""
        try:
            self.event_manager.redo()
        except Exception as e:
            logging.error(f"重做失败: {e}")
    
    def _delete_selected(self):
        """删除选中项"""
        try:
            self.obstacle_manager.delete_selected()
        except Exception as e:
            logging.error(f"删除失败: {e}")
    
    def _toggle_grid(self):
        """切换网格显示"""
        try:
            self.canvas_manager.toggle_grid()
        except Exception as e:
            logging.error(f"切换网格失败: {e}")
    
    def _toggle_aux_info(self):
        """切换辅助信息显示"""
        try:
            self.canvas_manager.toggle_aux_info()
        except Exception as e:
            logging.error(f"切换辅助信息失败: {e}")
    
    def _toggle_arc(self):
        """切换弧线显示"""
        try:
            # 实现弧线显示切换
            pass
        except Exception as e:
            logging.error(f"切换弧线失败: {e}")
    
    def _toggle_watermark(self):
        """切换水印显示"""
        try:
            self.canvas_manager.toggle_watermark()
        except Exception as e:
            logging.error(f"切换水印失败: {e}")
    
    def _show_settings(self):
        """显示设置对话框"""
        try:
            dialog = SettingsDialog(self.window, self.settings)
            dialog.show()
        except Exception as e:
            logging.error(f"显示设置对话框失败: {e}")
    
    def _show_about(self):
        """显示关于对话框"""
        try:
            dialog = AboutDialog(self.window)
            dialog.show()
        except Exception as e:
            logging.error(f"显示关于对话框失败: {e}")
    
    # 操作模式设置
    def _set_drag_mode(self):
        """设置拖拽模式"""
        self.settings.set_operation_mode('DRAG')
        self._update_mode_buttons()
    
    def _set_draw_mode(self):
        """设置绘制模式"""
        self.settings.set_operation_mode('DRAW')
        self._update_mode_buttons()
    
    def _set_rotate_mode(self):
        """设置旋转模式"""
        self.settings.set_operation_mode('ROTATE')
        self._update_mode_buttons()
    
    def _set_erase_mode(self):
        """设置擦除模式"""
        self.settings.set_operation_mode('ERASE')
        self._update_mode_buttons()
    
    def _update_mode_buttons(self):
        """更新模式按钮状态"""
        # 重置所有按钮样式
        for btn in [self.drag_btn, self.draw_btn, self.rotate_btn, self.erase_btn]:
            btn.configure(style='TButton')
        
        # 设置当前模式按钮的样式
        current_mode = self.settings.operation_mode
        if current_mode == 'DRAG':
            self.drag_btn.configure(style='Accent.TButton')
        elif current_mode == 'DRAW':
            self.draw_btn.configure(style='Accent.TButton')
        elif current_mode == 'ROTATE':
            self.rotate_btn.configure(style='Accent.TButton')
        elif current_mode == 'ERASE':
            self.erase_btn.configure(style='Accent.TButton')
    
    # 障碍物创建
    def _create_obstacle(self, obstacle_type: str):
        """创建障碍物"""
        try:
            if obstacle_type == "background":
                self._set_background()
            else:
                # 获取画布中心位置
                canvas_width = self.settings.canvas_width
                canvas_height = self.settings.canvas_height
                x = canvas_width // 2
                y = canvas_height // 2
                
                # 创建障碍物
                self.obstacle_manager.create_obstacle(obstacle_type, x, y)
                messagebox.showinfo("成功", f"已创建{OBSTACLE_TYPES.get(obstacle_type, obstacle_type)}")
        except Exception as e:
            logging.error(f"创建障碍物失败: {e}")
            messagebox.showerror("错误", f"创建障碍物失败: {e}")
    
    def _clear_route(self):
        """清除路线"""
        try:
            self.canvas_manager.clear_lines()
            messagebox.showinfo("成功", "路线已清除")
        except Exception as e:
            logging.error(f"清除路线失败: {e}")
            messagebox.showerror("错误", f"清除路线失败: {e}")
    
    def _set_background(self):
        """设置背景图片"""
        try:
            from tkinter import filedialog
            file_path = filedialog.askopenfilename(
                title="选择背景图片",
                filetypes=[
                    ("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp"),
                    ("所有文件", "*.*")
                ]
            )
            
            if file_path:
                self.canvas_manager.set_background_image(file_path)
                messagebox.showinfo("成功", "背景图片已设置")
        except Exception as e:
            logging.error(f"设置背景图片失败: {e}")
            messagebox.showerror("错误", f"设置背景图片失败: {e}")
    
    def update_stats(self):
        """更新统计信息"""
        try:
            route_length = self.settings.get_total_route_length()
            obstacle_count = len(self.settings.obstacle_instances)
            
            self.route_length_label.config(text=f"路线长度: {route_length:.2f}m")
            self.obstacle_count_label.config(text=f"障碍数量: {obstacle_count}")
        except Exception as e:
            logging.error(f"更新统计信息失败: {e}")
