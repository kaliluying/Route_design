# AGENTS.md

This document provides guidelines for AI agents working on the Route_design codebase.

## Project Overview

Route_design is a Python + tkinter application for designing equestrian show jumping courses. Users create course layouts through drag-and-drop operations.

**Tech Stack**: Python 3.9+ | tkinter | Pillow 9.4.0 | PyInstaller

## Build/Lint/Test Commands

### Run Application
```bash
# Development
python main.py

# Install dependencies
pip install -r requirements.txt

# Package for Windows
pyinstaller main.spec
```

### Code Quality
```bash
# Python linting (if flake8 installed)
flake8 --max-line-length=120 .

# Type checking (if mypy installed)
mypy .
```

**Note**: This project has no formal tests. When adding tests, place them in `TEST/` directory and run with `python -m pytest`.

## Code Style Guidelines

### Imports
- Standard library imports first, then third-party, then local
- Use `from Common import *` and `from Tools import *` as the codebase follows this pattern
- Example:
  ```python
  import os
  import tkinter as tk
  from tkinter import messagebox, filedialog
  from PIL import Image, ImageTk
  from Common import *
  from Tools import *
  ```

### Naming Conventions
| Type | Convention | Example |
|------|------------|---------|
| Functions | snake_case | `create_obstacle()`, `get_cur()` |
| Variables | snake_case | `index_img`, `current_tag` |
| Classes | PascalCase | `CreateImg`, `Focus` |
| Constants | UPPER_SNAKE_CASE | `DIRECTION_IMAGE`, `MAX_WIDTH` |
| Tkinter widget names | Chinese descriptive | `frame_edit`, `障碍编辑容器` |

### Type Hints
- Use type hints for new functions: `def set_len(length: float) -> None:`
- Avoid `Any`, `Union`, or `Optional` when possible; prefer explicit types
- Tkinter widgets don't require type hints

### Error Handling
- Use `try/except` with specific exception types when possible:
  ```python
  try:
      result = float(value)
  except ValueError:
      print(f"Invalid value: {value}")
      return None
  ```
- Use `logging.warning()` for errors that don't crash the app:
  ```python
  import logging
  logging.warning("Message here", e)
  ```
- Use `messagebox.showerror()` for user-facing errors

### Code Structure
- **Global state**: Use `Common.py` and `Middleware.py` for shared state
- **Canvas objects**: All canvas objects inherit from `T` class in `scale.py`
- **Singleton pattern**: Used in `Focus` class for edit panel
- **UI layout**: Pack geometry manager preferred over Grid

### File Organization
| File | Purpose |
|------|---------|
| `main.py` | Main window, event handling, UI layout, menu system |
| `focus.py` | Obstacle edit panel with input forms |
| `scale.py` | Canvas object classes (T base class) |
| `Tools.py` | Image processing: merge, expand, rotate |
| `Common.py` | Global state: `current_tag`, `line_tag`, `live_state`, `bar_len` |
| `Middleware.py` | State management functions (get/set) |

### Tkinter Patterns
- Use `functools.partial` for button commands with parameters
- Use `StringVar` for tkinter variable bindings
- Use `win.bind()` for keyboard shortcuts (support both Mac `Command` and Windows `Ctrl`)
- Platform-specific adjustments via `platform.system()`:
  ```python
  import platform
  sys_name = platform.system()  # 'Darwin' or 'Windows'
  font = 21 if sys_name == 'Darwin' else 15
  ```

### Comments & Documentation
- Use Chinese comments (matches existing codebase)
- Document function purpose with docstrings:
  ```python
  def get_cur():
      """
      获取障碍tag和辅助线tag
      :return: (current_tag, line_tag)
      """
  ```

### Layout Guidelines
- 10:1 coordinate ratio (1 pixel = 0.1 meters)
- Default canvas: 90m × 60m (900px × 600px)
- Images loaded from `img/` directory
- Save outputs to `ms_download/` directory

### What to Avoid
- ❌ Bare `except:` clauses
- ❌ `print()` for debugging (use logging instead)
- ❌ Type suppression: `as any`, `@ts-ignore` (Python, so not applicable but avoid equivalent patterns)
- ❌ Deleting test cases to "pass"
- ❌ Mixing `pack()` and `grid()` in the same container

### Frontend Changes (tkinter UI)
- All UI changes are logic changes in this tkinter app
- No separate frontend/backend separation
- UI and logic are intertwined in the same files
