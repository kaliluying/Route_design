"""
障碍物创建工厂模块
将 main.py 中的障碍物创建函数分离到这里
"""
from functools import partial
from PIL import Image

# 导入外部模块（需要在使用时传入canvas）
_canvas = None
_index_img = 0
_index_txt = 0


def init_factory(canvas, get_index_img, get_index_txt, drag_func, var_cir):
    """
    初始化工厂
    :param canvas: tkinter canvas 对象
    :param get_index_img: 获取 index_img 的函数
    :param get_index_txt: 获取 index_txt 的函数
    :param drag_func: drag 函数
    :param var_cir: 圆的半径变量
    """
    global _canvas
    _canvas = canvas


def set_index_img(value):
    global _index_img
    _index_img = value


def set_index_txt(value):
    global _index_txt
    _index_txt = value


# ===== 障碍号相关 =====

def insert(var_id, e_id, CreateTxt, drag_func):
    """障碍号确认"""
    global _index_txt
    _index_txt += 1
    CreateTxt(_canvas, _index_txt).create(var_id.get())
    e_id.delete(0, 'end')
    drag_func()


# ===== 参数相关 =====

def parameter(var_parameter, e_parameter, CreateParameter, drag_func):
    """障碍参数确认"""
    global _index_txt
    _index_txt += 1
    CreateParameter(_canvas, _index_txt).create(var_parameter.get())
    e_parameter.delete(0, 'end')
    drag_func()


def hidden(par_index, canvas, par_state):
    """隐藏障碍参数"""
    if par_index:
        canvas.itemconfig('parameter', state='hidden')
        par_state.config(text='显示')
        return 0
    else:
        canvas.itemconfig('parameter', state='normal')
        par_state.config(text='隐藏')
        return 1


# ===== 单个障碍物创建 =====

def create_monorail(CreateImg, expand, get_one_path, start_direction):
    """创建单横木"""
    global _index_img
    _index_img += 1
    image_path = expand(get_one_path())
    image_path = start_direction(image_path)
    CreateImg(_canvas, _index_img, image_path, obstacle='monorail').create()


def create_oxer(CreateImg, merge, start_direction):
    """创建双横木"""
    global _index_img
    _index_img += 1
    image_path = merge(10)
    image_path = start_direction(image_path)
    CreateImg(_canvas, _index_img, image_path, obstacle='oxer').create()


def create_tirail(CreateImg, merge):
    """创建三横木"""
    global _index_img
    _index_img += 1
    image_path = merge(10, 10)
    CreateImg(_canvas, _index_img, image_path, obstacle='tirail').create()


def create_combination_ab(CreateImg, merge_ab):
    """创建AB组合障碍"""
    global _index_img
    _index_img += 1
    image_path = merge_ab(state=1, m1=30)
    CreateImg(_canvas, _index_img, image_path, obstacle="combination_ab").create()


def create_combination_abc(CreateImg, merge_ab):
    """创建ABC组合障碍"""
    global _index_img
    _index_img += 1
    image_path = merge_ab(state=1, m1=30, m2=30)
    CreateImg(_canvas, _index_img, image_path, obstacle="combination_abc").create()


def create_live(CreateImg, live_one_tool):
    """创建利物浦障碍"""
    global _index_img
    _index_img += 1
    image_path = live_one_tool()
    CreateImg(_canvas, _index_img, image_path, obstacle='live').create()


def create_force(CreateImg, force_image):
    """创建强制通过点"""
    global _index_img
    _index_img += 1
    CreateImg(_canvas, _index_img, force_image).create()


def create_compass(CreateImg, expand, compass_image):
    """创建指北针"""
    global _index_img
    _index_img += 1
    image_path = expand(compass_image)
    CreateImg(_canvas, _index_img, image_path).create()


def create_water_barrier(CreateImg, expand, water_barrier_image, start_direction):
    """创建水障"""
    global _index_img
    _index_img += 1
    image_path = expand(water_barrier_image)
    image_path = start_direction(image_path)
    CreateImg(_canvas, _index_img, image_path, obstacle='water').create()


def create_brick_wall(CreateImg, expand, brick_wall_image):
    """创建砖墙"""
    global _index_img
    _index_img += 1
    image_path = expand(brick_wall_image)
    CreateImg(_canvas, _index_img, image_path).create()


def create_line(CreateImg, expand, line_image, start_direction):
    """创建起/终点线"""
    global _index_img
    _index_img += 1
    image_path = expand(line_image)
    image_path = start_direction(image_path)
    CreateImg(_canvas, _index_img, image_path).create()


def create_gate(CreateImg, expand, gate_image):
    """创建进出口"""
    global _index_img
    _index_img += 1
    image_path = expand(gate_image)
    CreateImg(_canvas, _index_img, image_path).create()


def create_circular(CreateImg, circular_image, var_cir):
    """创建圆"""
    global _index_img
    _index_img += 1
    cir = int(var_cir.get()) * 10
    img = Image.open(circular_image)
    img = img.resize((cir, cir))
    img.save('./img/cir.png')
    cir_path = './img/cir.png'
    CreateImg(_canvas, _index_img, cir_path).create()


def get_index_img_value():
    """获取当前 index_img 值"""
    return _index_img


def get_index_txt_value():
    """获取当前 index_txt 值"""
    return _index_txt
