#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试重构后的界面
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from main_new import main
    print("开始测试重构后的界面...")
    main()
    print("界面测试完成！")
except Exception as e:
    print(f"测试失败: {e}")
    import traceback
    traceback.print_exc()
