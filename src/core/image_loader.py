"""
图像加载模块
负责加载和预处理障碍物图像
"""
import os
from typing import Callable, Any
from PIL import Image, ImageTk


class ImageLoader:
    """图像加载器类"""

    # 默认图像路径
    DEFAULT_PATHS = {
        'one': 'img/one.png',
        'oxer': 'img/oxer.png',
        'liverpool': 'img/liverpool3.png',
        'force': 'img/force.png',
        'compass': 'img/compass.png',
        'water_barrier': 'img/water_barrier.png',
        'brick_wall': 'img/brick_wall.png',
        'line': 'img/line.png',
        'gate': 'img/gate.png',
        'icon': 'img/ic.png',
        'circular': 'img/circular.png',
    }

    def __init__(self, bar_length: float = 4.0):
        """
        初始化图像加载器
        :param bar_length: 障碍杆长度（米）
        """
        self._bar_length = bar_length
        self._temp_dir = './temp_img'
        self._ensure_temp_dir()

    def _ensure_temp_dir(self):
        """确保临时目录存在"""
        if not os.path.exists(self._temp_dir):
            os.mkdir(self._temp_dir)

    @property
    def bar_length(self) -> float:
        """获取障碍杆长度"""
        return self._bar_length

    @bar_length.setter
    def bar_length(self, value: float):
        """设置障碍杆长度"""
        self._bar_length = float(value)

    def adjust_image_size(self, image_path: str) -> str:
        """
        调整图像尺寸
        :param image_path: 图像路径
        :return: 调整后的图像路径
        """
        image = Image.open(image_path)
        w, h = image.size
        h = int(self._bar_length * 10)
        image = image.resize((w, h))

        file_name = os.path.basename(image_path)
        name = file_name.replace('.', '-adj.')
        file_path = os.path.join(self._temp_dir, name)
        image.save(file_path)

        return file_path

    def load_image(self, path: str) -> str:
        """
        加载图像并调整尺寸
        :param path: 图像路径
        :return: 调整后的图像路径
        """
        return self.adjust_image_size(path)

    def load_image_tk(self, path: str) -> ImageTk.PhotoImage:
        """
        加载图像为 PhotoImage 对象
        :param path: 图像路径
        :return: PhotoImage 对象
        """
        return ImageTk.PhotoImage(Image.open(path))

    def get_path(self, key: str) -> str:
        """
        获取默认图像路径
        :param key: 图像键名
        :return: 图像路径
        """
        return self.DEFAULT_PATHS.get(key, '')


# 全局图像加载器实例
_image_loader: ImageLoader = None


def get_image_loader() -> ImageLoader:
    """获取全局图像加载器"""
    global _image_loader
    if _image_loader is None:
        _image_loader = ImageLoader()
    return _image_loader


def set_bar_length(length: float):
    """设置全局障碍杆长度"""
    loader = get_image_loader()
    loader.bar_length = length


def get_bar_length() -> float:
    """获取全局障碍杆长度"""
    return get_image_loader().bar_length


def load_image(path: str) -> str:
    """加载并调整图像尺寸"""
    return get_image_loader().load_image(path)


def load_image_tk(path: str) -> ImageTk.PhotoImage:
    """加载图像为 PhotoImage"""
    return get_image_loader().load_image_tk(path)


def get_image_path(key: str) -> str:
    """获取默认图像路径"""
    return get_image_loader().get_path(key)
