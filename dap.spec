# -*- mode: python -*-

block_cipher = None


a = Analysis(['apps/dap/src/dap.py'],
             pathex=['apps/meta_models/power_daps/python3/src', '/Users/ppendse/src/power-daps'],
             binaries=None,
             datas=None,
             hiddenimports=['actions', 'actions.default_action'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name='dap',
          debug=False,
          strip=False,
          upx=True,
          console=True )
