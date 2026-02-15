"""
Common.py 兼容层
提供旧全局变量名到 AppState 的映射

使用方法:
    from src.state.compat import WIDTH, HEIGHT, sys_name
"""
import tkinter as tk
from typing import Any

# 延迟导入
_app_state_cls = None


def _get_state():
    """获取 AppState 单例"""
    global _app_state_cls
    if _app_state_cls is None:
        from .app_state import AppState
        _app_state_cls = AppState
    return _app_state_cls()


class _TkVarProxy:
    """Tk 变量代理，用于兼容旧代码"""

    def __init__(self, name: str):
        self._name = name

    def get(self):
        return getattr(_get_state(), self._name).get()

    def set(self, value):
        getattr(_get_state(), self._name).set(value)

    def __repr__(self):
        return f"<_TkVarProxy({self._name})>"


class _DynamicModule:
    """动态模块，用于模拟全局变量"""

    def __getattr__(self, name: str) -> Any:
        state = _get_state()
        # 检查是否是 tk 变量
        if name in ('X', 'Y', 'what', 'no_what', 'move_x', 'move_y',
                    'start_x', 'start_y', 'end_x', 'end_y'):
            return _TkVarProxy(name)
        # 检查是否是普通属性
        if hasattr(state, name):
            attr = getattr(state, name)
            # 如果是 tk.Variable，直接返回
            if isinstance(attr, tk.Variable):
                return attr
            return attr
        raise AttributeError(f"模块没有属性 '{name}'")

    def __setattr__(self, name: str, value: Any) -> None:
        if name.startswith('_'):
            object.__setattr__(self, name, value)
        else:
            setattr(_get_state(), name, value)


# 创建动态模块
_state = _DynamicModule()


def __getattr__(name: str) -> Any:
    """模块级 __getattr__ 用于延迟导入"""
    return getattr(_state, name)


def __setattr__(name: str, value: Any) -> None:
    """模块级 __setattr__ 用于设置状态"""
    setattr(_state, name, value)


# ===== 便捷函数 =====

def update_sys_name(name: str):
    """更新系统名称"""
    _get_state().set_system(name)


def update_canvas_size(width: int, height: int):
    """更新画布尺寸"""
    _get_state().update_canvas_size(width, height)


def get_bar_len() -> float:
    """获取障碍长度"""
    return _get_state().bar_len


def set_bar_len(value: float):
    """设置障碍长度"""
    _get_state().bar_len = float(value)


def get_current_tag():
    """获取当前选中标签"""
    return _get_state().current_tag


def set_current_tag(tag):
    """设置当前选中标签"""
    _get_state().current_tag = tag
