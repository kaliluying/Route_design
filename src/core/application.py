"""
应用程序主类
使用MVC模式组织代码结构
"""

import logging
import threading
import time
from typing import Optional
import tkinter as tk
from tkinter import ttk
# from ttkbootstrap.utility import enable_high_dpi_awareness

from ..config import Settings, APP_NAME, APP_VERSION, IS_WINDOWS, IS_MACOS
from .canvas_manager import CanvasManager
from .obstacle_manager import ObstacleManager
from .event_manager import EventManager
from .file_manager import FileManager
from ..ui.main_window import MainWindow


class Application:
    """应用程序主类"""
    
    def __init__(self):
        self.settings = Settings()
        self.window = None
        self.canvas_manager = None
        self.obstacle_manager = None
        self.event_manager = None
        self.file_manager = None
        self.main_window = None
        
        self._setup_window()
        self._setup_managers()
        self._setup_auto_save()
        self._setup_error_handling()
    
    def _setup_window(self):
        """设置主窗口"""
        self.window = tk.Tk()
        self.window.title(APP_NAME)
        try:
            self.window.iconphoto(True, tk.PhotoImage(file='img/ic.png'))
        except:
            pass
        
        # 设置窗口大小
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.window.geometry(f"{screen_width}x{screen_height}")
        
        # 高DPI支持
        if IS_WINDOWS:
            pass
            # enable_high_dpi_awareness(self.window, 2.0)
    
    def _setup_managers(self):
        """设置管理器"""
        self.canvas_manager = CanvasManager(self.window, self.settings)
        self.obstacle_manager = ObstacleManager(self.canvas_manager, self.settings)
        self.event_manager = EventManager(self.window, self.settings)
        self.file_manager = FileManager(self.settings)
        
        # 创建主窗口UI
        self.main_window = MainWindow(
            self.window,
            self.canvas_manager,
            self.obstacle_manager,
            self.event_manager,
            self.file_manager,
            self.settings
        )
    
    def _setup_auto_save(self):
        """设置自动保存"""
        def auto_save():
            while True:
                time.sleep(300)  # 5分钟自动保存
                try:
                    self.file_manager.auto_save()
                except Exception as e:
                    logging.error(f"自动保存失败: {e}")
        
        auto_save_thread = threading.Thread(target=auto_save, daemon=True)
        auto_save_thread.start()
    
    def _setup_error_handling(self):
        """设置错误处理"""
        def handle_exception(exctype, value, tb):
            error_msg = f"未处理的异常: {exctype.__name__}: {value}"
            logging.error(error_msg, exc_info=(exctype, value, tb))
            print(error_msg)
        
        self.window.report_callback_exception = handle_exception
    
    def run(self):
        """运行应用程序"""
        try:
            # 加载上次的会话
            self.file_manager.load_last_session()
            
            # 启动主循环
            self.window.mainloop()
        except Exception as e:
            logging.error(f"应用程序运行失败: {e}")
            raise
    
    def quit(self):
        """退出应用程序"""
        try:
            # 保存当前状态
            self.file_manager.save_current_session()
            
            # 销毁窗口
            if self.window:
                self.window.destroy()
        except Exception as e:
            logging.error(f"退出应用程序时出错: {e}")
    
    def get_version(self) -> str:
        """获取版本信息"""
        return APP_VERSION
    
    def check_for_updates(self) -> bool:
        """检查更新"""
        try:
            import requests
            response = requests.get("https://github.com/kaliluying/Route_design/raw/dev/version.txt")
            latest_version = response.text.strip()
            return latest_version != APP_VERSION
        except Exception as e:
            logging.error(f"检查更新失败: {e}")
            return False
