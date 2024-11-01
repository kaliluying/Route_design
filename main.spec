# -*- mode: python ; coding: utf-8 -*-  # 文件编码声明，表明该文件为 Python 格式并采用 UTF-8 编码


block_cipher = None  # 初始化加密块，默认设置为 None


a = Analysis(  # 创建一个 Analysis 对象，用于分析应用程序及其依赖
    ['main.py', 'Common.py', 'focus.py', 'scale.py', 'Tools.py', 'Middleware.py'],  # 指定要分析的主要 Python 文件
    pathex=[r'C:\Users\gaozh\Desktop\Route_design'],  # 指定额外的路径，PyInstaller 会在这里查找模块
    # pathex=['/Users/gml/code/python_demo/Route_design'],  # 备用的路径（已注释掉）
    binaries=[],  # 列表用于指定需要打包的二进制文件，如 DLL 等
    datas=[('./img/*', 'img')],  # 指定要打包的额外数据文件，这里打包 'img' 文件夹下的所有文件
    hiddenimports=[r'C:\Users\gaozh\Desktop\Route_design'],  # 指定需要强制包括的隐藏模块
    # hiddenimports=['/Users/gml/code/python_demo/Route_design'],  # 备用的隐藏导入（已注释掉）
    hookspath=[],  # 指定自定义的 hook 脚本路径
    hooksconfig={},  # 钩子配置选项的字典
    runtime_hooks=[],  # 运行时钩子，在程序运行时加载
    excludes=[],  # 指定要排除的模块列表
    win_no_prefer_redirects=False,  # 在 Windows 系统上，是否避免重定向
    win_private_assemblies=False,  # 在 Windows 系统上，是否为私有组件
    cipher=block_cipher,  # 指定加密块，通常设置为 None
    noarchive=False,  # 如果为 True，PyInstaller 将不会创建归档
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)  # 创建一个 PYZ 对象，压缩分析到的纯 Python 模块


exe = EXE(  # 创建可执行文件对象
    pyz,  # 指定之前创建的压缩包作为可执行文件的核心
    a.scripts,  # 包括分析过程中找到的脚本
    [],  # 额外的参数，通常用于包含其他需要的文件（此处为空）
    exclude_binaries=True,  # 设置为 True 时，排除分析到的二进制文件
    name='路线设计',  # 指定生成的可执行文件的名称
    debug=False,  # 是否启用调试模式，设置为 True 可以生成调试信息
    bootloader_ignore_signals=False,  # 是否让 bootloader 忽略信号
    strip=False,  # 是否从可执行文件中剥离调试符号
    upx=True,  # 是否使用 UPX 压缩，以减小可执行文件大小
    console=False,  # 设置为 False 表示不显示控制台窗口（适用于 GUI 应用）
    disable_windowed_traceback=False,  # 是否禁用窗口应用中的 traceback 窗口
    argv_emulation=False,  # 是否启用 argv 模拟，通常在特定场景下使用
    target_arch=None,  # 指定目标架构，未指定则使用默认值
    codesign_identity=None,  # 针对 macOS 指定的代码签名身份（如果适用）
    entitlements_file=None,  # 针对 macOS 指定的权限文件（如果适用）
)

coll = COLLECT(  # 收集文件，准备最终的分发包
    exe,  # 指定前面创建的可执行文件
    a.binaries,  # 包含上述分析到的所有二进制文件
    a.zipfiles,  # 包含 ZIP 文件（如果有）
    a.datas,  # 包含的数据文件
    strip=False,  # 是否剥离文件中的调试信息
    upx=True,  # 是否使用 UPX 压缩
    upx_exclude=[],  # 不需要压缩的文件列表
    name='路线设计',  # 指定最终输出文件的名称
)

app = BUNDLE(  # 创建应用程序包，通常用于 macOS
    exe,  # 指定可执行文件
    name='路线设计.app',  # 指定应用程序包的名称
    icon='img/ic.ico',  # 指定应用的图标文件路径
    bundle_identifier=None,  # 包的标识符（可选，通常用于 macOS）
    info_plist={  # 应用的 Info.plist 配置
       "NSHighResolutionCapable": "True",  # 指定支持高分辨率显示
    }
)
