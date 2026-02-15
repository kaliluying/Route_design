#!/usr/bin/env python3
"""
马术路线设计软件 - 测试版本
使用标准tkinter的简化版本
"""

import sys
import os
import logging
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

import tkinter as tk
from tkinter import ttk, messagebox
from src.config import Settings, APP_NAME, APP_VERSION


class SimpleApplication:
    """简化的应用程序类"""
    
    def __init__(self):
        """初始化应用程序"""
        # 初始化设置
        self.settings = Settings()
        
        # 创建主窗口
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        self.root.geometry("1200x800")
        
        # 设置窗口图标（如果有的话）
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
        
        # 创建界面
        self._create_widgets()
        
        # 设置关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_widgets(self):
        """创建界面组件"""
        # 创建菜单栏
        self._create_menu()
        
        # 创建主框架
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 创建工具栏
        toolbar_frame = ttk.Frame(main_frame)
        toolbar_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 工具栏按钮
        ttk.Button(toolbar_frame, text="新建", command=self._new_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar_frame, text="打开", command=self._open_project).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar_frame, text="保存", command=self._save_project).pack(side=tk.LEFT, padx=5)
        ttk.Separator(toolbar_frame, orient=tk.VERTICAL).pack(side=tk.LEFT, fill=tk.Y, padx=10)
        ttk.Button(toolbar_frame, text="图像障碍物", command=self._create_image_obstacle).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar_frame, text="文本障碍物", command=self._create_text_obstacle).pack(side=tk.LEFT, padx=5)
        ttk.Button(toolbar_frame, text="参数障碍物", command=self._create_parameter_obstacle).pack(side=tk.LEFT, padx=5)
        
        # 创建画布框架
        canvas_frame = ttk.Frame(main_frame)
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建画布
        self.canvas = tk.Canvas(
            canvas_frame,
            width=self.settings.canvas_width,
            height=self.settings.canvas_height,
            bg="white",
            relief=tk.SUNKEN,
            bd=2
        )
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # 创建状态栏
        status_frame = ttk.Frame(main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="就绪")
        self.status_label.pack(side=tk.LEFT)
        
        # 绑定画布事件
        self.canvas.bind("<Button-1>", self._on_canvas_click)
        self.canvas.bind("<B1-Motion>", self._on_canvas_drag)
        self.canvas.bind("<ButtonRelease-1>", self._on_canvas_release)
    
    def _create_menu(self):
        """创建菜单栏"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # 文件菜单
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="文件", menu=file_menu)
        file_menu.add_command(label="新建", command=self._new_project)
        file_menu.add_command(label="打开", command=self._open_project)
        file_menu.add_command(label="保存", command=self._save_project)
        file_menu.add_separator()
        file_menu.add_command(label="退出", command=self._on_closing)
        
        # 编辑菜单
        edit_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="编辑", menu=edit_menu)
        edit_menu.add_command(label="撤销", command=self._undo)
        edit_menu.add_command(label="重做", command=self._redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="删除", command=self._delete)
        
        # 视图菜单
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="视图", menu=view_menu)
        view_menu.add_checkbutton(label="显示网格", command=self._toggle_grid)
        view_menu.add_checkbutton(label="显示辅助信息", command=self._toggle_aux_info)
        view_menu.add_checkbutton(label="显示水印", command=self._toggle_watermark)
        
        # 帮助菜单
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="帮助", menu=help_menu)
        help_menu.add_command(label="关于", command=self._show_about)
    
    def _new_project(self):
        """新建项目"""
        if messagebox.askyesno("确认", "是否创建新项目？当前项目将被清除。"):
            self.canvas.delete("all")
            self.status_label.config(text="新建项目")
    
    def _open_project(self):
        """打开项目"""
        messagebox.showinfo("信息", "打开项目功能待实现")
    
    def _save_project(self):
        """保存项目"""
        messagebox.showinfo("信息", "保存项目功能待实现")
    
    def _create_image_obstacle(self):
        """创建图像障碍物"""
        messagebox.showinfo("信息", "创建图像障碍物功能待实现")
    
    def _create_text_obstacle(self):
        """创建文本障碍物"""
        messagebox.showinfo("信息", "创建文本障碍物功能待实现")
    
    def _create_parameter_obstacle(self):
        """创建参数障碍物"""
        messagebox.showinfo("信息", "创建参数障碍物功能待实现")
    
    def _undo(self):
        """撤销"""
        messagebox.showinfo("信息", "撤销功能待实现")
    
    def _redo(self):
        """重做"""
        messagebox.showinfo("信息", "重做功能待实现")
    
    def _delete(self):
        """删除"""
        messagebox.showinfo("信息", "删除功能待实现")
    
    def _toggle_grid(self):
        """切换网格显示"""
        messagebox.showinfo("信息", "网格显示功能待实现")
    
    def _toggle_aux_info(self):
        """切换辅助信息显示"""
        messagebox.showinfo("信息", "辅助信息显示功能待实现")
    
    def _toggle_watermark(self):
        """切换水印显示"""
        messagebox.showinfo("信息", "水印显示功能待实现")
    
    def _show_about(self):
        """显示关于对话框"""
        about_text = f"""
{APP_NAME} v{APP_VERSION}

马术路线设计软件

这是一个专业的马术路线设计工具，
帮助用户创建和编辑马术比赛路线图。

© 2024 山东体育学院. 保留所有权利.
        """
        messagebox.showinfo("关于", about_text)
    
    def _on_canvas_click(self, event):
        """画布点击事件"""
        self.status_label.config(text=f"点击位置: ({event.x}, {event.y})")
    
    def _on_canvas_drag(self, event):
        """画布拖拽事件"""
        pass
    
    def _on_canvas_release(self, event):
        """画布释放事件"""
        pass
    
    def _on_closing(self):
        """关闭事件"""
        if messagebox.askyesno("确认", "确定要退出程序吗？"):
            self.root.destroy()
    
    def run(self):
        """运行应用程序"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n程序被用户中断")
        except Exception as e:
            logging.error(f"程序运行失败: {e}")
            messagebox.showerror("错误", f"程序运行失败: {e}")


def main():
    """主函数"""
    try:
        # 创建并运行应用程序
        app = SimpleApplication()
        app.run()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        logging.error(f"程序运行失败: {e}")
        print(f"程序运行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
