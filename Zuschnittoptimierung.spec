# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_all

datas = [('app.py', '.'), ('config.py', '.'), ('optimizer.py', '.'), ('excel_handler.py', '.')]
binaries = []
hiddenimports = ['streamlit', 'streamlit.web.cli', 'streamlit.runtime.scriptrunner.magic_funcs', 'pandas', 'openpyxl', 'plotly', 'plotly.graph_objects', 'plotly.express', 'altair', 'PIL', 'PIL.Image', 'packaging', 'packaging.version', 'packaging.specifiers', 'packaging.requirements', 'pyarrow', 'tornado', 'tornado.web', 'click', 'validators', 'watchdog']
tmp_ret = collect_all('streamlit')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('plotly')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]
tmp_ret = collect_all('altair')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]


a = Analysis(
    ['app_launcher.py'],
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Zuschnittoptimierung',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='NONE',
)
