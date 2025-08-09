"""
数学工具类
提供数学计算相关的功能
"""

import math
from typing import Tuple, List, Optional
import numpy as np


class MathUtils:
    """数学工具类"""
    
    @staticmethod
    def distance(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """
        计算两点之间的距离
        
        Args:
            point1: 第一个点 (x, y)
            point2: 第二个点 (x, y)
            
        Returns:
            两点之间的距离
        """
        x1, y1 = point1
        x2, y2 = point2
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    
    @staticmethod
    def angle_between_points(point1: Tuple[float, float], point2: Tuple[float, float]) -> float:
        """
        计算两点之间的角度
        
        Args:
            point1: 第一个点 (x, y)
            point2: 第二个点 (x, y)
            
        Returns:
            角度（弧度）
        """
        x1, y1 = point1
        x2, y2 = point2
        return math.atan2(y2 - y1, x2 - x1)
    
    @staticmethod
    def rotate_point(point: Tuple[float, float], center: Tuple[float, float], 
                    angle: float) -> Tuple[float, float]:
        """
        旋转点
        
        Args:
            point: 要旋转的点 (x, y)
            center: 旋转中心 (x, y)
            angle: 旋转角度（弧度）
            
        Returns:
            旋转后的点坐标
        """
        x, y = point
        cx, cy = center
        
        # 平移到原点
        x -= cx
        y -= cy
        
        # 旋转
        cos_a = math.cos(angle)
        sin_a = math.sin(angle)
        new_x = x * cos_a - y * sin_a
        new_y = x * sin_a + y * cos_a
        
        # 平移回原位置
        new_x += cx
        new_y += cy
        
        return (new_x, new_y)
    
    @staticmethod
    def scale_point(point: Tuple[float, float], center: Tuple[float, float], 
                   scale_x: float, scale_y: float) -> Tuple[float, float]:
        """
        缩放点
        
        Args:
            point: 要缩放的点 (x, y)
            center: 缩放中心 (x, y)
            scale_x: X轴缩放比例
            scale_y: Y轴缩放比例
            
        Returns:
            缩放后的点坐标
        """
        x, y = point
        cx, cy = center
        
        # 平移到原点
        x -= cx
        y -= cy
        
        # 缩放
        new_x = x * scale_x
        new_y = y * scale_y
        
        # 平移回原位置
        new_x += cx
        new_y += cy
        
        return (new_x, new_y)
    
    @staticmethod
    def point_in_rectangle(point: Tuple[float, float], 
                          rect: Tuple[float, float, float, float]) -> bool:
        """
        判断点是否在矩形内
        
        Args:
            point: 点坐标 (x, y)
            rect: 矩形 (x1, y1, x2, y2)
            
        Returns:
            点是否在矩形内
        """
        x, y = point
        x1, y1, x2, y2 = rect
        return x1 <= x <= x2 and y1 <= y <= y2
    
    @staticmethod
    def point_in_circle(point: Tuple[float, float], center: Tuple[float, float], 
                       radius: float) -> bool:
        """
        判断点是否在圆内
        
        Args:
            point: 点坐标 (x, y)
            center: 圆心坐标 (x, y)
            radius: 半径
            
        Returns:
            点是否在圆内
        """
        return MathUtils.distance(point, center) <= radius
    
    @staticmethod
    def line_intersection(line1: Tuple[Tuple[float, float], Tuple[float, float]], 
                         line2: Tuple[Tuple[float, float], Tuple[float, float]]) -> Optional[Tuple[float, float]]:
        """
        计算两条直线的交点
        
        Args:
            line1: 第一条直线 ((x1, y1), (x2, y2))
            line2: 第二条直线 ((x3, y3), (x4, y4))
            
        Returns:
            交点坐标，如果平行则返回None
        """
        (x1, y1), (x2, y2) = line1
        (x3, y3), (x4, y4) = line2
        
        denominator = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        
        if abs(denominator) < 1e-10:  # 平行线
            return None
        
        t = ((x1 - x3) * (y3 - y4) - (y1 - y3) * (x3 - x4)) / denominator
        
        intersection_x = x1 + t * (x2 - x1)
        intersection_y = y1 + t * (y2 - y1)
        
        return (intersection_x, intersection_y)
    
    @staticmethod
    def polygon_area(points: List[Tuple[float, float]]) -> float:
        """
        计算多边形面积（使用鞋带公式）
        
        Args:
            points: 多边形顶点列表 [(x1, y1), (x2, y2), ...]
            
        Returns:
            多边形面积
        """
        if len(points) < 3:
            return 0.0
        
        area = 0.0
        n = len(points)
        
        for i in range(n):
            j = (i + 1) % n
            area += points[i][0] * points[j][1]
            area -= points[j][0] * points[i][1]
        
        return abs(area) / 2.0
    
    @staticmethod
    def polygon_center(points: List[Tuple[float, float]]) -> Tuple[float, float]:
        """
        计算多边形重心
        
        Args:
            points: 多边形顶点列表 [(x1, y1), (x2, y2), ...]
            
        Returns:
            重心坐标
        """
        if not points:
            return (0.0, 0.0)
        
        x_sum = sum(point[0] for point in points)
        y_sum = sum(point[1] for point in points)
        n = len(points)
        
        return (x_sum / n, y_sum / n)
    
    @staticmethod
    def bezier_curve(points: List[Tuple[float, float]], t: float) -> Tuple[float, float]:
        """
        计算贝塞尔曲线上的点
        
        Args:
            points: 控制点列表 [(x1, y1), (x2, y2), ...]
            t: 参数值 (0-1)
            
        Returns:
            曲线上的点坐标
        """
        if len(points) == 1:
            return points[0]
        
        new_points = []
        for i in range(len(points) - 1):
            x = (1 - t) * points[i][0] + t * points[i + 1][0]
            y = (1 - t) * points[i][1] + t * points[i + 1][1]
            new_points.append((x, y))
        
        return MathUtils.bezier_curve(new_points, t)
    
    @staticmethod
    def bezier_curve_points(points: List[Tuple[float, float]], 
                           num_points: int = 100) -> List[Tuple[float, float]]:
        """
        生成贝塞尔曲线上的点列表
        
        Args:
            points: 控制点列表 [(x1, y1), (x2, y2), ...]
            num_points: 生成的点数量
            
        Returns:
            曲线上的点列表
        """
        curve_points = []
        for i in range(num_points):
            t = i / (num_points - 1)
            curve_points.append(MathUtils.bezier_curve(points, t))
        
        return curve_points
    
    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        """
        将值限制在指定范围内
        
        Args:
            value: 要限制的值
            min_val: 最小值
            max_val: 最大值
            
        Returns:
            限制后的值
        """
        return max(min_val, min(value, max_val))
    
    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        """
        线性插值
        
        Args:
            a: 起始值
            b: 结束值
            t: 插值参数 (0-1)
            
        Returns:
            插值结果
        """
        return a + (b - a) * t
    
    @staticmethod
    def smoothstep(edge0: float, edge1: float, x: float) -> float:
        """
        平滑步进函数
        
        Args:
            edge0: 下边界
            edge1: 上边界
            x: 输入值
            
        Returns:
            平滑步进结果
        """
        t = MathUtils.clamp((x - edge0) / (edge1 - edge0), 0.0, 1.0)
        return t * t * (3.0 - 2.0 * t)
    
    @staticmethod
    def degrees_to_radians(degrees: float) -> float:
        """
        角度转弧度
        
        Args:
            degrees: 角度
            
        Returns:
            弧度
        """
        return degrees * math.pi / 180.0
    
    @staticmethod
    def radians_to_degrees(radians: float) -> float:
        """
        弧度转角度
        
        Args:
            radians: 弧度
            
        Returns:
            角度
        """
        return radians * 180.0 / math.pi
    
    @staticmethod
    def normalize_angle(angle: float) -> float:
        """
        标准化角度到 [0, 2π) 范围
        
        Args:
            angle: 角度（弧度）
            
        Returns:
            标准化后的角度
        """
        while angle < 0:
            angle += 2 * math.pi
        while angle >= 2 * math.pi:
            angle -= 2 * math.pi
        return angle
