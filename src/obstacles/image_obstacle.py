"""
图像障碍物类
继承自BaseObstacle，实现图像类型的障碍物
"""

import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os
from typing import Dict, Any, Optional, Tuple

from .base_obstacle import BaseObstacle
from ..config import Settings, IMAGE_PATHS, OBSTACLE_CONFIG


class ImageObstacle(BaseObstacle):
    """图像障碍物类"""

    def __init__(self, canvas: tk.Canvas, obstacle_type: str, x: float = 0, y: float = 0,
                 angle: float = 0, scale: float = 1.0, settings: Optional[Settings] = None):
        """
        初始化图像障碍物
        
        Args:
            canvas: 画布对象
            obstacle_type: 障碍物类型
            x: x坐标
            y: y坐标
            angle: 旋转角度
            scale: 缩放比例
            settings: 设置对象
        """
        self.obstacle_type = obstacle_type
        self.image_path = IMAGE_PATHS.get(obstacle_type, "")
        self.original_image = None
        self.photo_image = None
        self.image_id = None

        super().__init__(canvas, x, y, angle, scale, settings)

    def _setup_obstacle(self) -> None:
        """设置障碍物"""
        if not self.image_path or not os.path.exists(self.image_path):
            # 如果图像文件不存在，创建一个默认的矩形
            self._create_default_shape()
            return

        try:
            # 加载图像
            self.original_image = Image.open(self.image_path)

            # 调整图像大小
            default_size = OBSTACLE_CONFIG.get('default_size', 50)
            self.original_image = self.original_image.resize(
                (default_size, default_size), Image.Resampling.LANCZOS
            )

            # 创建PhotoImage对象
            self.photo_image = ImageTk.PhotoImage(self.original_image)

            # 在画布上创建图像
            self.image_id = self.canvas.create_image(
                self.x, self.y,
                image=self.photo_image,
                tags=self.tag
            )

        except Exception as e:
            print(f"加载图像失败 {self.image_path}: {e}")
            self._create_default_shape()

    def _create_default_shape(self) -> None:
        """创建默认形状（当图像加载失败时）"""
        default_size = OBSTACLE_CONFIG.get('default_size', 50)
        half_size = default_size // 2

        self.image_id = self.canvas.create_rectangle(
            self.x - half_size, self.y - half_size,
            self.x + half_size, self.y + half_size,
            fill="lightblue", outline="blue", width=2,
            tags=self.tag
        )

        # 添加文本标签
        text_id = self.canvas.create_text(
            self.x, self.y,
            text=self.obstacle_type,
            fill="black",
            font=("Arial", 8),
            tags=self.tag
        )

    def _apply_rotation(self) -> None:
        """应用旋转"""
        if self.image_id:
            # 对于图像，我们需要重新创建旋转后的图像
            if self.original_image and self.photo_image:
                # 旋转原始图像
                rotated_image = self.original_image.rotate(
                    -self.angle, expand=True, resample=Image.Resampling.BICUBIC
                )
                self.photo_image = ImageTk.PhotoImage(rotated_image)

                # 更新画布上的图像
                self.canvas.itemconfig(self.image_id, image=self.photo_image)

    def _apply_scale(self) -> None:
        """应用缩放"""
        if self.image_id and self.original_image:
            # 计算新的尺寸
            original_size = self.original_image.size[0]
            new_size = int(original_size * self.scale)

            # 缩放图像
            scaled_image = self.original_image.resize(
                (new_size, new_size), Image.Resampling.LANCZOS
            )

            # 应用旋转
            if self.angle != 0:
                scaled_image = scaled_image.rotate(
                    -self.angle, expand=True, resample=Image.Resampling.BICUBIC
                )

            self.photo_image = ImageTk.PhotoImage(scaled_image)
            self.canvas.itemconfig(self.image_id, image=self.photo_image)

    def get_bounds(self) -> Tuple[float, float, float, float]:
        """获取边界"""
        if self.image_id:
            bbox = self.canvas.bbox(self.image_id)
            if bbox:
                return bbox
        return self.x - 25, self.y - 25, self.x + 25, self.y + 25

    def save(self) -> Dict[str, Any]:
        """保存障碍物数据"""
        data = super().save()
        data.update({
            'type': 'image',
            'obstacle_type': self.obstacle_type,
            'image_path': self.image_path
        })
        return data

    def load(self, data: Dict[str, Any]) -> None:
        """加载障碍物数据"""
        super().load(data)
        self.obstacle_type = data.get('obstacle_type', '')
        self.image_path = data.get('image_path', '')

        # 重新设置障碍物
        self._setup_obstacle()
        self._apply_rotation()
        self._apply_scale()

    def duplicate(self) -> 'ImageObstacle':
        """复制障碍物"""
        new_obstacle = ImageObstacle(
            self.canvas, self.obstacle_type,
            self.x + 20, self.y + 20,  # 稍微偏移位置
            self.angle, self.scale, self.settings
        )
        return new_obstacle
