# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Video Unicalization Desktop App
"""

import sys
from pathlib import Path

block_cipher = None

# Get the project root directory
project_root = Path('.').absolute()

# Collect all Python files and dependencies
a = Analysis(
    ['main.py'],
    pathex=[str(project_root)],
    binaries=[],
    datas=[
        ('.env.example', '.'),
        ('README.md', '.'),
    ],
    hiddenimports=[
        'aiogram',
        'fastapi',
        'uvicorn',
        'sqlalchemy',
        'aiosqlite',
        'ffmpeg',
        'kivy',
        'kivy.core.window',
        'kivy.core.text',
        'kivy.core.image',
        'kivy.garden',
        'pkg_resources.py2_warn',
        'pydantic',
        'pydantic_settings',
        'python_multipart',
        'jinja2',
        'aiofiles',
        'PIL',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
    ],
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
    name='VideoUnicalization',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,  # Set to False for windowed app (no console)
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add icon path here if you have one
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='VideoUnicalization',
)

# For macOS, create an app bundle
if sys.platform == 'darwin':
    app = BUNDLE(
        coll,
        name='VideoUnicalization.app',
        icon=None,  # Add icon path here if you have one
        bundle_identifier='com.videounicalization.app',
        info_plist={
            'NSPrincipalClass': 'NSApplication',
            'NSHighResolutionCapable': 'True',
            'CFBundleShortVersionString': '1.0.0',
        },
    )
