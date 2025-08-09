"""
障碍物基类
定义所有障碍物的通用接口和基本功能
"""

import math
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple
from functools import partial
import ttkbootstrap as ttk

from ..config import Settings, OPERATION_MODES


class BaseObstacle(ABC):
    """障碍物基类"""
    
    def __init__(self, canvas, index: int, settings: Settings, **kwargs):
        self.canvas = canvas
        self.index = index
        self.settings = settings
        self.tag = None
        self.id = None
        self.ui_state = True
        
        # 位置和角度
        self.current_x = kwargs.get('current_x', 160)
        self.current_y = kwargs.get('current_y', 25)
        self.angle = kwargs.get('angle', 0)
        self.temp_angle = kwargs.get('temp_angle', 0)
        self.lest_angle = kwargs.get('lest_angle', 0)
        
        # 拖拽相关
        self.start_x = kwargs.get('start_x', 160)
        self.start_y = kwargs.get('start_y', 25)
        
        # 初始化
        self._setup_obstacle()
        self._bind_events()
    
    @abstractmethod
    def _setup_obstacle(self):
        """设置障碍物（子类必须实现）"""
        pass
    
    def _bind_events(self):
        """绑定事件"""
        if self.tag:
            self.canvas.tag_bind(self.tag, "<Button-1>", partial(self._on_mouse_down, self.tag))
            self.canvas.tag_bind(self.tag, "<B1-Motion>", partial(self._on_drag, self.tag))
            self.canvas.tag_bind(self.tag, "<ButtonRelease-1>", self._on_mouse_up)
    
    def _on_mouse_down(self, tag, event):
        """鼠标按下事件"""
        # 设置当前障碍物
        self.canvas.image_data[self.id] = self
        
        # 更新坐标显示
        x = self.current_x / 10 - 1.5
        y = self.current_y / 10 - 5
        self.canvas.itemconfig('障碍x', text=f'x:{x:.2f}')
        self.canvas.itemconfig('障碍y', text=f'y:{y:.2f}')
        
        # 记录起始位置
        self.start_x = event.x
        self.start_y = event.y
        
        # 设置当前对象
        self.canvas.dtag('current', 'current')
        self.canvas.addtag_withtag('current', tag)
        
        # 提升层级
        self.canvas.lift(tag)
    
    def _on_drag(self, tag, event):
        """拖拽事件"""
        if self.settings.operation_mode == OPERATION_MODES['DRAG']:
            # 移动障碍物
            dx = event.x - self.start_x
            dy = event.y - self.start_y
            self.move(dx, dy)
            self.start_x = event.x
            self.start_y = event.y
        elif self.settings.operation_mode == OPERATION_MODES['ROTATE']:
            # 旋转障碍物
            self._handle_rotation(event)
    
    def _on_mouse_up(self, event):
        """鼠标释放事件"""
        # 记录操作历史
        if hasattr(self, '_last_operation'):
            self._record_operation()
    
    def _handle_rotation(self, event):
        """处理旋转"""
        # 计算旋转角度
        origin = (self.current_x, self.current_y)
        start = (self.start_x, self.start_y)
        end = (event.x, event.y)
        
        # 计算向量角度
        start_vector = (start[0] - origin[0], start[1] - origin[1])
        end_vector = (end[0] - origin[0], end[1] - origin[1])
        
        start_angle = math.atan2(start_vector[1], start_vector[0])
        end_angle = math.atan2(end_vector[1], end_vector[0])
        
        # 计算角度差
        angle_diff = math.degrees(end_angle - start_angle)
        new_angle = self.lest_angle + angle_diff
        
        # 确保角度在0-360范围内
        new_angle = new_angle % 360
        
        # 应用旋转
        self.rotate(new_angle)
        
        # 更新起始位置
        self.start_x = event.x
        self.start_y = event.y
    
    def move(self, dx: float, dy: float):
        """移动障碍物"""
        try:
            self.current_x += dx
            self.current_y += dy
            self.canvas.move(self.tag, dx, dy)
            self._update_position()
        except Exception as e:
            logging.error(f"移动障碍物失败: {e}")
    
    def rotate(self, angle: float):
        """旋转障碍物"""
        try:
            self.angle = angle
            self._apply_rotation()
            self._update_position()
        except Exception as e:
            logging.error(f"旋转障碍物失败: {e}")
    
    def scale(self, scale_factor: float):
        """缩放障碍物"""
        try:
            self._apply_scale(scale_factor)
            self._update_position()
        except Exception as e:
            logging.error(f"缩放障碍物失败: {e}")
    
    @abstractmethod
    def _apply_rotation(self):
        """应用旋转（子类必须实现）"""
        pass
    
    @abstractmethod
    def _apply_scale(self, scale_factor: float):
        """应用缩放（子类必须实现）"""
        pass
    
    def _update_position(self):
        """更新位置信息"""
        # 更新坐标显示
        x = self.current_x / 10 - 1.5
        y = self.current_y / 10 - 5
        self.canvas.itemconfig('障碍x', text=f'x:{x:.2f}')
        self.canvas.itemconfig('障碍y', text=f'y:{y:.2f}')
    
    def get_center(self) -> Tuple[float, float]:
        """获取障碍物中心点"""
        return (self.current_x, self.current_y)
    
    def get_bounds(self) -> Tuple[float, float, float, float]:
        """获取障碍物边界"""
        # 默认实现，子类可以重写
        return (self.current_x - 20, self.current_y - 20, 
                self.current_x + 20, self.current_y + 20)
    
    def delete(self):
        """删除障碍物"""
        try:
            if self.tag:
                self.canvas.delete(self.tag)
            if self.id in self.canvas.image_data:
                del self.canvas.image_data[self.id]
        except Exception as e:
            logging.error(f"删除障碍物失败: {e}")
    
    def duplicate(self) -> Optional['BaseObstacle']:
        """复制障碍物"""
        try:
            # 创建新的障碍物实例
            new_obstacle = self.__class__(
                self.canvas,
                self.index + 1,
                self.settings,
                current_x=self.current_x + 20,
                current_y=self.current_y + 20,
                angle=self.angle
            )
            return new_obstacle
        except Exception as e:
            logging.error(f"复制障碍物失败: {e}")
            return None
    
    @abstractmethod
    def save(self) -> Dict[str, Any]:
        """保存障碍物状态（子类必须实现）"""
        pass
    
    @classmethod
    @abstractmethod
    def load(cls, canvas, data: Dict[str, Any]) -> 'BaseObstacle':
        """加载障碍物状态（子类必须实现）"""
        pass
    
    def _record_operation(self):
        """记录操作历史"""
        # 可以在这里实现撤销/重做功能
        pass
    
    def set_visible(self, visible: bool):
        """设置可见性"""
        try:
            state = 'normal' if visible else 'hidden'
            self.canvas.itemconfig(self.tag, state=state)
            self.ui_state = visible
        except Exception as e:
            logging.error(f"设置障碍物可见性失败: {e}")
    
    def bring_to_front(self):
        """置于顶层"""
        try:
            self.canvas.lift(self.tag)
        except Exception as e:
            logging.error(f"将障碍物置于顶层失败: {e}")
    
    def send_to_back(self):
        """置于底层"""
        try:
            self.canvas.lower(self.tag)
            self.canvas.lower("watermark")
        except Exception as e:
            logging.error(f"将障碍物置于底层失败: {e}")
    
    def __str__(self):
        return f"{self.__class__.__name__}(index={self.index}, pos=({self.current_x:.1f}, {self.current_y:.1f}))"
    
    def __repr__(self):
        return self.__str__()
