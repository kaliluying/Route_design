# 渐进式重构计划

## 目标

逐步将 src/ 中的重构模块集成到主程序，同时保持原代码可用。

## 迁移顺序（由易到难）

### 1. 图像处理模块 (image_processor.py)
- 难度：低：低
-
- 风险 目标：用 ImageProcessor 类替换 Tools.py 中的函数

### 2. 画布对象模块 (canvas_objects.py)
- 难度：中
- 风险：中
- 目标：用 CanvasObject 类替换 scale.py 中的 T 类

### 3. 编辑面板模块 (edit_panel.py)
- 难度：中
- 风险：中
- 目标：用 EditPanel 类替换 focus.py 中的 Focus 类

### 4. 状态管理优化
- 难度：高
- 风险：高
- 目标：统一使用 AppState，消除 Common.py 中的冗余代码

## 实施策略

1. **添加兼容性包装器** - 在 src/ 中创建兼容层，让原代码可以调用新模块
2. **条件切换** - 通过配置开关选择使用原版或新版
3. **测试验证** - 每次迁移后验证功能正常
