"""
图像处理工具类
提供图像处理相关的功能
"""

import os
from PIL import Image, ImageTk, ImageEnhance, ImageFilter
from typing import Tuple, Optional, List
import tkinter as tk


class ImageProcessor:
    """图像处理工具类"""
    
    @staticmethod
    def load_image(image_path: str, target_size: Optional[Tuple[int, int]] = None) -> Optional[Image.Image]:
        """
        加载图像
        
        Args:
            image_path: 图像文件路径
            target_size: 目标尺寸 (width, height)
            
        Returns:
            加载的图像对象，如果失败返回None
        """
        try:
            if not os.path.exists(image_path):
                return None
            
            image = Image.open(image_path)
            
            if target_size:
                image = image.resize(target_size, Image.Resampling.LANCZOS)
            
            return image
        except Exception as e:
            print(f"加载图像失败 {image_path}: {e}")
            return None
    
    @staticmethod
    def create_photo_image(image: Image.Image) -> Optional[ImageTk.PhotoImage]:
        """
        创建PhotoImage对象
        
        Args:
            image: PIL图像对象
            
        Returns:
            PhotoImage对象，如果失败返回None
        """
        try:
            return ImageTk.PhotoImage(image)
        except Exception as e:
            print(f"创建PhotoImage失败: {e}")
            return None
    
    @staticmethod
    def resize_image(image: Image.Image, size: Tuple[int, int], 
                    keep_aspect_ratio: bool = True) -> Image.Image:
        """
        调整图像大小
        
        Args:
            image: 原始图像
            size: 目标尺寸 (width, height)
            keep_aspect_ratio: 是否保持宽高比
            
        Returns:
            调整后的图像
        """
        if keep_aspect_ratio:
            # 计算缩放比例
            width, height = image.size
            target_width, target_height = size
            
            width_ratio = target_width / width
            height_ratio = target_height / height
            ratio = min(width_ratio, height_ratio)
            
            new_size = (int(width * ratio), int(height * ratio))
        else:
            new_size = size
        
        return image.resize(new_size, Image.Resampling.LANCZOS)
    
    @staticmethod
    def rotate_image(image: Image.Image, angle: float, 
                    expand: bool = True) -> Image.Image:
        """
        旋转图像
        
        Args:
            image: 原始图像
            angle: 旋转角度（度）
            expand: 是否扩展画布以适应旋转后的图像
            
        Returns:
            旋转后的图像
        """
        return image.rotate(angle, expand=expand, resample=Image.Resampling.BICUBIC)
    
    @staticmethod
    def apply_filter(image: Image.Image, filter_type: str) -> Image.Image:
        """
        应用滤镜
        
        Args:
            image: 原始图像
            filter_type: 滤镜类型 ('blur', 'sharpen', 'edge_enhance', 'emboss')
            
        Returns:
            应用滤镜后的图像
        """
        if filter_type == 'blur':
            return image.filter(ImageFilter.BLUR)
        elif filter_type == 'sharpen':
            return image.filter(ImageFilter.SHARPEN)
        elif filter_type == 'edge_enhance':
            return image.filter(ImageFilter.EDGE_ENHANCE)
        elif filter_type == 'emboss':
            return image.filter(ImageFilter.EMBOSS)
        else:
            return image
    
    @staticmethod
    def adjust_brightness(image: Image.Image, factor: float) -> Image.Image:
        """
        调整亮度
        
        Args:
            image: 原始图像
            factor: 亮度因子 (0.0-2.0, 1.0为原始亮度)
            
        Returns:
            调整后的图像
        """
        enhancer = ImageEnhance.Brightness(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def adjust_contrast(image: Image.Image, factor: float) -> Image.Image:
        """
        调整对比度
        
        Args:
            image: 原始图像
            factor: 对比度因子 (0.0-2.0, 1.0为原始对比度)
            
        Returns:
            调整后的图像
        """
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)
    
    @staticmethod
    def convert_to_grayscale(image: Image.Image) -> Image.Image:
        """
        转换为灰度图像
        
        Args:
            image: 原始图像
            
        Returns:
            灰度图像
        """
        return image.convert('L')
    
    @staticmethod
    def create_thumbnail(image: Image.Image, size: Tuple[int, int]) -> Image.Image:
        """
        创建缩略图
        
        Args:
            image: 原始图像
            size: 缩略图尺寸 (width, height)
            
        Returns:
            缩略图
        """
        return image.copy().thumbnail(size, Image.Resampling.LANCZOS)
    
    @staticmethod
    def get_image_info(image_path: str) -> Optional[dict]:
        """
        获取图像信息
        
        Args:
            image_path: 图像文件路径
            
        Returns:
            图像信息字典，包含尺寸、格式、模式等
        """
        try:
            with Image.open(image_path) as image:
                return {
                    'size': image.size,
                    'format': image.format,
                    'mode': image.mode,
                    'filename': image.filename
                }
        except Exception as e:
            print(f"获取图像信息失败 {image_path}: {e}")
            return None
    
    @staticmethod
    def is_valid_image_file(file_path: str) -> bool:
        """
        检查是否为有效的图像文件
        
        Args:
            file_path: 文件路径
            
        Returns:
            是否为有效图像文件
        """
        try:
            with Image.open(file_path) as image:
                image.verify()
            return True
        except Exception:
            return False
    
    @staticmethod
    def get_supported_formats() -> List[str]:
        """
        获取支持的图像格式
        
        Returns:
            支持的图像格式列表
        """
        return ['PNG', 'JPEG', 'JPG', 'GIF', 'BMP', 'TIFF', 'ICO']
