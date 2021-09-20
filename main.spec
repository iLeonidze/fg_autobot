# -*- mode: python ; coding: utf-8 -*-

block_cipher = None
options = [ ('u', None, 'OPTION')]

a = Analysis(['main.py'],
             hiddenimports=[],
             pathex=['./'],
             binaries=[], datas=[
                 ('./images/buttons/*', './images/buttons'),
                 ('./images/test_windows/*', './images/test_windows')
             ],
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
          a.datas,
          options,
          exclude_binaries=False,
          name='fg_autobot',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False)

coll = COLLECT(exe,
               a.scripts,
               a.binaries,
               a.zipfiles,
               a.datas,
               debug=False,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='main')
