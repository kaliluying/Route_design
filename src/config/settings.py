"""
应用程序设置管理
使用单例模式管理全局设置
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional
from .constants import *


class Settings:
    """应用程序设置管理类"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            self._load_default_settings()
            self._setup_logging()
            self._ensure_directories()
    
    def _load_default_settings(self):
        """加载默认设置"""
        self.canvas_width = UI_CONFIG['default_width']
        self.canvas_height = UI_CONFIG['default_height']
        self.obstacle_length = OBSTACLE_CONFIG['default_length']
        self.font_size = OBSTACLE_CONFIG['font_size']
        self.remove_size = OBSTACLE_CONFIG['remove_size']
        self.operation_mode = OPERATION_MODES['DRAG']
        self.show_grid = False
        self.show_aux_info = True
        self.show_arc = False
        self.show_watermark = True
        self.background_image = None
        self.event_info = {}
        self.lines = []
        self.arc_list = []
        self.obstacle_instances = []
    
    def _setup_logging(self):
        """设置日志"""
        logging.basicConfig(
            format='%(asctime)s.%(msecs)03d [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s',
            filename='logging.log',
            level=logging.INFO
        )
    
    def _ensure_directories(self):
        """确保必要的目录存在"""
        for directory in [BACKUP_DIR, AUTO_BACKUP_DIR, DOWNLOAD_DIR]:
            directory.mkdir(exist_ok=True)
    
    def update_canvas_size(self, width: int, height: int):
        """更新画布尺寸"""
        self.canvas_width = width
        self.canvas_height = height
    
    def update_obstacle_length(self, length: float):
        """更新障碍物长度"""
        self.obstacle_length = length
    
    def update_operation_mode(self, mode: int):
        """更新操作模式"""
        self.operation_mode = mode
    
    def set_operation_mode(self, mode: str):
        """设置操作模式（字符串版本）"""
        mode_map = {
            'DRAG': OPERATION_MODES['DRAG'],
            'DRAW': OPERATION_MODES['DRAW'],
            'ROTATE': OPERATION_MODES['ROTATE'],
            'ERASE': OPERATION_MODES['ERASE']
        }
        self.operation_mode = mode_map.get(mode, OPERATION_MODES['DRAG'])
    
    def set_default_obstacle_length(self, length: float):
        """设置默认障碍物长度"""
        self.obstacle_length = length
    
    def get_total_route_length(self) -> float:
        """获取总路线长度"""
        total_length = 0.0
        for line in self.lines:
            total_length += line.get('length', 0.0)
        return total_length
    
    def toggle_grid(self):
        """切换网格显示"""
        self.show_grid = not self.show_grid
    
    def toggle_aux_info(self):
        """切换辅助信息显示"""
        self.show_aux_info = not self.show_aux_info
    
    def toggle_arc(self):
        """切换弧线显示"""
        self.show_arc = not self.show_arc
    
    def toggle_watermark(self):
        """切换水印显示"""
        self.show_watermark = not self.show_watermark
    
    def set_background_image(self, image_path: Optional[str]):
        """设置背景图片"""
        self.background_image = image_path
    
    def update_event_info(self, info: Dict[str, str]):
        """更新赛事信息"""
        self.event_info.update(info)
    
    def add_line(self, line_data: Dict[str, Any]):
        """添加路线"""
        self.lines.append(line_data)
    
    def clear_lines(self):
        """清除所有路线"""
        self.lines.clear()
    
    def add_arc(self, arc_data: tuple):
        """添加弧线"""
        self.arc_list.append(arc_data)
    
    def clear_arcs(self):
        """清除所有弧线"""
        self.arc_list.clear()
    
    def add_obstacle_instance(self, instance):
        """添加障碍物实例"""
        self.obstacle_instances.append(instance)
    
    def clear_obstacle_instances(self):
        """清除所有障碍物实例"""
        self.obstacle_instances.clear()
    
    def save_to_file(self, file_path: str):
        """保存设置到文件"""
        data = {
            'canvas_width': self.canvas_width,
            'canvas_height': self.canvas_height,
            'obstacle_length': self.obstacle_length,
            'font_size': self.font_size,
            'remove_size': self.remove_size,
            'operation_mode': self.operation_mode,
            'show_grid': self.show_grid,
            'show_aux_info': self.show_aux_info,
            'show_arc': self.show_arc,
            'show_watermark': self.show_watermark,
            'background_image': self.background_image,
            'event_info': self.event_info,
            'lines': self.lines,
            'arc_list': self.arc_list,
        }
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def load_from_file(self, file_path: str):
        """从文件加载设置"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.canvas_width = data.get('canvas_width', UI_CONFIG['default_width'])
            self.canvas_height = data.get('canvas_height', UI_CONFIG['default_height'])
            self.obstacle_length = data.get('obstacle_length', OBSTACLE_CONFIG['default_length'])
            self.font_size = data.get('font_size', OBSTACLE_CONFIG['font_size'])
            self.remove_size = data.get('remove_size', OBSTACLE_CONFIG['remove_size'])
            self.operation_mode = data.get('operation_mode', OPERATION_MODES['DRAG'])
            self.show_grid = data.get('show_grid', False)
            self.show_aux_info = data.get('show_aux_info', True)
            self.show_arc = data.get('show_arc', False)
            self.show_watermark = data.get('show_watermark', True)
            self.background_image = data.get('background_image')
            self.event_info = data.get('event_info', {})
            self.lines = data.get('lines', [])
            self.arc_list = data.get('arc_list', [])
            
            return True
        except Exception as e:
            logging.error(f"加载设置文件失败: {e}")
            return False
    
    def get_ui_config(self) -> Dict[str, Any]:
        """获取UI配置"""
        return {
            'width': self.canvas_width + UI_CONFIG['canvas_padding'],
            'height': self.canvas_height + UI_CONFIG['canvas_height_padding'],
            'font': UI_CONFIG['font'],
            'confirm_style': UI_CONFIG['confirm_style'],
            'button_style': UI_CONFIG['button_style'],
        }
    
    def get_obstacle_config(self) -> Dict[str, Any]:
        """获取障碍物配置"""
        return {
            'length': self.obstacle_length,
            'font_size': self.font_size,
            'remove_size': self.remove_size,
            **OBSTACLE_CONFIG
        }
