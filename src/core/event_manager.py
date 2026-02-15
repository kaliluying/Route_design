"""
事件管理器
统一处理应用程序的所有事件
"""

import logging
from typing import Dict, Any, Callable, Optional
import ttkbootstrap as ttk

from ..config import Settings, OPERATION_MODES


class EventManager:
    """事件管理器"""
    
    def __init__(self, window, settings: Settings):
        self.window = window
        self.settings = settings
        self.event_handlers: Dict[str, Callable] = {}
        self.keyboard_shortcuts: Dict[str, Callable] = {}
        
        self._setup_global_events()
        self._setup_keyboard_shortcuts()
    
    def _setup_global_events(self):
        """设置全局事件"""
        # 窗口事件
        self.window.protocol("WM_DELETE_WINDOW", self._on_window_close)
        
        # 全局键盘事件
        self.window.bind("<Command-KeyPress-z>", self._on_undo)
        self.window.bind("<Control-KeyPress-z>", self._on_undo)
        self.window.bind("<BackSpace>", self._on_delete)
        self.window.bind("<Delete>", self._on_delete)
        
        # 全局鼠标事件
        self.window.bind('<Button-1>', self._on_global_click)
    
    def _setup_keyboard_shortcuts(self):
        """设置键盘快捷键"""
        self.keyboard_shortcuts = {
            'ctrl+s': self._on_save,
            'ctrl+o': self._on_open,
            'ctrl+n': self._on_new,
            'ctrl+z': self._on_undo,
            'ctrl+y': self._on_redo,
            'delete': self._on_delete,
            'escape': self._on_escape,
        }
    
    def register_event_handler(self, event_name: str, handler: Callable):
        """注册事件处理器"""
        self.event_handlers[event_name] = handler
    
    def unregister_event_handler(self, event_name: str):
        """注销事件处理器"""
        if event_name in self.event_handlers:
            del self.event_handlers[event_name]
    
    def trigger_event(self, event_name: str, *args, **kwargs):
        """触发事件"""
        if event_name in self.event_handlers:
            try:
                self.event_handlers[event_name](*args, **kwargs)
            except Exception as e:
                logging.error(f"事件处理失败 {event_name}: {e}")
    
    def _on_window_close(self):
        """窗口关闭事件"""
        try:
            # 保存当前状态
            self.trigger_event('before_close')
            
            # 销毁窗口
            self.window.destroy()
        except Exception as e:
            logging.error(f"窗口关闭失败: {e}")
    
    def _on_undo(self, event):
        """撤销操作"""
        self.trigger_event('undo')
    
    def _on_redo(self, event):
        """重做操作"""
        self.trigger_event('redo')
    
    def _on_delete(self, event):
        """删除操作"""
        self.trigger_event('delete')
    
    def _on_save(self, event=None):
        """保存操作"""
        self.trigger_event('save')
    
    def _on_open(self, event=None):
        """打开操作"""
        self.trigger_event('open')
    
    def _on_new(self, event=None):
        """新建操作"""
        self.trigger_event('new')
    
    def _on_escape(self, event=None):
        """取消操作"""
        self.trigger_event('escape')
    
    def _on_global_click(self, event):
        """全局点击事件"""
        # 处理全局点击，如取消选择等
        self.trigger_event('global_click', event)
    
    def handle_keyboard_event(self, event):
        """处理键盘事件"""
        # 构建快捷键字符串
        modifiers = []
        if event.state & 0x4:  # Control
            modifiers.append('ctrl')
        if event.state & 0x8:  # Alt
            modifiers.append('alt')
        if event.state & 0x1:  # Shift
            modifiers.append('shift')
        
        key = event.keysym.lower()
        shortcut = '+'.join(modifiers + [key])
        
        if shortcut in self.keyboard_shortcuts:
            self.keyboard_shortcuts[shortcut](event)
            return True
        
        return False
    
    def set_operation_mode(self, mode: int):
        """设置操作模式"""
        self.settings.update_operation_mode(mode)
        self.trigger_event('operation_mode_changed', mode)
    
    def get_current_mode(self) -> int:
        """获取当前操作模式"""
        return self.settings.operation_mode
    
    def is_drag_mode(self) -> bool:
        """是否为拖拽模式"""
        return self.settings.operation_mode == OPERATION_MODES['DRAG']
    
    def is_draw_mode(self) -> bool:
        """是否为绘制模式"""
        return self.settings.operation_mode == OPERATION_MODES['DRAW']
    
    def is_rotate_mode(self) -> bool:
        """是否为旋转模式"""
        return self.settings.operation_mode == OPERATION_MODES['ROTATE']
    
    def is_erase_mode(self) -> bool:
        """是否为擦除模式"""
        return self.settings.operation_mode == OPERATION_MODES['ERASE']
