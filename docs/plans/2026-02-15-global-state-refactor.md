# 重构设计方案：全局变量迁移到 AppState

## 目标

将 main.py 和 scale.py 中的所有全局变量迁移到 AppState 单例，消除 `global` 声明，实现集中式状态管理。

## 问题现状

1. **main.py** 使用大量 `global` 声明但变量未在模块级定义
2. **scale.py** 使用全局变量 `choice_tup`, `stack`, `rotate_` 等但未正确导入
3. **Common.py** 已做部分导出，但使用不完整

## 架构设计

### AppState 增强

在现有 `src/state/app_state.py` 基础上添加：

```python
# 新增变量
self.watermark = None      # 水印 canvas 对象
self.fg_img = None         # 前景图像
self.fg_path = ""         # 前景图像路径
self.info_var = []         # 比赛信息变量列表
self.pro_var = []          # 比赛信息值列表
self.h1 = None            # 画布长文本对象
self.h2 = None            # 画布宽文本对象
self.route_click = []      # 路线点击历史（兼容旧代码）
self.aux_stare = True     # 辅助信息显示状态
self.current_frame_stare = True  # 多选框状态
```

### 变量映射表

| 旧变量名 | AppState 属性 | 说明 |
|----------|---------------|------|
| `choice_tup` | `choice_tuple` | 多选框坐标 |
| `route_click` | `route_clicks` | 路线点击 |
| `current_frame_stare` | `current_frame_stare` | 多选框状态 |
| `aux_stare` | `aux_state` | 辅助信息 |

## 实施步骤

### 1. 增强 AppState
- 添加缺失的变量定义
- 添加便捷访问器方法

### 2. 更新 Common.py
- 导出 AppState 实例
- 添加模块级变量引用（兼容旧代码）

### 3. 重构 main.py
- 删除所有 `global` 声明
- 使用 `Common.state` 或 `get_app_state()` 访问状态
- 更新变量引用（如 `index_txt` → `state.index_txt`）

### 4. 重构 scale.py
- 正确导入 AppState
- 替换全局变量为 `state.xxx`
- 删除不必要的 `global` 声明

## 验收标准

1. 运行 `python main.py` 无全局变量错误
2. 所有障碍物操作（拖拽、旋转、删除）正常工作
3. 测量功能正常工作
4. 撤销/重做功能正常工作
