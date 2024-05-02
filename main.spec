# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['main.py','Commom.py', 'focus.py', 'scale.py', 'Tools.py'],
    pathex=['/Users/gml/code/python_demo/Route_design'],
    binaries=[],
    datas=[('./img/*','img')],
    hiddenimports=['/Users/gml/code/python_demo/Route_design'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='路线设计',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,

)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='路线设计',
)
app = BUNDLE(exe,
    name='路线设计.app',
    icon='img/ic.ico',
    bundle_identifier=None,
    info_plist={
       "NSHighResolutionCapable":"True",
       })
