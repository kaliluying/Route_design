"""
日志配置模块
提供统一的日志记录功能，支持控制台和文件输出
"""

import os
import sys
import logging
from logging import handlers
from datetime import datetime
from typing import Optional

# 项目根目录
_PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_FILE = os.path.join(_PROJECT_ROOT, "logging.log")


class LoggerConfig:
    """日志配置单例"""

    _instance: Optional["LoggerConfig"] = None
    _initialized: bool = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        self._initialized = True
        self._logger: Optional[logging.Logger] = None
        self._setup_logger()

    def _setup_logger(self):
        """设置日志记录器"""
        # 创建日志文件夹（如果不存在）
        log_dir = os.path.dirname(LOG_FILE)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir, exist_ok=True)

        # 创建logger
        logger = logging.getLogger("RouteDesign")
        logger.setLevel(logging.DEBUG)

        # 防止重复添加handler
        if logger.handlers:
            return

        # ===== 控制台处理器 =====
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(message)s",
            datefmt="%H:%M:%S"
        )
        console_handler.setFormatter(console_format)
        logger.addHandler(console_handler)

        # ===== 文件处理器（轮转日志，保留5个备份）=====
        file_handler = handlers.RotatingFileHandler(
            LOG_FILE,
            maxBytes=1024 * 1024,  # 1MB
            backupCount=5,
            encoding="utf-8"
        )
        file_handler.setLevel(logging.DEBUG)
        file_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(file_format)
        logger.addHandler(file_handler)

        self._logger = logger

    @property
    def logger(self) -> logging.Logger:
        """获取日志记录器"""
        if self._logger is None:
            self._setup_logger()
        return self._logger


# 单例实例
_config: Optional[LoggerConfig] = None


def get_logger() -> logging.Logger:
    """获取日志记录器单例"""
    global _config
    if _config is None:
        _config = LoggerConfig()
    return _config.logger


def log_exception(func):
    """
    异常捕获装饰器
    自动记录函数调用信息和异常详情
    """
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            logger.error(
                f"函数执行失败: {func.__name__}",
                exc_info=True
            )
            raise

    return wrapper


def log_call(func):
    """
    函数调用日志装饰器
    记录函数入口和出口
    """
    from functools import wraps

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger = get_logger()
        logger.debug(f"进入函数: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"退出函数: {func.__name__}")
            return result
        except Exception as e:
            logger.debug(f"异常退出函数: {func.__name__} - {e}")
            raise

    return wrapper


# 便捷函数
debug = lambda msg, *args, **kwargs: get_logger().debug(msg, *args, **kwargs)
info = lambda msg, *args, **kwargs: get_logger().info(msg, *args, **kwargs)
warning = lambda msg, *args, **kwargs: get_logger().warning(msg, *args, **kwargs)
error = lambda msg, *args, **kwargs: get_logger().error(msg, *args, **kwargs)
critical = lambda msg, *args, **kwargs: get_logger().critical(msg, *args, **kwargs)


def clear_log_file():
    """清空日志文件（用于测试）"""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            f.write("")


def get_log_content() -> str:
    """获取日志文件内容"""
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            return f.read()
    return ""
