# -*- mode: python ; coding: utf-8 -*-

import glob
import os

block_cipher = None

# Find all data files and include them.
base_dir = os.getcwd()
data_files = []
for data_file in glob.glob('**/*json*', recursive=True):
    relpath = os.path.relpath(data_file, base_dir)
    data_dir = os.path.dirname(relpath)
    data_files.append((data_file.replace('\\', '/'), data_dir.replace('\\', '/')))

# Find all of the "hidden imports" and include them.
hidden_imports = [
    'pony.orm.dbproviders',
    'pony.orm.dbproviders.sqlite',
]

a = Analysis(['wow_server.py'],
             pathex=['C:\\Users\\Jeshua\\Code\\wow-server-py'],
             binaries=[],
             datas=data_files,
             hiddenimports=hidden_imports,
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas, [],
          name='wow_server',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=True)
