# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Site to DOCX (Windows)

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    # Bundle the templates folder so Flask can find index.html
    datas=[
        ('templates', 'templates'),
    ],
    hiddenimports=[
        # Flask internals
        'flask',
        'jinja2',
        'jinja2.ext',
        'werkzeug',
        'werkzeug.serving',
        'werkzeug.routing',
        # Scraper dependencies
        'selenium',
        'selenium.webdriver',
        'selenium.webdriver.chrome',
        'selenium.webdriver.chrome.options',
        'selenium.webdriver.chrome.service',
        'selenium.webdriver.common.by',
        'bs4',
        'lxml',
        'lxml.etree',
        'lxml._elementpath',
        'docx',
        'docx.shared',
        'docx.enum.text',
        'requests',
        # App modules
        'app',
        'scraper',
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
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SiteToDocx',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    # console=True shows a terminal window — useful so users can see progress
    # and know the app is running. Set to False for a silent background app.
    console=True,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # replace with 'icon.ico' if you have one
)
