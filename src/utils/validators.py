"""
验证工具类
提供数据验证相关的功能
"""

import re
import os
from typing import Any, List, Optional, Tuple
from pathlib import Path


class Validators:
    """验证工具类"""
    
    @staticmethod
    def is_valid_filename(filename: str) -> bool:
        """
        验证文件名是否有效
        
        Args:
            filename: 文件名
            
        Returns:
            文件名是否有效
        """
        if not filename or len(filename) > 255:
            return False
        
        # 检查是否包含非法字符
        invalid_chars = '<>:"/\\|?*'
        return not any(char in filename for char in invalid_chars)
    
    @staticmethod
    def is_valid_file_path(file_path: str) -> bool:
        """
        验证文件路径是否有效
        
        Args:
            file_path: 文件路径
            
        Returns:
            文件路径是否有效
        """
        try:
            path = Path(file_path)
            return path.is_file() or path.parent.exists()
        except Exception:
            return False
    
    @staticmethod
    def is_valid_directory_path(dir_path: str) -> bool:
        """
        验证目录路径是否有效
        
        Args:
            dir_path: 目录路径
            
        Returns:
            目录路径是否有效
        """
        try:
            path = Path(dir_path)
            return path.is_dir() or path.parent.exists()
        except Exception:
            return False
    
    @staticmethod
    def is_valid_number(value: Any, min_val: Optional[float] = None, 
                       max_val: Optional[float] = None) -> bool:
        """
        验证数值是否有效
        
        Args:
            value: 要验证的值
            min_val: 最小值
            max_val: 最大值
            
        Returns:
            数值是否有效
        """
        try:
            num = float(value)
            if min_val is not None and num < min_val:
                return False
            if max_val is not None and num > max_val:
                return False
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_integer(value: Any, min_val: Optional[int] = None, 
                        max_val: Optional[int] = None) -> bool:
        """
        验证整数是否有效
        
        Args:
            value: 要验证的值
            min_val: 最小值
            max_val: 最大值
            
        Returns:
            整数是否有效
        """
        try:
            num = int(value)
            if min_val is not None and num < min_val:
                return False
            if max_val is not None and num > max_val:
                return False
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_angle(angle: float) -> bool:
        """
        验证角度是否有效
        
        Args:
            angle: 角度值
            
        Returns:
            角度是否有效
        """
        return Validators.is_valid_number(angle, 0, 360)
    
    @staticmethod
    def is_valid_scale(scale: float) -> bool:
        """
        验证缩放比例是否有效
        
        Args:
            scale: 缩放比例
            
        Returns:
            缩放比例是否有效
        """
        return Validators.is_valid_number(scale, 0.1, 10.0)
    
    @staticmethod
    def is_valid_coordinate(x: float, y: float, 
                           canvas_width: float, canvas_height: float) -> bool:
        """
        验证坐标是否在画布范围内
        
        Args:
            x: x坐标
            y: y坐标
            canvas_width: 画布宽度
            canvas_height: 画布高度
            
        Returns:
            坐标是否有效
        """
        return (0 <= x <= canvas_width and 0 <= y <= canvas_height)
    
    @staticmethod
    def is_valid_color(color: str) -> bool:
        """
        验证颜色值是否有效
        
        Args:
            color: 颜色值（可以是颜色名称或十六进制值）
            
        Returns:
            颜色值是否有效
        """
        if not color:
            return False
        
        # 检查是否为有效的颜色名称
        valid_color_names = {
            'red', 'green', 'blue', 'yellow', 'cyan', 'magenta', 'black', 'white',
            'gray', 'grey', 'orange', 'purple', 'pink', 'brown', 'lightblue',
            'lightgreen', 'lightgray', 'lightgrey', 'darkblue', 'darkgreen',
            'darkgray', 'darkgrey', 'transparent'
        }
        
        if color.lower() in valid_color_names:
            return True
        
        # 检查是否为有效的十六进制颜色值
        hex_pattern = r'^#[0-9A-Fa-f]{6}$'
        if re.match(hex_pattern, color):
            return True
        
        # 检查是否为RGB格式
        rgb_pattern = r'^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$'
        if re.match(rgb_pattern, color):
            return True
        
        return False
    
    @staticmethod
    def is_valid_font_family(font_family: str) -> bool:
        """
        验证字体族是否有效
        
        Args:
            font_family: 字体族名称
            
        Returns:
            字体族是否有效
        """
        if not font_family:
            return False
        
        # 常见的有效字体族
        valid_fonts = {
            'Arial', 'Helvetica', 'Times', 'Times New Roman', 'Courier', 'Courier New',
            'Verdana', 'Georgia', 'Palatino', 'Garamond', 'Bookman', 'Comic Sans MS',
            'Trebuchet MS', 'Arial Black', 'Impact', 'Lucida Console', 'Tahoma',
            'Geneva', 'Lucida Sans Unicode', 'Franklin Gothic Medium', 'Arial Narrow'
        }
        
        return font_family in valid_fonts
    
    @staticmethod
    def is_valid_font_size(font_size: int) -> bool:
        """
        验证字体大小是否有效
        
        Args:
            font_size: 字体大小
            
        Returns:
            字体大小是否有效
        """
        return Validators.is_valid_integer(font_size, 6, 72)
    
    @staticmethod
    def is_valid_operation_mode(mode: str) -> bool:
        """
        验证操作模式是否有效
        
        Args:
            mode: 操作模式
            
        Returns:
            操作模式是否有效
        """
        valid_modes = {'drag', 'draw', 'rotate', 'erase'}
        return mode in valid_modes
    
    @staticmethod
    def is_valid_obstacle_type(obstacle_type: str) -> bool:
        """
        验证障碍物类型是否有效
        
        Args:
            obstacle_type: 障碍物类型
            
        Returns:
            障碍物类型是否有效
        """
        if not obstacle_type:
            return False
        
        # 这里可以根据实际的障碍物类型列表进行验证
        # 暂时返回True，实际使用时应该检查具体的类型列表
        return True
    
    @staticmethod
    def is_valid_file_extension(filename: str, allowed_extensions: List[str]) -> bool:
        """
        验证文件扩展名是否在允许的列表中
        
        Args:
            filename: 文件名
            allowed_extensions: 允许的扩展名列表
            
        Returns:
            文件扩展名是否有效
        """
        if not filename:
            return False
        
        file_ext = Path(filename).suffix.lower()
        return file_ext in [ext.lower() for ext in allowed_extensions]
    
    @staticmethod
    def sanitize_filename(filename: str) -> str:
        """
        清理文件名，移除或替换非法字符
        
        Args:
            filename: 原始文件名
            
        Returns:
            清理后的文件名
        """
        if not filename:
            return "untitled"
        
        # 替换非法字符
        invalid_chars = '<>:"/\\|?*'
        for char in invalid_chars:
            filename = filename.replace(char, '_')
        
        # 移除前后空格
        filename = filename.strip()
        
        # 如果文件名为空，使用默认名称
        if not filename:
            filename = "untitled"
        
        # 限制长度
        if len(filename) > 255:
            filename = filename[:255]
        
        return filename
    
    @staticmethod
    def validate_settings(settings: dict) -> Tuple[bool, List[str]]:
        """
        验证设置字典的有效性
        
        Args:
            settings: 设置字典
            
        Returns:
            (是否有效, 错误信息列表)
        """
        errors = []
        
        # 验证画布尺寸
        if 'canvas_width' in settings:
            if not Validators.is_valid_integer(settings['canvas_width'], 100, 5000):
                errors.append("画布宽度必须在100-5000之间")
        
        if 'canvas_height' in settings:
            if not Validators.is_valid_integer(settings['canvas_height'], 100, 5000):
                errors.append("画布高度必须在100-5000之间")
        
        # 验证操作模式
        if 'operation_mode' in settings:
            if not Validators.is_valid_operation_mode(settings['operation_mode']):
                errors.append("无效的操作模式")
        
        # 验证障碍物设置
        if 'obstacle_length' in settings:
            if not Validators.is_valid_number(settings['obstacle_length'], 1, 1000):
                errors.append("障碍物长度必须在1-1000之间")
        
        if 'obstacle_size' in settings:
            if not Validators.is_valid_number(settings['obstacle_size'], 0.1, 100):
                errors.append("障碍物大小必须在0.1-100之间")
        
        # 验证自动保存设置
        if 'auto_save_interval' in settings:
            if not Validators.is_valid_integer(settings['auto_save_interval'], 10, 3600):
                errors.append("自动保存间隔必须在10-3600秒之间")
        
        return len(errors) == 0, errors
