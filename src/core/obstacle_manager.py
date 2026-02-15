"""
障碍物管理器
负责所有障碍物的创建、管理和操作
"""

import logging
import math
from typing import Dict, Any, Optional, List, Tuple
from functools import partial
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from ..config import Settings, OBSTACLE_TYPES, IMAGE_PATHS
from ..obstacles.base_obstacle import BaseObstacle
from ..obstacles.image_obstacle import ImageObstacle
from ..obstacles.text_obstacle import TextObstacle
from ..obstacles.parameter_obstacle import ParameterObstacle


class ObstacleManager:
    """障碍物管理器"""
    
    def __init__(self, canvas_manager, settings: Settings):
        self.canvas_manager = canvas_manager
        self.settings = settings
        self.canvas = canvas_manager.get_canvas()
        self.image_data = canvas_manager.get_image_data()
        
        self.obstacles: List[BaseObstacle] = []
        self.current_obstacle: Optional[BaseObstacle] = None
        self.obstacle_counter = 0
        self.text_counter = 0
        self.parameter_counter = 0
        
        # 弧线相关
        self.arc_list = []
        self.arc_click = 0
        self.arc_start = None
        self.arc_start_obj = None
        self.arc_end_obj = None
    
    def create_obstacle(self, obstacle_type: str, x: float = None, y: float = None, **kwargs) -> Optional[BaseObstacle]:
        """创建障碍物"""
        try:
            if obstacle_type in OBSTACLE_TYPES:
                # 如果没有提供位置，使用画布中心
                if x is None or y is None:
                    x = self.settings.canvas_width // 2
                    y = self.settings.canvas_height // 2
                
                obstacle = ImageObstacle(
                    self.canvas,
                    obstacle_type,
                    x,
                    y,
                    0,  # 默认角度
                    1.0,  # 默认缩放
                    self.settings
                )
                self.obstacles.append(obstacle)
                self.obstacle_counter += 1
                self.settings.add_obstacle_instance(obstacle)
                return obstacle
            else:
                logging.error(f"未知的障碍物类型: {obstacle_type}")
                return None
        except Exception as e:
            logging.error(f"创建障碍物失败: {e}")
            return None
    
    def create_text_obstacle(self, text: str, **kwargs) -> Optional[TextObstacle]:
        """创建文字障碍物"""
        try:
            obstacle = TextObstacle(
                self.canvas,
                self.text_counter,
                text,
                self.settings,
                **kwargs
            )
            self.obstacles.append(obstacle)
            self.text_counter += 1
            self.settings.add_obstacle_instance(obstacle)
            return obstacle
        except Exception as e:
            logging.error(f"创建文字障碍物失败: {e}")
            return None
    
    def create_parameter_obstacle(self, parameter: str, **kwargs) -> Optional[ParameterObstacle]:
        """创建参数障碍物"""
        try:
            obstacle = ParameterObstacle(
                self.canvas,
                self.parameter_counter,
                parameter,
                self.settings,
                **kwargs
            )
            self.obstacles.append(obstacle)
            self.parameter_counter += 1
            self.settings.add_obstacle_instance(obstacle)
            return obstacle
        except Exception as e:
            logging.error(f"创建参数障碍物失败: {e}")
            return None
    
    def select_obstacle(self, obstacle: BaseObstacle):
        """选择障碍物"""
        self.current_obstacle = obstacle
        if obstacle:
            # 更新坐标显示
            x = obstacle.current_x / 10 - 1.5
            y = obstacle.current_y / 10 - 5
            self.canvas.itemconfig('障碍x', text=f'x:{x:.2f}')
            self.canvas.itemconfig('障碍y', text=f'y:{y:.2f}')
    
    def delete_obstacle(self, obstacle: BaseObstacle):
        """删除障碍物"""
        try:
            if obstacle in self.obstacles:
                self.obstacles.remove(obstacle)
                obstacle.delete()
                if self.current_obstacle == obstacle:
                    self.current_obstacle = None
                self.settings.obstacle_instances.remove(obstacle)
        except Exception as e:
            logging.error(f"删除障碍物失败: {e}")
    
    def delete_selected_obstacles(self):
        """删除选中的障碍物"""
        selected_items = self.canvas.find_withtag("choice_start")
        if selected_items:
            for item_id in selected_items[:-1]:  # 排除最后一个（通常是选择框）
                if item_id in self.image_data:
                    obstacle = self.image_data[item_id]
                    self.delete_obstacle(obstacle)
            
            # 清除选择状态
            self.canvas.itemconfig('choice', state='hidden')
            self.canvas.itemconfig('choice_start', state='hidden')
            self.canvas.dtag('choice_start', 'choice_start')
    
    def delete_selected(self):
        """删除选中项（简化版本）"""
        try:
            # 删除所有障碍物（简化实现）
            self.clear_all_obstacles()
            return True
        except Exception as e:
            logging.error(f"删除选中项失败: {e}")
            return False
    
    def move_obstacle(self, obstacle: BaseObstacle, dx: float, dy: float):
        """移动障碍物"""
        try:
            obstacle.move(dx, dy)
            # 更新弧线
            self._update_arcs()
        except Exception as e:
            logging.error(f"移动障碍物失败: {e}")
    
    def rotate_obstacle(self, obstacle: BaseObstacle, angle: float):
        """旋转障碍物"""
        try:
            obstacle.rotate(angle)
            # 更新弧线
            self._update_arcs()
        except Exception as e:
            logging.error(f"旋转障碍物失败: {e}")
    
    def scale_obstacle(self, obstacle: BaseObstacle, scale_factor: float):
        """缩放障碍物"""
        try:
            obstacle.scale(scale_factor)
        except Exception as e:
            logging.error(f"缩放障碍物失败: {e}")
    
    def get_obstacle_at_position(self, x: float, y: float) -> Optional[BaseObstacle]:
        """获取指定位置的障碍物"""
        items = self.canvas.find_overlapping(x-5, y-5, x+5, y+5)
        for item_id in items:
            if item_id in self.image_data:
                return self.image_data[item_id]
        return None
    
    def get_all_obstacles(self) -> List[BaseObstacle]:
        """获取所有障碍物"""
        return self.obstacles.copy()
    
    def clear_all_obstacles(self):
        """清除所有障碍物"""
        for obstacle in self.obstacles[:]:
            self.delete_obstacle(obstacle)
    
    def save_obstacles(self) -> Dict[str, Any]:
        """保存所有障碍物状态"""
        data = {}
        for obstacle in self.obstacles:
            if obstacle.ui_state:
                obstacle_data = obstacle.save()
                data.update(obstacle_data)
        return data
    
    def load_obstacles(self, data: Dict[str, Any]):
        """加载障碍物状态"""
        try:
            # 清除现有障碍物
            self.clear_all_obstacles()
            
            # 加载障碍物数据
            for key, value in data.items():
                if '障碍组件' in key:
                    obstacle = ImageObstacle.load(self.canvas, value)
                    self.obstacles.append(obstacle)
                    self.settings.add_obstacle_instance(obstacle)
                elif '障碍号' in key:
                    obstacle = TextObstacle.load(self.canvas, value)
                    self.obstacles.append(obstacle)
                    self.settings.add_obstacle_instance(obstacle)
                elif '障碍备注' in key:
                    obstacle = ParameterObstacle.load(self.canvas, value)
                    self.obstacles.append(obstacle)
                    self.settings.add_obstacle_instance(obstacle)
            
            # 更新计数器
            self._update_counters()
            
        except Exception as e:
            logging.error(f"加载障碍物失败: {e}")
    
    def _update_counters(self):
        """更新计数器"""
        self.obstacle_counter = max([obs.index for obs in self.obstacles if hasattr(obs, 'index')], default=0) + 1
        self.text_counter = max([obs.index for obs in self.obstacles if isinstance(obs, TextObstacle)], default=0) + 1
        self.parameter_counter = max([obs.index for obs in self.obstacles if isinstance(obs, ParameterObstacle)], default=0) + 1
    
    def create_arc(self, start_obj: BaseObstacle, end_obj: BaseObstacle, control_point: Optional[Tuple[float, float]] = None):
        """创建弧线"""
        try:
            start_center = start_obj.get_center()
            end_center = end_obj.get_center()
            
            arc_id = self.canvas.create_line(
                start_center[0], start_center[1],
                end_center[0], end_center[1],
                smooth=True, width=1, dash=(5, 3), tags='arc'
            )
            
            arc_data = (arc_id, start_obj, end_obj, control_point)
            self.arc_list.append(arc_data)
            self.settings.add_arc(arc_data)
            
            return arc_id
        except Exception as e:
            logging.error(f"创建弧线失败: {e}")
            return None
    
    def delete_arc(self, arc_id: int):
        """删除弧线"""
        try:
            self.canvas.delete(arc_id)
            # 从列表中移除
            self.arc_list = [(arc, start, end, control) for arc, start, end, control in self.arc_list if arc != arc_id]
            self.settings.arc_list = self.arc_list.copy()
        except Exception as e:
            logging.error(f"删除弧线失败: {e}")
    
    def clear_all_arcs(self):
        """清除所有弧线"""
        self.canvas.delete('arc')
        self.arc_list.clear()
        self.settings.clear_arcs()
    
    def _update_arcs(self):
        """更新所有弧线"""
        for arc_id, start_obj, end_obj, control_point in self.arc_list:
            try:
                start_center = start_obj.get_center()
                end_center = end_obj.get_center()
                
                self.canvas.coords(arc_id, start_center[0], start_center[1], end_center[0], end_center[1])
            except Exception as e:
                logging.error(f"更新弧线失败: {e}")
    
    def get_obstacle_by_id(self, obstacle_id: int) -> Optional[BaseObstacle]:
        """根据ID获取障碍物"""
        for obstacle in self.obstacles:
            if obstacle.id == obstacle_id:
                return obstacle
        return None
    
    def get_obstacle_by_tag(self, tag: str) -> Optional[BaseObstacle]:
        """根据标签获取障碍物"""
        for obstacle in self.obstacles:
            if obstacle.tag == tag:
                return obstacle
        return None
    
    def set_obstacle_visibility(self, obstacle: BaseObstacle, visible: bool):
        """设置障碍物可见性"""
        try:
            state = 'normal' if visible else 'hidden'
            self.canvas.itemconfig(obstacle.tag, state=state)
            obstacle.ui_state = visible
        except Exception as e:
            logging.error(f"设置障碍物可见性失败: {e}")
    
    def bring_to_front(self, obstacle: BaseObstacle):
        """将障碍物置于顶层"""
        try:
            self.canvas.lift(obstacle.tag)
        except Exception as e:
            logging.error(f"将障碍物置于顶层失败: {e}")
    
    def send_to_back(self, obstacle: BaseObstacle):
        """将障碍物置于底层"""
        try:
            self.canvas.lower(obstacle.tag)
            self.canvas.lower("watermark")
        except Exception as e:
            logging.error(f"将障碍物置于底层失败: {e}")
    
    def duplicate_obstacle(self, obstacle: BaseObstacle) -> Optional[BaseObstacle]:
        """复制障碍物"""
        try:
            # 创建新的障碍物，位置稍微偏移
            new_obstacle = obstacle.duplicate()
            if new_obstacle:
                new_obstacle.current_x += 20
                new_obstacle.current_y += 20
                new_obstacle.update_position()
                self.obstacles.append(new_obstacle)
                self.settings.add_obstacle_instance(new_obstacle)
                return new_obstacle
        except Exception as e:
            logging.error(f"复制障碍物失败: {e}")
        return None
