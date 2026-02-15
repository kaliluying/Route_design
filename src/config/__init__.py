"""
配置模块
包含应用程序的所有配置信息
"""

from .settings import Settings
from .constants import *

__all__ = [
    'Settings', 
    'APP_NAME', 
    'APP_VERSION', 
    'IS_WINDOWS', 
    'IS_MACOS',
    'UI_CONFIG', 
    'OBSTACLE_CONFIG',
    'IMAGE_PATHS',
    'OBSTACLE_TYPES',
    'EVENT_INFO_FIELDS',
    'OPERATION_MODES',
    'FILE_TYPES'
]
