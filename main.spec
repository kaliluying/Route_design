# 创建Analysis类的实例a
a = Analysis(
    ['main.py','Common.py', 'focus.py', 'scale.py', 'Tools.py'],  # 待分析的模块列表
    pathex=[r'C:\Users\gaozh\Desktop\Route_design'],  # 搜索模块的路径列表
    binaries=[],  # 附加的二进制文件列表
    datas=[('./img/*','img')],  # 打包的数据文件列表
    hiddenimports=[r'C:\Users\gaozh\Desktop\Route_design'],  # 隐藏的模块列表
    hookspath=[],  # 导入钩子路径列表
    hooksconfig={},  # 钩子配置
    runtime_hooks=[],  # 运行时钩子列表
    excludes=[],  # 排除模块列表
    win_no_prefer_redirects=False,  # Windows平台标志
    win_private_assemblies=False,  # Windows私有程序集
    cipher=block_cipher,  # 加密标志
    noarchive=False,  # 不归档标志
)

# 创建PYZ实例pyz
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)  # 建立捆绑库

# 创建EXE实例exe
exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='路线设计',  # 程序名称
    debug=False,  # 调试标志
    bootloader_ignore_signals=False,  # 引导加载程序忽略信号标志
    strip=False,  # 剥离调试信息
    upx=True,  # 使用UPX压缩
    console=False,  # 控制台标志
    disable_windowed_traceback=False,  # 禁用窗口回溯标志
    argv_emulation=False,  # 命令行参数仿真
    target_arch=None,  # 目标架构
    codesign_identity=None,  # 代码签名标识
    entitlements_file=None,  # 特权文件
)

# 创建COLLECT实例coll
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='路线设计',  # 程序名称
)

# 创建BUNDLE实例app
app = BUNDLE(exe,
    name='路线设计.app',  # 应用程序名称
    icon='img/ic.ico',  # 图标文件
    bundle_identifier=None,  # 捆绑标识
    info_plist={
       "NSHighResolutionCapable":"True",  # 信息属性列表
       })
