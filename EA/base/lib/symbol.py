single_input = 256
    if type(_value) is type(0):
        sym_name[_value] = _name
def _main():
    import sys
    import token
    if len(sys.argv) == 1:
        sys.argv = sys.argv + ['Include/graminit.h', 'Lib/symbol.py']
    token._main()

    _main()