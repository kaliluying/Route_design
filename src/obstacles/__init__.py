"""
障碍物模块
包含所有障碍物的基类和具体实现
"""

from .base_obstacle import BaseObstacle
from .image_obstacle import ImageObstacle
from .text_obstacle import TextObstacle
from .parameter_obstacle import ParameterObstacle

__all__ = [
    'BaseObstacle',
    'ImageObstacle',
    'TextObstacle',
    'ParameterObstacle'
]
