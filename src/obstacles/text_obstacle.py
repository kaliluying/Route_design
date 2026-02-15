"""
文本障碍物类
继承自BaseObstacle，实现文本类型的障碍物
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, Tuple

from .base_obstacle import BaseObstacle
from ..config import Settings, OBSTACLE_CONFIG


class TextObstacle(BaseObstacle):
    """文本障碍物类"""
    
    def __init__(self, canvas: tk.Canvas, text: str = "", x: float = 0, y: float = 0, 
                 angle: float = 0, scale: float = 1.0, settings: Optional[Settings] = None):
        """
        初始化文本障碍物
        
        Args:
            canvas: 画布对象
            text: 文本内容
            x: x坐标
            y: y坐标
            angle: 旋转角度
            scale: 缩放比例
            settings: 设置对象
        """
        self.text = text
        self.text_id = None
        self.font_family = OBSTACLE_CONFIG.get('text_font_family', 'Arial')
        self.font_size = OBSTACLE_CONFIG.get('text_font_size', 12)
        self.font_weight = OBSTACLE_CONFIG.get('text_font_weight', 'normal')
        self.text_color = OBSTACLE_CONFIG.get('text_color', 'black')
        self.background_color = OBSTACLE_CONFIG.get('text_background_color', 'white')
        self.border_color = OBSTACLE_CONFIG.get('text_border_color', 'black')
        self.border_width = OBSTACLE_CONFIG.get('text_border_width', 1)
        
        super().__init__(canvas, x, y, angle, scale, settings)
    
    def _setup_obstacle(self) -> None:
        """设置障碍物"""
        # 创建文本
        font = (self.font_family, int(self.font_size * self.scale), self.font_weight)
        
        self.text_id = self.canvas.create_text(
            self.x, self.y,
            text=self.text,
            font=font,
            fill=self.text_color,
            tags=self.tag
        )
        
        # 如果有背景色或边框，创建背景矩形
        if self.background_color != 'transparent' or self.border_width > 0:
            self._create_background()
    
    def _create_background(self) -> None:
        """创建背景矩形"""
        if not self.text_id:
            return
        
        # 获取文本边界
        bbox = self.canvas.bbox(self.text_id)
        if not bbox:
            return
        
        # 添加一些内边距
        padding = 5
        x1, y1, x2, y2 = bbox
        x1 -= padding
        y1 -= padding
        x2 += padding
        y2 += padding
        
        # 创建背景矩形
        self.background_id = self.canvas.create_rectangle(
            x1, y1, x2, y2,
            fill=self.background_color if self.background_color != 'transparent' else '',
            outline=self.border_color if self.border_width > 0 else '',
            width=self.border_width,
            tags=self.tag
        )
        
        # 将背景矩形移到文本后面
        self.canvas.tag_lower(self.background_id, self.text_id)
    
    def _apply_rotation(self) -> None:
        """应用旋转"""
        if self.text_id:
            # 对于文本，我们使用画布的旋转功能
            self.canvas.itemconfig(self.text_id, angle=-self.angle)
            
            if hasattr(self, 'background_id') and self.background_id:
                self.canvas.itemconfig(self.background_id, angle=-self.angle)
    
    def _apply_scale(self) -> None:
        """应用缩放"""
        if self.text_id:
            # 更新字体大小
            font = (self.font_family, int(self.font_size * self.scale), self.font_weight)
            self.canvas.itemconfig(self.text_id, font=font)
            
            # 重新创建背景
            if hasattr(self, 'background_id') and self.background_id:
                self.canvas.delete(self.background_id)
            self._create_background()
    
    def set_text(self, text: str) -> None:
        """设置文本内容"""
        self.text = text
        if self.text_id:
            self.canvas.itemconfig(self.text_id, text=text)
            # 重新创建背景以适应新文本
            if hasattr(self, 'background_id') and self.background_id:
                self.canvas.delete(self.background_id)
            self._create_background()
    
    def set_font(self, font_family: str = None, font_size: int = None, 
                font_weight: str = None) -> None:
        """设置字体"""
        if font_family:
            self.font_family = font_family
        if font_size:
            self.font_size = font_size
        if font_weight:
            self.font_weight = font_weight
        
        if self.text_id:
            font = (self.font_family, int(self.font_size * self.scale), self.font_weight)
            self.canvas.itemconfig(self.text_id, font=font)
    
    def set_colors(self, text_color: str = None, background_color: str = None, 
                  border_color: str = None) -> None:
        """设置颜色"""
        if text_color:
            self.text_color = text_color
            if self.text_id:
                self.canvas.itemconfig(self.text_id, fill=text_color)
        
        if background_color:
            self.background_color = background_color
        
        if border_color:
            self.border_color = border_color
        
        # 重新创建背景
        if hasattr(self, 'background_id') and self.background_id:
            self.canvas.delete(self.background_id)
        self._create_background()
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """获取边界"""
        if self.text_id:
            bbox = self.canvas.bbox(self.text_id)
            if bbox:
                return bbox
        
        # 默认边界
        text_width = len(self.text) * self.font_size * 0.6 * self.scale
        text_height = self.font_size * self.scale
        return (self.x - text_width/2, self.y - text_height/2, 
                self.x + text_width/2, self.y + text_height/2)
    
    def save(self) -> Dict[str, Any]:
        """保存障碍物数据"""
        data = super().save()
        data.update({
            'type': 'text',
            'text': self.text,
            'font_family': self.font_family,
            'font_size': self.font_size,
            'font_weight': self.font_weight,
            'text_color': self.text_color,
            'background_color': self.background_color,
            'border_color': self.border_color,
            'border_width': self.border_width
        })
        return data
    
    def load(self, data: Dict[str, Any]) -> None:
        """加载障碍物数据"""
        super().load(data)
        self.text = data.get('text', '')
        self.font_family = data.get('font_family', 'Arial')
        self.font_size = data.get('font_size', 12)
        self.font_weight = data.get('font_weight', 'normal')
        self.text_color = data.get('text_color', 'black')
        self.background_color = data.get('background_color', 'white')
        self.border_color = data.get('border_color', 'black')
        self.border_width = data.get('border_width', 1)
        
        # 重新设置障碍物
        self._setup_obstacle()
        self._apply_rotation()
        self._apply_scale()
    
    def duplicate(self) -> 'TextObstacle':
        """复制障碍物"""
        new_obstacle = TextObstacle(
            self.canvas, self.text,
            self.x + 20, self.y + 20,  # 稍微偏移位置
            self.angle, self.scale, self.settings
        )
        # 复制字体和颜色设置
        new_obstacle.font_family = self.font_family
        new_obstacle.font_size = self.font_size
        new_obstacle.font_weight = self.font_weight
        new_obstacle.text_color = self.text_color
        new_obstacle.background_color = self.background_color
        new_obstacle.border_color = self.border_color
        new_obstacle.border_width = self.border_width
        
        return new_obstacle
