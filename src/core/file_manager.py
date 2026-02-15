"""
文件管理器
统一处理所有文件操作，包括保存、加载、自动保存等
"""

import json
import logging
import time
import os
from pathlib import Path
from typing import Dict, Any, Optional
from tkinter import filedialog, messagebox

from ..config import Settings, BACKUP_DIR, AUTO_BACKUP_DIR, FILE_TYPES


class FileManager:
    """文件管理器"""
    
    def __init__(self, settings: Settings):
        self.settings = settings
        self.current_file_path: Optional[str] = None
        self.last_save_time = 0
        self.auto_save_interval = 300  # 5分钟自动保存
    
    def save_project(self, file_path: Optional[str] = None, auto_save: bool = False) -> bool:
        """保存项目"""
        try:
            if not file_path and not auto_save:
                file_path = filedialog.asksaveasfilename(
                    title='保存路线图数据',
                    filetypes=FILE_TYPES['json'],
                    initialdir=str(BACKUP_DIR)
                )
            
            if not file_path:
                return False
            
            # 确保文件扩展名正确
            if not file_path.endswith('.json'):
                file_path += '.json'
            
            # 准备保存数据
            save_data = self._prepare_save_data()
            
            # 写入文件
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(save_data, f, ensure_ascii=False, indent=2)
            
            self.current_file_path = file_path
            self.last_save_time = time.time()
            
            if not auto_save:
                messagebox.showinfo("保存成功", f"项目已保存至: {file_path}")
            
            logging.info(f"项目保存成功: {file_path}")
            return True
            
        except Exception as e:
            error_msg = f"保存项目失败: {e}"
            logging.error(error_msg)
            if not auto_save:
                messagebox.showerror("保存失败", error_msg)
            return False
    
    def load_project(self, file_path: Optional[str] = None) -> bool:
        """加载项目"""
        try:
            if not file_path:
                file_path = filedialog.askopenfilename(
                    title='加载路线图数据',
                    filetypes=FILE_TYPES['json'],
                    initialdir=str(BACKUP_DIR)
                )
            
            if not file_path:
                return False
            
            # 读取文件
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # 应用加载的数据
            self._apply_loaded_data(data)
            
            self.current_file_path = file_path
            messagebox.showinfo("加载成功", f"项目已从文件加载: {file_path}")
            
            logging.info(f"项目加载成功: {file_path}")
            return True
            
        except Exception as e:
            error_msg = f"加载项目失败: {e}"
            logging.error(error_msg)
            messagebox.showerror("加载失败", error_msg)
            return False
    
    def auto_save(self) -> bool:
        """自动保存"""
        try:
            # 检查是否需要自动保存
            if time.time() - self.last_save_time < self.auto_save_interval:
                return True
            
            # 生成自动保存文件名
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            auto_save_path = AUTO_BACKUP_DIR / f"auto_save_{timestamp}.json"
            
            return self.save_project(str(auto_save_path), auto_save=True)
            
        except Exception as e:
            logging.error(f"自动保存失败: {e}")
            return False
    
    def load_last_session(self) -> bool:
        """加载上次会话"""
        try:
            # 查找最新的自动保存文件
            auto_save_files = list(AUTO_BACKUP_DIR.glob("auto_save_*.json"))
            if not auto_save_files:
                return False
            
            # 获取最新的文件
            latest_file = max(auto_save_files, key=lambda f: f.stat().st_mtime)
            
            # 检查文件是否太旧（超过1小时）
            if time.time() - latest_file.stat().st_mtime > 3600:
                return False
            
            # 询问用户是否恢复
            result = messagebox.askyesno(
                "恢复会话",
                f"发现上次的自动保存文件，是否恢复？\n文件: {latest_file.name}"
            )
            
            if result:
                return self.load_project(str(latest_file))
            
            return False
            
        except Exception as e:
            logging.error(f"加载上次会话失败: {e}")
            return False
    
    def save_current_session(self) -> bool:
        """保存当前会话"""
        if self.current_file_path:
            return self.save_project(self.current_file_path)
        else:
            return self.auto_save()
    
    def export_image(self, include_info: bool = True) -> bool:
        """导出图片"""
        try:
            from PIL import ImageGrab
            
            # 获取保存路径
            timestamp = time.strftime("%Y%m%d-%H%M%S")
            default_name = f"路线设计_{timestamp}.jpg"
            
            file_path = filedialog.asksaveasfilename(
                title='导出图片',
                filetypes=FILE_TYPES['image'],
                initialdir=str(BACKUP_DIR),
                initialfile=default_name
            )
            
            if not file_path:
                return False
            
            # 确保文件扩展名正确
            if not file_path.endswith(('.jpg', '.png')):
                file_path += '.jpg'
            
            # 截取画布区域
            canvas = self.settings.canvas_manager.get_canvas()
            if not canvas:
                return False
            
            # 获取画布位置和大小
            x = canvas.winfo_rootx()
            y = canvas.winfo_rooty()
            width = canvas.winfo_width()
            height = canvas.winfo_height()
            
            # 如果需要包含信息面板，调整截图区域
            if include_info:
                # 这里需要根据实际UI布局调整
                pass
            
            # 截取屏幕
            screenshot = ImageGrab.grab(bbox=(x, y, x + width, y + height))
            screenshot.save(file_path)
            
            messagebox.showinfo("导出成功", f"图片已导出至: {file_path}")
            logging.info(f"图片导出成功: {file_path}")
            return True
            
        except Exception as e:
            error_msg = f"导出图片失败: {e}"
            logging.error(error_msg)
            messagebox.showerror("导出失败", error_msg)
            return False
    
    def _prepare_save_data(self) -> Dict[str, Any]:
        """准备保存数据"""
        return {
            'version': '2.0.0',
            'canvas_width': self.settings.canvas_width,
            'canvas_height': self.settings.canvas_height,
            'obstacle_length': self.settings.obstacle_length,
            'font_size': self.settings.font_size,
            'remove_size': self.settings.remove_size,
            'operation_mode': self.settings.operation_mode,
            'show_grid': self.settings.show_grid,
            'show_aux_info': self.settings.show_aux_info,
            'show_arc': self.settings.show_arc,
            'show_watermark': self.settings.show_watermark,
            'background_image': self.settings.background_image,
            'event_info': self.settings.event_info,
            'lines': self.settings.lines,
            'arc_list': self.settings.arc_list,
            'obstacles': self._serialize_obstacles(),
            'save_time': time.time(),
        }
    
    def _apply_loaded_data(self, data: Dict[str, Any]):
        """应用加载的数据"""
        try:
            # 更新基本设置
            self.settings.canvas_width = data.get('canvas_width', 900)
            self.settings.canvas_height = data.get('canvas_height', 600)
            self.settings.obstacle_length = data.get('obstacle_length', 4.0)
            self.settings.font_size = data.get('font_size', 1)
            self.settings.remove_size = data.get('remove_size', 1)
            self.settings.operation_mode = data.get('operation_mode', 0)
            self.settings.show_grid = data.get('show_grid', False)
            self.settings.show_aux_info = data.get('show_aux_info', True)
            self.settings.show_arc = data.get('show_arc', False)
            self.settings.show_watermark = data.get('show_watermark', True)
            self.settings.background_image = data.get('background_image')
            self.settings.event_info = data.get('event_info', {})
            self.settings.lines = data.get('lines', [])
            self.settings.arc_list = data.get('arc_list', [])
            
            # 更新画布尺寸
            if hasattr(self.settings, 'canvas_manager'):
                self.settings.canvas_manager.update_canvas_size(
                    self.settings.canvas_width,
                    self.settings.canvas_height
                )
            
            # 加载障碍物
            self._deserialize_obstacles(data.get('obstacles', {}))
            
        except Exception as e:
            logging.error(f"应用加载数据失败: {e}")
            raise
    
    def _serialize_obstacles(self) -> Dict[str, Any]:
        """序列化障碍物数据"""
        obstacles_data = {}
        for obstacle in self.settings.obstacle_instances:
            if obstacle.ui_state:
                obstacle_data = obstacle.save()
                obstacles_data.update(obstacle_data)
        return obstacles_data
    
    def _deserialize_obstacles(self, obstacles_data: Dict[str, Any]):
        """反序列化障碍物数据"""
        try:
            # 清空现有障碍物
            self.settings.obstacle_instances.clear()
            
            # 如果obstacles_data是字典，转换为列表
            if isinstance(obstacles_data, dict):
                obstacles_list = [obstacles_data]
            elif isinstance(obstacles_data, list):
                obstacles_list = obstacles_data
            else:
                return
            
            for obstacle_data in obstacles_list:
                try:
                    obstacle_type = obstacle_data.get('type', '')
                    
                    if obstacle_type == 'image':
                        from ..obstacles.image_obstacle import ImageObstacle
                        obstacle = ImageObstacle(
                            self.canvas_manager.canvas,
                            obstacle_data.get('obstacle_type', ''),
                            obstacle_data.get('x', 0),
                            obstacle_data.get('y', 0),
                            obstacle_data.get('angle', 0),
                            obstacle_data.get('scale', 1.0),
                            self.settings
                        )
                        obstacle.load(obstacle_data)
                        self.settings.obstacle_instances.append(obstacle)
                        
                    elif obstacle_type == 'text':
                        from ..obstacles.text_obstacle import TextObstacle
                        obstacle = TextObstacle(
                            self.canvas_manager.canvas,
                            obstacle_data.get('text', ''),
                            obstacle_data.get('x', 0),
                            obstacle_data.get('y', 0),
                            obstacle_data.get('angle', 0),
                            obstacle_data.get('scale', 1.0),
                            self.settings
                        )
                        obstacle.load(obstacle_data)
                        self.settings.obstacle_instances.append(obstacle)
                        
                    elif obstacle_type == 'parameter':
                        from ..obstacles.parameter_obstacle import ParameterObstacle
                        obstacle = ParameterObstacle(
                            self.canvas_manager.canvas,
                            obstacle_data.get('parameter_type', ''),
                            obstacle_data.get('x', 0),
                            obstacle_data.get('y', 0),
                            obstacle_data.get('angle', 0),
                            obstacle_data.get('scale', 1.0),
                            self.settings
                        )
                        obstacle.load(obstacle_data)
                        self.settings.obstacle_instances.append(obstacle)
                        
                except Exception as e:
                    logging.error(f"反序列化障碍物失败: {e}")
                    continue
                    
        except Exception as e:
            logging.error(f"反序列化障碍物数据失败: {e}")
    
    def get_current_file_path(self) -> Optional[str]:
        """获取当前文件路径"""
        return self.current_file_path
    
    def has_unsaved_changes(self) -> bool:
        """检查是否有未保存的更改"""
        # 这里可以实现更复杂的更改检测逻辑
        return time.time() - self.last_save_time > 0
    
    def clear_auto_save_files(self, max_age_hours: int = 24):
        """清理旧的自动保存文件"""
        try:
            current_time = time.time()
            max_age_seconds = max_age_hours * 3600
            
            for file_path in AUTO_BACKUP_DIR.glob("auto_save_*.json"):
                if current_time - file_path.stat().st_mtime > max_age_seconds:
                    file_path.unlink()
                    logging.info(f"删除旧的自动保存文件: {file_path}")
                    
        except Exception as e:
            logging.error(f"清理自动保存文件失败: {e}")
    
    def get_file_info(self) -> Dict[str, Any]:
        """获取文件信息"""
        return {
            'current_file': self.current_file_path,
            'last_save_time': self.last_save_time,
            'auto_save_interval': self.auto_save_interval,
            'has_unsaved_changes': self.has_unsaved_changes(),
        }
