from __future__ import absolute_import
def load_ipython_extension(ip):
    from Build.IpythonMagic import CythonMagics
    ip.register_magics(CythonMagics)
