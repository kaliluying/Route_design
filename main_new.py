#!/usr/bin/env python3
"""
马术路线设计软件 - 重构版本
主程序入口
"""

import sys
import os
import logging
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from src.core.application import Application


def main():
    """主函数"""
    try:
        # 创建并运行应用程序
        app = Application()
        app.run()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        logging.error(f"程序运行失败: {e}")
        print(f"程序运行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
