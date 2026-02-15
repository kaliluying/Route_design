"""
障碍物创建工厂模块
将 main.py 中的障碍物创建函数分离到这里

使用方式:
    from src.core.obstacle_factory import create_monorail, create_oxer, etc.
    # 直接调用，会自动获取所需的依赖
"""
from PIL import Image


def _get_dependencies():
    """获取所需依赖"""
    from Common import (
        canvas, state, drag,
        expand, start_direction, get_one_path, merge, merge_ab,
        live_one_tool, force_image, compass_image, water_barrier_image,
        brick_wall_image, line_image, gate_image, circular_image,
        CreateImg
    )
    return {
        'canvas': canvas,
        'state': state,
        'drag': drag,
        'expand': expand,
        'start_direction': start_direction,
        'get_one_path': get_one_path,
        'merge': merge,
        'merge_ab': merge_ab,
        'live_one_tool': live_one_tool,
        'force_image': force_image,
        'compass_image': compass_image,
        'water_barrier_image': water_barrier_image,
        'brick_wall_image': brick_wall_image,
        'line_image': line_image,
        'gate_image': gate_image,
        'circular_image': circular_image,
        'CreateImg': CreateImg,
    }


# ===== 单个障碍物创建 =====

def create_monorail():
    """创建单横木"""
    dep = _get_dependencies()
    image_path = dep['expand'](dep['get_one_path']())
    image_path = dep['start_direction'](image_path)
    dep['CreateImg'](dep['canvas'], dep['state'].index_img, image_path, obstacle='monorail').create()
    dep['state'].index_img += 1
    dep['drag']()


def create_oxer():
    """创建双横木"""
    dep = _get_dependencies()
    image_path = dep['merge'](10)
    image_path = dep['start_direction'](image_path)
    dep['CreateImg'](dep['canvas'], dep['state'].index_img, image_path, obstacle="oxer").create()
    dep['state'].index_img += 1
    dep['drag']()


def create_tirail():
    """创建三横木"""
    dep = _get_dependencies()
    image_path = dep['merge'](10, 10)
    dep['CreateImg'](dep['canvas'], dep['state'].index_img, image_path, obstacle="tirail").create()
    dep['state'].index_img += 1
    dep['drag']()


def create_combination_ab():
    """创建AB组合障碍"""
    dep = _get_dependencies()
    image_path = dep['merge_ab'](state=1, m1=30)
    dep['CreateImg'](dep['canvas'], dep['state'].index_img, image_path, obstacle="combination_ab").create()
    dep['state'].index_img += 1
    dep['drag']()


def create_combination_abc():
    """创建ABC组合障碍"""
    dep = _get_dependencies()
    image_path = dep['merge_ab'](state=1, m1=30, m2=30)
    dep['CreateImg'](dep['canvas'], dep['state'].index_img, image_path, obstacle="combination_abc").create()
    dep['state'].index_img += 1
    dep['drag']()


def create_live():
    """创建利物浦障碍"""
    dep = _get_dependencies()
    image_path = dep['live_one_tool']()
    dep['CreateImg'](dep['canvas'], dep['state'].index_img, image_path, obstacle='live').create()
    dep['state'].index_img += 1
    dep['drag']()


def create_force():
    """创建强制通过点"""
    dep = _get_dependencies()
    dep['CreateImg'](dep['canvas'], dep['state'].index_img, dep['force_image']).create()
    dep['state'].index_img += 1
    dep['drag']()


def create_compass():
    """创建指北针"""
    dep = _get_dependencies()
    image_path = dep['expand'](dep['compass_image'])
    dep['CreateImg'](dep['canvas'], dep['state'].index_img, image_path).create()
    dep['state'].index_img += 1
    dep['drag']()


def create_water_barrier():
    """创建水障"""
    dep = _get_dependencies()
    image_path = dep['expand'](dep['water_barrier_image'])
    image_path = dep['start_direction'](image_path)
    dep['CreateImg'](dep['canvas'], dep['state'].index_img, image_path, obstacle='water').create()
    dep['state'].index_img += 1
    dep['drag']()


def create_brick_wall():
    """创建砖墙"""
    dep = _get_dependencies()
    image_path = dep['expand'](dep['brick_wall_image'])
    dep['CreateImg'](dep['canvas'], dep['state'].index_img, image_path).create()
    dep['state'].index_img += 1
    dep['drag']()


def create_line():
    """创建起/终点线"""
    dep = _get_dependencies()
    image_path = dep['expand'](dep['line_image'])
    image_path = dep['start_direction'](image_path)
    dep['CreateImg'](dep['canvas'], dep['state'].index_img, image_path).create()
    dep['state'].index_img += 1
    dep['drag']()


def create_gate():
    """创建进出口"""
    dep = _get_dependencies()
    image_path = dep['expand'](dep['gate_image'])
    dep['CreateImg'](dep['canvas'], dep['state'].index_img, image_path).create()
    dep['state'].index_img += 1
    dep['drag']()


def create_circular(var_cir):
    """创建圆"""
    dep = _get_dependencies()
    cir = int(var_cir.get()) * 10
    img = Image.open(dep['circular_image'])
    img = img.resize((cir, cir))
    img.save('./img/cir.png')
    cir_path = './img/cir.png'
    dep['CreateImg'](dep['canvas'], dep['state'].index_img, cir_path).create()
    dep['state'].index_img += 1
    dep['drag']()


# ===== 障碍号和参数相关 =====

def insert(var_id, e_id, CreateTxt, drag_func):
    """障碍号确认"""
    from Common import canvas, state
    state.index_txt += 1
    CreateTxt(canvas, state.index_txt).create(var_id.get())
    e_id.delete(0, 'end')
    drag_func()


def parameter(var_parameter, e_parameter, CreateParameter, drag_func):
    """障碍参数确认"""
    from Common import canvas, state
    state.index_txt += 1
    CreateParameter(canvas, state.index_txt).create(var_parameter.get())
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
