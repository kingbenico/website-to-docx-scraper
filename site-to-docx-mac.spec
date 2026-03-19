# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec file for Site to DOCX (macOS)

block_cipher = None

a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
    ],
    hiddenimports=[
        # Flask internals
        'flask',
        'jinja2',
        'jinja2.ext',
        'werkzeug',
        'werkzeug.serving',
        'werkzeug.routing',
        # Selenium — full module tree
        'selenium',
        'selenium.webdriver',
        'selenium.webdriver.chrome',
        'selenium.webdriver.chrome.webdriver',
        'selenium.webdriver.chrome.options',
        'selenium.webdriver.chrome.service',
        'selenium.webdriver.chromium',
        'selenium.webdriver.chromium.webdriver',
        'selenium.webdriver.chromium.options',
        'selenium.webdriver.chromium.service',
        'selenium.webdriver.common',
        'selenium.webdriver.common.by',
        'selenium.webdriver.common.options',
        'selenium.webdriver.common.driver_finder',
        'selenium.webdriver.common.service',
        'selenium.webdriver.remote',
        'selenium.webdriver.remote.webdriver',
        'selenium.webdriver.remote.remote_connection',
        'selenium.webdriver.remote.command',
        'selenium.webdriver.remote.errorhandler',
        'selenium.common',
        'selenium.common.exceptions',
        'selenium.webdriver.common.selenium_manager',
        # BS4 / lxml
        'bs4',
        'lxml',
        'lxml.etree',
        'lxml._elementpath',
        'lxml.html',
        # python-docx
        'docx',
        'docx.shared',
        'docx.enum.text',
        'docx.oxml',
        'docx.oxml.ns',
        # requests + urllib3
        'requests',
        'urllib3',
        'urllib3.util',
        'certifi',
        'charset_normalizer',
        'idna',
        # UI
        'tkinter',
        'tkinter.ttk',
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
    console=True,  # show terminal so users can see it's running
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,
)

app = BUNDLE(
    exe,
    name='SiteToDocx.app',
    icon=None,
    bundle_identifier='com.sitetodocx.app',
    info_plist={
        'NSPrincipalClass': 'NSApplication',
        'NSHighResolutionCapible': True,
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleName': 'Site to DOCX',
        'LSUIElement': False,
        'NSAppTransportSecurity': {
            'NSAllowsLocalNetworking': True,
            'NSAllowsArbitraryLoads': True,
        },
    },
)
