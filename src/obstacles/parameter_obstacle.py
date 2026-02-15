"""
参数障碍物类
继承自BaseObstacle，实现参数类型的障碍物
"""

import tkinter as tk
from tkinter import ttk
from typing import Dict, Any, Optional, Tuple, List

from .base_obstacle import BaseObstacle
from ..config import Settings, OBSTACLE_CONFIG


class ParameterObstacle(BaseObstacle):
    """参数障碍物类"""
    
    def __init__(self, canvas: tk.Canvas, parameter_type: str = "", x: float = 0, y: float = 0, 
                 angle: float = 0, scale: float = 1.0, settings: Optional[Settings] = None):
        """
        初始化参数障碍物
        
        Args:
            canvas: 画布对象
            parameter_type: 参数类型
            x: x坐标
            y: y坐标
            angle: 旋转角度
            scale: 缩放比例
            settings: 设置对象
        """
        self.parameter_type = parameter_type
        self.parameter_value = ""
        self.unit = ""
        self.parameter_ids = []  # 存储所有画布元素的ID
        self.font_family = OBSTACLE_CONFIG.get('parameter_font_family', 'Arial')
        self.font_size = OBSTACLE_CONFIG.get('parameter_font_size', 10)
        self.font_weight = OBSTACLE_CONFIG.get('parameter_font_weight', 'normal')
        self.text_color = OBSTACLE_CONFIG.get('parameter_text_color', 'black')
        self.background_color = OBSTACLE_CONFIG.get('parameter_background_color', 'lightyellow')
        self.border_color = OBSTACLE_CONFIG.get('parameter_border_color', 'orange')
        self.border_width = OBSTACLE_CONFIG.get('parameter_border_width', 2)
        
        super().__init__(canvas, x, y, angle, scale, settings)
    
    def _setup_obstacle(self) -> None:
        """设置障碍物"""
        # 创建参数显示框
        self._create_parameter_display()
    
    def _create_parameter_display(self) -> None:
        """创建参数显示框"""
        # 计算显示文本
        display_text = self._get_display_text()
        
        # 创建背景矩形
        font = (self.font_family, int(self.font_size * self.scale), self.font_weight)
        
        # 估算文本尺寸
        text_width = len(display_text) * self.font_size * 0.6 * self.scale
        text_height = self.font_size * self.scale
        
        # 添加内边距
        padding = 8
        rect_width = text_width + padding * 2
        rect_height = text_height + padding * 2
        
        # 创建背景矩形
        rect_id = self.canvas.create_rectangle(
            self.x - rect_width/2, self.y - rect_height/2,
            self.x + rect_width/2, self.y + rect_height/2,
            fill=self.background_color,
            outline=self.border_color,
            width=self.border_width,
            tags=self.tag
        )
        self.parameter_ids.append(rect_id)
        
        # 创建文本
        text_id = self.canvas.create_text(
            self.x, self.y,
            text=display_text,
            font=font,
            fill=self.text_color,
            tags=self.tag
        )
        self.parameter_ids.append(text_id)
        
        # 如果有参数类型，创建类型标签
        if self.parameter_type:
            self._create_type_label()
    
    def _create_type_label(self) -> None:
        """创建类型标签"""
        # 在参数框上方创建类型标签
        label_font = (self.font_family, int((self.font_size - 2) * self.scale), 'bold')
        label_text = f"[{self.parameter_type}]"
        
        # 估算标签尺寸
        label_width = len(label_text) * (self.font_size - 2) * 0.6 * self.scale
        label_height = (self.font_size - 2) * self.scale
        
        # 计算标签位置（在参数框上方）
        label_y = self.y - label_height - 5
        
        # 创建标签背景
        label_padding = 3
        label_rect_id = self.canvas.create_rectangle(
            self.x - label_width/2 - label_padding, label_y - label_height/2 - label_padding,
            self.x + label_width/2 + label_padding, label_y + label_height/2 + label_padding,
            fill='white',
            outline=self.border_color,
            width=1,
            tags=self.tag
        )
        self.parameter_ids.append(label_rect_id)
        
        # 创建标签文本
        label_text_id = self.canvas.create_text(
            self.x, label_y,
            text=label_text,
            font=label_font,
            fill=self.border_color,
            tags=self.tag
        )
        self.parameter_ids.append(label_text_id)
    
    def _get_display_text(self) -> str:
        """获取显示文本"""
        if self.parameter_value:
            if self.unit:
                return f"{self.parameter_value} {self.unit}"
            else:
                return self.parameter_value
        else:
            return "参数值"
    
    def set_parameter(self, value: str, unit: str = "") -> None:
        """设置参数值"""
        self.parameter_value = value
        self.unit = unit
        self._update_display()
    
    def set_parameter_type(self, parameter_type: str) -> None:
        """设置参数类型"""
        self.parameter_type = parameter_type
        self._update_display()
    
    def _update_display(self) -> None:
        """更新显示"""
        # 删除旧的显示元素
        for element_id in self.parameter_ids:
            self.canvas.delete(element_id)
        self.parameter_ids.clear()
        
        # 重新创建显示
        self._create_parameter_display()
    
    def _apply_rotation(self) -> None:
        """应用旋转"""
        # 对于参数障碍物，我们通常不需要旋转，因为文本应该保持可读
        # 但如果有特殊需求，可以在这里实现
        pass
    
    def _apply_scale(self) -> None:
        """应用缩放"""
        # 重新创建显示以应用新的缩放
        self._update_display()
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """获取边界"""
        if self.parameter_ids:
            # 获取所有元素的边界
            all_bboxes = []
            for element_id in self.parameter_ids:
                bbox = self.canvas.bbox(element_id)
                if bbox:
                    all_bboxes.append(bbox)
            
            if all_bboxes:
                # 计算所有边界的并集
                min_x = min(bbox[0] for bbox in all_bboxes)
                min_y = min(bbox[1] for bbox in all_bboxes)
                max_x = max(bbox[2] for bbox in all_bboxes)
                max_y = max(bbox[3] for bbox in all_bboxes)
                return (min_x, min_y, max_x, max_y)
        
        # 默认边界
        text_width = len(self._get_display_text()) * self.font_size * 0.6 * self.scale
        text_height = self.font_size * self.scale
        return (self.x - text_width/2, self.y - text_height/2, 
                self.x + text_width/2, self.y + text_height/2)
    
    def save(self) -> Dict[str, Any]:
        """保存障碍物数据"""
        data = super().save()
        data.update({
            'type': 'parameter',
            'parameter_type': self.parameter_type,
            'parameter_value': self.parameter_value,
            'unit': self.unit,
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
        self.parameter_type = data.get('parameter_type', '')
        self.parameter_value = data.get('parameter_value', '')
        self.unit = data.get('unit', '')
        self.font_family = data.get('font_family', 'Arial')
        self.font_size = data.get('font_size', 10)
        self.font_weight = data.get('font_weight', 'normal')
        self.text_color = data.get('text_color', 'black')
        self.background_color = data.get('background_color', 'lightyellow')
        self.border_color = data.get('border_color', 'orange')
        self.border_width = data.get('border_width', 2)
        
        # 重新设置障碍物
        self._setup_obstacle()
        self._apply_rotation()
        self._apply_scale()
    
    def duplicate(self) -> 'ParameterObstacle':
        """复制障碍物"""
        new_obstacle = ParameterObstacle(
            self.canvas, self.parameter_type,
            self.x + 20, self.y + 20,  # 稍微偏移位置
            self.angle, self.scale, self.settings
        )
        # 复制参数设置
        new_obstacle.parameter_value = self.parameter_value
        new_obstacle.unit = self.unit
        new_obstacle.font_family = self.font_family
        new_obstacle.font_size = self.font_size
        new_obstacle.font_weight = self.font_weight
        new_obstacle.text_color = self.text_color
        new_obstacle.background_color = self.background_color
        new_obstacle.border_color = self.border_color
        new_obstacle.border_width = self.border_width
        
        return new_obstacle
    
    def delete(self) -> None:
        """删除障碍物"""
        # 删除所有画布元素
        for element_id in self.parameter_ids:
            self.canvas.delete(element_id)
        self.parameter_ids.clear()
        
        # 调用父类的删除方法
        super().delete()
