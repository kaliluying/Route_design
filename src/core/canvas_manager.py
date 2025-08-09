"""
画布管理器
负责画布的所有操作，包括绘制、事件处理等
"""

import math
import logging
from typing import List, Tuple, Optional, Dict, Any
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

from ..config import Settings, UI_CONFIG, OPERATION_MODES, IS_MACOS


class CanvasManager:
    """画布管理器"""
    
    def __init__(self, window, settings: Settings):
        self.window = window
        self.settings = settings
        self.canvas = None
        self.image_data = {}
        self.current_line = None
        self.route_click = []
        self.click_num = 1
        self.px = 0
        self.remove_px = {}
        self.last_draw = 0
        self.end = [0]
        
        self._create_canvas()
        self._setup_canvas_events()
        self._create_auxiliary_elements()
    
    def _create_canvas(self):
        """创建画布"""
        ui_config = self.settings.get_ui_config()
        self.canvas = tk.Canvas(
            self.window,
            width=ui_config['width'],
            height=ui_config['height'],
            highlightthickness=0
        )
        self.canvas.place(x=UI_CONFIG['canvas_x'], y=UI_CONFIG['canvas_y'])
        self.canvas.image_data = self.image_data
    
    def _setup_canvas_events(self):
        """设置画布事件"""
        self.canvas.bind('<Button-1>', self._on_mouse_down)
        self.canvas.bind('<B1-Motion>', self._on_mouse_move)
        self.canvas.bind('<ButtonRelease-1>', self._on_mouse_up)
        self.canvas.bind('<Motion>', self._on_mouse_motion)
        self.canvas.bind('<MouseWheel>', self._on_mouse_wheel)
    
    def _create_auxiliary_elements(self):
        """创建辅助元素"""
        # 创建实际画布边界
        self.canvas.create_rectangle(
            30, 120, 
            self.settings.canvas_width + 30, 
            self.settings.canvas_height + 120,
            state='disabled', 
            tags=('不框选', '实际画布')
        )
        
        # 创建尺寸显示
        self._create_size_display()
        
        # 创建比例尺
        self._create_scale_display()
        
        # 创建路线长度显示
        self._create_route_length_display()
        
        # 创建坐标显示
        self._create_coordinate_display()
        
        # 创建水印
        self._create_watermark()
        
        # 创建标题
        self._create_title()
    
    def _create_size_display(self):
        """创建尺寸显示"""
        w = self.settings.canvas_width / 10
        h = self.settings.canvas_height / 10
        
        self.canvas.create_text(
            self.settings.canvas_width - 40, 130,
            text=f"长：{w}m",
            tags=('辅助信息', '不框选', '长')
        )
        
        self.canvas.create_text(
            self.settings.canvas_width - 40, 150,
            text=f"宽：{h}m",
            tags=('辅助信息', '不框选', '宽')
        )
    
    def _create_scale_display(self):
        """创建比例尺"""
        self.canvas.create_text(60, 130, text="5m", tags=('辅助信息', '不框选'))
        self.canvas.create_line(35, 135, 35, 140, tags=('辅助信息', '不框选'))
        self.canvas.create_line(85, 135, 85, 140, tags=('辅助信息', '不框选'))
        self.canvas.create_line(35, 140, 85, 140, tags=('辅助信息', '不框选'))
    
    def _create_route_length_display(self):
        """创建路线长度显示"""
        self.canvas.create_text(
            self.settings.canvas_width - 40, 100,
            text=f"{self.px / 10}m",
            tags=('实时路线', '不框选', '辅助信息')
        )
    
    def _create_coordinate_display(self):
        """创建坐标显示"""
        # 鼠标坐标
        self.canvas.create_text(
            self.settings.canvas_width - 10, self.settings.canvas_height + 130,
            text='x:', tags=('辅助信息', '不框选', '鼠标x')
        )
        self.canvas.create_text(
            self.settings.canvas_width - 10, self.settings.canvas_height + 140,
            text='y:', tags=('辅助信息', '不框选', '鼠标y')
        )
        
        # 障碍坐标
        self.canvas.create_text(
            35, self.settings.canvas_height + 130,
            text="x:", tags=('辅助信息', '不框选', '障碍x')
        )
        self.canvas.create_text(
            35, self.settings.canvas_height + 140,
            text="y:", tags=('辅助信息', '不框选', '障碍y')
        )
    
    def _create_watermark(self):
        """创建水印"""
        if self.settings.show_watermark:
            font_size = 0.16 if IS_MACOS else 0.1
            self.canvas.create_text(
                (self.settings.canvas_width + 35) / 2,
                (self.settings.canvas_height + 220) / 2,
                text="DEMO",
                font=("行楷", int(self.settings.canvas_width * font_size), "bold", "italic"),
                fill="#e4e4dc",
                tags=("watermark", '不框选'),
                state='disabled'
            )
    
    def _create_title(self):
        """创建标题"""
        # 比赛名称
        self.canvas.create_text(
            (self.settings.canvas_width + 40) / 2, 20,
            text='比赛名称',
            font=("微软雅黑", 18),
            tags=('比赛名称', '不框选')
        )
        
        # 级别赛制
        self.canvas.create_text(
            (self.settings.canvas_width + 40) / 2, 40,
            text='级别赛制',
            font=("微软雅黑", 14),
            tags=('级别赛制', '不框选')
        )
    
    def _on_mouse_down(self, event):
        """鼠标按下事件"""
        if self.settings.operation_mode == OPERATION_MODES['DRAW']:
            self._start_drawing(event)
        elif self.settings.operation_mode == OPERATION_MODES['DRAG']:
            self._start_dragging(event)
    
    def _on_mouse_move(self, event):
        """鼠标移动事件"""
        if self.settings.operation_mode == OPERATION_MODES['DRAW']:
            self._continue_drawing(event)
        elif self.settings.operation_mode == OPERATION_MODES['DRAG']:
            self._continue_dragging(event)
    
    def _on_mouse_up(self, event):
        """鼠标释放事件"""
        if self.settings.operation_mode == OPERATION_MODES['DRAW']:
            self._finish_drawing(event)
        elif self.settings.operation_mode == OPERATION_MODES['DRAG']:
            self._finish_dragging(event)
    
    def _on_mouse_motion(self, event):
        """鼠标移动事件（用于显示坐标）"""
        x = event.x / 10 - 3
        y = event.y / 10 - 12
        self.canvas.itemconfig('鼠标x', text=f'x:{x:.2f}')
        self.canvas.itemconfig('鼠标y', text=f'y:{y:.2f}')
    
    def _on_mouse_wheel(self, event):
        """鼠标滚轮事件"""
        # 处理自定义障碍的缩放
        pass
    
    def _start_drawing(self, event):
        """开始绘制"""
        self.current_line = [(event.x, event.y)]
        self.route_click.append((event.x, event.y))
    
    def _continue_drawing(self, event):
        """继续绘制"""
        if self.current_line:
            self.current_line.append((event.x, event.y))
            
            # 创建线段
            line_id = self.canvas.create_line(
                self.current_line[-2][0], self.current_line[-2][1],
                event.x, event.y,
                fill='#000000',
                width=self.settings.font_size,
                tags=("line", '不框选'),
                smooth=True
            )
            
            # 计算长度
            x1, y1 = self.current_line[-2]
            x2, y2 = event.x, event.y
            distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / 10
            self.px += distance
            
            # 更新显示
            self.canvas.itemconfig('实时路线', text=f"{self.px / 10:.2f}m")
            
            # 记录撤销信息
            self.remove_px[line_id] = distance
            self.end.append(line_id)
    
    def _finish_drawing(self, event):
        """完成绘制"""
        if self.current_line:
            self.settings.add_line({
                'coords': self.current_line,
                'length': self.px / 10
            })
            self.current_line = None
    
    def _start_dragging(self, event):
        """开始拖拽"""
        # 处理障碍物拖拽
        pass
    
    def _continue_dragging(self, event):
        """继续拖拽"""
        # 处理障碍物拖拽
        pass
    
    def _finish_dragging(self, event):
        """完成拖拽"""
        # 处理障碍物拖拽
        pass
    
    def clear_lines(self):
        """清除所有路线"""
        self.canvas.delete("line")
        self.px = 0
        self.remove_px.clear()
        self.end = [0]
        self.settings.clear_lines()
        self.canvas.itemconfig('实时路线', text="0.00m")
    
    def update_canvas_size(self, width: int, height: int):
        """更新画布尺寸"""
        self.settings.update_canvas_size(width, height)
        
        # 重新配置画布
        ui_config = self.settings.get_ui_config()
        self.canvas.config(width=ui_config['width'], height=ui_config['height'])
        
        # 更新实际画布边界
        self.canvas.coords('实际画布', 30, 120, width + 30, height + 120)
        
        # 更新辅助元素位置
        self._update_auxiliary_elements(width, height)
    
    def _update_auxiliary_elements(self, width: int, height: int):
        """更新辅助元素位置"""
        # 更新尺寸显示
        w, h = width / 10, height / 10
        self.canvas.itemconfig('长', text=f"长：{w}m")
        self.canvas.itemconfig('宽', text=f"宽：{h}m")
        self.canvas.coords('长', width - 40, 130)
        self.canvas.coords('宽', width - 40, 150)
        
        # 更新路线长度显示
        self.canvas.coords('实时路线', width - 40, 100)
        
        # 更新坐标显示
        self.canvas.coords('鼠标x', width - 10, height + 130)
        self.canvas.coords('鼠标y', width - 10, height + 140)
        self.canvas.coords('障碍x', 35, height + 130)
        self.canvas.coords('障碍y', 35, height + 140)
        
        # 更新标题位置
        self.canvas.coords('比赛名称', (width + 40) / 2, 20)
        self.canvas.coords('级别赛制', (width + 40) / 2, 40)
    
    def set_background_image(self, image_path: str):
        """设置背景图片"""
        try:
            img = Image.open(image_path)
            img = img.resize((self.settings.canvas_width, self.settings.canvas_height))
            photo = ImageTk.PhotoImage(img)
            
            # 删除旧的背景
            self.canvas.delete('bg')
            
            # 创建新的背景
            self.canvas.create_image(
                15, 50, image=photo,
                anchor='nw', tags=('不框选', 'bg')
            )
            
            # 保存引用防止垃圾回收
            self.canvas.background_image = photo
            self.settings.set_background_image(image_path)
            
        except Exception as e:
            logging.error(f"设置背景图片失败: {e}")
    
    def remove_background_image(self):
        """移除背景图片"""
        self.canvas.delete('bg')
        self.settings.set_background_image(None)
    
    def toggle_grid(self):
        """切换网格显示"""
        if self.settings.show_grid:
            self.canvas.delete('grid')
            self.settings.toggle_grid()
        else:
            self._create_grid()
            self.settings.toggle_grid()
    
    def _create_grid(self):
        """创建网格"""
        range_x = (self.settings.canvas_width + 15) // 100
        range_y = (self.settings.canvas_height + 70) // 100
        
        # 垂直线
        for i in range(range_x):
            x = 30 + i * 100
            self.canvas.create_line(
                x, 50, x, self.settings.canvas_height + 50,
                dash=(5, 3), tags=('grid', '不框选'), smooth=True
            )
        
        # 水平线
        for i in range(range_y):
            y = 50 + i * 100
            self.canvas.create_line(
                30, y, self.settings.canvas_width + 15, y,
                dash=(5, 3), tags=('grid', '不框选'), smooth=True
            )
    
    def toggle_aux_info(self):
        """切换辅助信息显示"""
        state = 'hidden' if self.settings.show_aux_info else 'normal'
        self.canvas.itemconfig('辅助信息', state=state)
        self.settings.toggle_aux_info()
    
    def toggle_watermark(self):
        """切换水印显示"""
        if self.settings.show_watermark:
            self.canvas.delete('watermark')
            self.settings.toggle_watermark()
        else:
            self._create_watermark()
            self.settings.toggle_watermark()
    
    def get_canvas(self):
        """获取画布对象"""
        return self.canvas
    
    def get_image_data(self):
        """获取图片数据"""
        return self.image_data
