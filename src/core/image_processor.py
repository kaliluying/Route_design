"""
图像处理模块
封装所有图像处理功能，替代 Tools.py
"""

import os
import sys
from typing import Optional
from PIL import Image, ImageOps

# 项目根目录
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _get_img_path(filename):
    """获取 img 目录下的文件完整路径（相对于项目根目录）"""
    return os.path.join(_PROJECT_ROOT, "img", filename)


class ImageProcessor:
    """图像处理器单例"""

    _instance: Optional["ImageProcessor"] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self._direction_image = "img/direction2.png"
            self._one_path = "img/one.png"
            self._liverpool_path = "img/liverpool3.png"

    # ===== 路径获取方法 =====

    def get_one_path(self) -> str:
        """获取单横木路径"""
        return self._one_path

    def get_live_path(self) -> str:
        """获取利物浦路径"""
        return self._liverpool_path

    @property
    def direction_image(self) -> str:
        """获取方向图像路径"""
        return self._direction_image

    # ===== 基础图像操作 =====

    def merge(self, m: int, m1: int = 0, state: int = 1) -> str:
        """
        合并图片（创建组合障碍）
        :param m: 第一个障碍间距
        :param m1: 第二个障碍间距（可选）
        :param state: 状态
        :return: 处理后的图像路径
        """
        img_obj = Image.open(self._one_path)
        img_obj2 = Image.open(self._one_path)
        w, h = img_obj.size
        result = Image.new(img_obj.mode, (m + m1 + 10, h))
        result.paste(img_obj, box=(0, 0))

        if m1:
            a = 10
        else:
            a = 5
        result.paste(img_obj2, box=(m + m1 - a, 0))

        if m1:
            image3 = Image.open(self._one_path)
            result.paste(image3, box=(m - 5, 0))
            result.save(_get_img_path("com_2.png"))
            com_image = _get_img_path("com_2.png")
            return self.start_direction(self.expand(com_image, state))
        com_image = _get_img_path("com.png")
        result.save(com_image)
        return self.start_direction(self.expand(com_image, state))

    def expand(self, path: str, state: int = 1) -> str:
        """
        图片扩展（使图片变为正方形）
        :param path: 图像路径
        :param state: 状态
        :return: 处理后的图像路径
        """
        img = Image.open(path)
        w, h = img.size
        l = r = t = b = 0

        if w < h:
            var_ex = h - w
            l = var_ex // 2
            r = var_ex - l
        elif state and w > h:
            var_ex = w - h
            t = var_ex // 2
            b = var_ex - t

        left_pad = l
        top_pad = t
        right_pad = r
        bottom_pad = b

        padding = (left_pad, top_pad, right_pad, bottom_pad)
        img2 = ImageOps.expand(img, padding, fill=(236, 236, 236, 0))
        directory = os.path.dirname(path)
        file_name = os.path.basename(path)
        image_name = file_name.replace(".", "-exp.")
        image_path = directory + "/" + image_name
        img2.save(image_path)
        return image_path

    def start_direction(self, image_path: str) -> str:
        """
        添加行进方向标识
        :param image_path: 图像路径
        :return: 处理后的图像路径
        """
        img1 = Image.open(image_path)
        w, h = img1.size
        img2 = Image.open(self._direction_image)
        w1, h1 = img2.size
        img2 = img2.resize((w, h1))
        r, g, b, alpha = img2.split()
        img1.paste(img2, (0, h // 2 - 5), alpha)
        directory = os.path.dirname(image_path)
        file_name = os.path.basename(image_path)
        image_name = file_name.replace(".", "-dir.")
        image_path = directory + "/" + image_name
        img1.save(image_path)
        return image_path

    # ===== 组合障碍 =====

    def combination(self, m1: int, m2: int, m3: int) -> str:
        """创建三杆组合障碍"""
        img_obj = Image.open(self._one_path)
        img_obj2 = Image.open(self._one_path)
        img_obj3 = Image.open(self._one_path)
        img_obj4 = Image.open(self._one_path)

        result = Image.new(img_obj.mode, (m1 + m2 + m3 + 20, 40))
        result.paste(img_obj, box=(0, 0))
        result.paste(img_obj2, box=(m1 + 5, 0))
        result.paste(img_obj3, box=(m1 + m2 + 10, 0))
        result.paste(img_obj4, box=(m1 + m2 + m3 + 15, 0))
        result.save(_get_img_path("com_3.png"))
        com_image = _get_img_path("com_3.png")
        return self.start_direction(self.expand(com_image))

    def merge_ab(self, state: int, m1: int = 0, m2: int = 0) -> str:
        """创建AB/ABC组合障碍"""
        if state == 1:
            path = self.start_direction(self.expand(self._one_path))
        if state == 2:
            path = self.start_direction(self.merge(10))
        img_obj = Image.open(path)
        img_obj2 = Image.open(path)
        var = 45
        if m2:
            var = 50
        result = Image.new(img_obj.mode, (m1 + m2 + var, 40))
        result.paste(img_obj, box=(0, 0))
        result.paste(img_obj2, box=(m1 + 5, 0))
        if m2:
            image3 = Image.open(path)
            result.paste(image3, box=(m1 + m2 + 10, 0))
            result.save(_get_img_path("com_abc.png"))
            com_image = _get_img_path("com_abc.png")
            return com_image
        com_image = _get_img_path("com_ab.png")
        result.save(com_image)
        return com_image

    def oxer_obs_ab(
        self,
        stare_a: str,
        state_b: str,
        state_c: str = "0",
        a: int = 0,
        b: int = 0,
        c: int = 0,
        a_b: int = 30,
        b_c: int = 0,
    ) -> str:
        """创建双横木AB组合"""
        a_img = self._one_exp_dir_path
        b_img = self._one_exp_dir_path
        c_img = self._one_exp_dir_path

        if stare_a == "1":
            a_img = self.merge(a + 5, state=0)
        if state_b == "1":
            b_img = self.merge(b + 5, state=0)
        if state_c == "1":
            c_img = self.merge(c + 5, state=0)

        var = 45
        if state_c:
            var = 50
        img_obj = Image.open(a_img)
        img_obj2 = Image.open(b_img)
        result = Image.new(img_obj.mode, (a + b + c + a_b + b_c + var, 40))
        result.paste(img_obj, box=(0, 0))
        result.paste(img_obj2, box=(a_b + 5, 0))
        if state_c:
            image3 = Image.open(c_img)
            result.paste(image3, box=(a_b + b_c + 10, 0))
            result.save(_get_img_path("oxer_obs_abc.png"))
            return _get_img_path("oxer_obs_abc.png")
        result.save(_get_img_path("oxer_obs_ab.png"))
        return _get_img_path("oxer_obs_ab.png")

    def oxer_obs_abc(
        self, a: int = 0, b: int = 0, c: int = 0, a_b: int = 30, b_c: int = 0
    ) -> str:
        """创建ABC障碍"""
        a_img = self.merge(a if a else 0, state=0)
        img_obj = Image.open(a_img)
        b_img = self.merge(b if b else 0, state=0)
        img_obj2 = Image.open(b_img)
        c_img = self.merge(c if c else 0, state=0)
        image3 = Image.open(c_img)
        result = Image.new(img_obj.mode, (a + b + c + a_b + b_c + 50, 40))
        result.paste(img_obj, box=(0, 0))
        result.paste(img_obj2, box=(a + a_b + (10 if a else 5), 0))
        result.paste(
            image3, box=(a + b + a_b + b_c + (10 if a else 5) + (10 if b else 5), 0)
        )
        result.save(_get_img_path("obs_abc.png"))
        return _get_img_path("obs_abc.png")

    def obs_ab(self, a: int = 0, b: int = 0, a_b: int = 30) -> str:
        """创建AB障碍"""
        a_img = self.merge(a if a else 0, state=0)
        img_obj = Image.open(a_img)
        b_img = self.merge(b if b else 0, state=0)
        img_obj2 = Image.open(b_img)
        result = Image.new(img_obj.mode, (a + b + a_b + 45, 40))
        result.paste(img_obj, box=(0, 0))
        result.paste(img_obj2, box=(a + a_b + (10 if a else 5), 0))
        result.save(_get_img_path("obs_ab.png"))
        return _get_img_path("obs_ab.png")

    # ===== 水障 =====

    def water_wh(
        self, w: int, h: int, water_barrier_image: str = "img/water_barrier.png"
    ) -> str:
        """水障调整"""
        img = Image.open(water_barrier_image)
        img = img.resize((w, h))
        img.save(_get_img_path("water_wh.png"))
        return self.start_direction(self.expand(_get_img_path("water_wh.png")))

    # ===== 利物浦 =====

    def live_two_tool(self, path: str = "img/liverpool3.png") -> str:
        """利物浦单横木变双横木"""
        img = Image.open(path)
        img2 = Image.open("img/one.png")
        w, h = img.size
        result = Image.new(img.mode, (w, h))
        result.paste(img, box=(0, 0))
        result.paste(img2, box=(0, 0))
        result.paste(img2, box=(w - 5, 0))
        result.save(_get_img_path("live_two.png"))
        return self.start_direction(self.expand(_get_img_path("live_two.png")))

    def live_one_tool(self, path: str = "img/liverpool3.png") -> str:
        """利物浦单横木"""
        img = Image.open(path)
        img2 = Image.open("img/one.png")
        w, h = img.size
        result = Image.new(img.mode, (w, h))
        result.paste(img, box=(0, 0))
        result.paste(img2, box=(int(w / 2 - 1), 0))
        result.save(_get_img_path("live_one.png"))
        return self.start_direction(self.expand(_get_img_path("live_one.png")))

    def live_edit(self, w: int, h: int, get_live_state: callable) -> str:
        """利物浦编辑"""
        img = Image.open("img/liverpool3.png")
        img = img.resize((w, h))
        img.save(_get_img_path("live_wh.png"))
        live_id = get_live_state()
        if live_id == "1" or live_id == 1:
            return self.live_two_tool(_get_img_path("live_wh.png"))
        elif live_id == 0 or live_id == "0":
            return self.live_one_tool(_get_img_path("live_wh.png"))

    # ===== 缓存的路径 =====

    @property
    def _one_exp_dir_path(self) -> str:
        """单横木带方向路径（缓存）"""
        return self.start_direction(self.expand(self._one_path))


# 单例实例
_image_processor = None


def get_image_processor() -> ImageProcessor:
    """获取图像处理器单例"""
    global _image_processor
    if _image_processor is None:
        _image_processor = ImageProcessor()
    return _image_processor


# ===== 便捷函数（向后兼容）=====


# 检测字符串中是否是数字
def is_number(s: str) -> bool:
    """检测字符串是否为数字"""
    try:
        float(s)
        return True
    except ValueError:
        pass
    try:
        import unicodedata

        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass
    return False


# 便捷访问
_merge = lambda m, m1=0, state=1: get_image_processor().merge(m, m1, state)
_expand = lambda path, state=1: get_image_processor().expand(path, state)
_start_direction = lambda path: get_image_processor().start_direction(path)
_merge_ab = lambda state, m1=0, m2=0: get_image_processor().merge_ab(state, m1, m2)
_oxer_obs_abc = lambda a=0, b=0, c=0, a_b=30, b_c=0: get_image_processor().oxer_obs_abc(
    a, b, c, a_b, b_c
)
_obs_ab = lambda a=0, b=0, a_b=30: get_image_processor().obs_ab(a, b, a_b)
_water_wh = lambda w, h, path="img/water_barrier.png": get_image_processor().water_wh(
    w, h, path
)
_live_two_tool = lambda path="img/liverpool3.png": get_image_processor().live_two_tool(
    path
)
_live_one_tool = lambda path="img/liverpool3.png": get_image_processor().live_one_tool(
    path
)
