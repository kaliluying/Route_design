# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with this repository.

## Project Overview

Route_design is an equestrian show jumping course design application built with Python and tkinter. Users create professional course layouts through drag-and-drop operations.

**Tech Stack:** Python 3 + tkinter + Pillow 9.4.0 + PyInstaller

## Common Commands

```bash
# Install dependencies (uv)
uv sync

# Run application
python main.py

# Package for Windows
pyinstaller main.spec
```

## Architecture

### Entry Points

- `main.py` - Legacy entry point (still used, imports from Common.py)
- `Common.py` - Compatibility layer that initializes both old and new modules
- `src/` - Refactored modules (partially complete)

### Core Modules

| File | Purpose |
|------|---------|
| `main.py` | Main window, event handling, UI layout, menu system |
| `focus.py` | Obstacle edit panel with input forms |
| `scale.py` | Canvas object classes (legacy T base class) |
| `Tools.py` | Image processing: merge, expand, rotate obstacles |
| `Common.py` | Compatibility layer, exports window/canvas/frames from src |
| `src/state/app_state.py` | `AppState` singleton for global state |
| `src/ui/main_window.py` | Main window refactored |
| `src/core/image_processor.py` | Refactored image processing |

### Class Hierarchy (scale.py)

```
T (base class for all canvas objects)
├── CreateTxt    - Text labels (obstacle numbers)
├── CreateParameter - Parameter text (obstacle measurements)
└── CreateImg    - Image obstacles with full editing support
```

### New Architecture (src/)

```
src/
├── state/
│   └── app_state.py    # AppState singleton - centralized global state
├── ui/
│   ├── main_window.py  # Main window refactored
│   ├── event_handler.py
│   ├── obstacle_handler.py
│   ├── measurement_handler.py
│   └── save_handler.py
├── core/
│   ├── image_processor.py  # Image processing refactored
│   ├── image_loader.py
│   └── obstacle_factory.py
└── models/
    ├── canvas_objects.py    # Refactored canvas objects
    └── edit_panel.py
```

### Image Processing Pipeline (Tools.py / src/core/image_processor.py)

1. Load base image from `img/` directory
2. `expand()` - Make image square
3. `start_direction()` - Add movement direction arrow
4. `@load_image` decorator - Adjust size based on `bar_len`
5. `merge()`, `merge_ab()`, `oxer_obs_ab()` - Combine obstacles

### Global State (src/state/app_state.py)

The `AppState` singleton manages all global state:
- `bar_len` - Global obstacle length (meters)
- `current_tag` - Currently selected canvas object
- `line_tag` - Active measurement line
- `px` - Total route length
- `canvas` dimensions, grid state, measurement state

### Coordinate System

- Ratio: 10:1 (1 pixel = 0.1 meters)
- Default arena: 90m × 60m (900px × 600px)
- Obstacle images loaded from `img/` folder

## UI Layout

- **Left sidebar**: Operation modules, auxiliary modules, measurement modules
- **Top**: Production modules (obstacle type buttons)
- **Center**: Drawing canvas
- **Right**: Competition info panel
- **Menu bar**: Tools, functions, font size, help

## Important Patterns

- **Undo system**: Stack-based undo/redo (Ctrl+Z) - each input field has independent history
- **Cross-platform**: Use `platform.system()` for font and shortcut adjustments (Mac vs Windows)
- **Logging**: Errors logged to `logging.log`, format: `timestamp [level] [filename:line] message`
- **Singleton**: `AppState` in src/state/app_state.py for global state
- **Tkinter**: Pack geometry manager preferred over Grid
