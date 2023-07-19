__all__ = ['cmp_op', 'hasconst', 'hasname', 'hasjrel', 'hasjabs', 'haslocal', 'hascompare', 'hasfree', 'opname', 'opmap', 'HAVE_ARGUMENT', 'EXTENDED_ARG', 'hasnargs']
    from _opcode import stack_effect
    __all__.append('stack_effect')
except ImportError:
    pass
def def_op(name, op):
    opname[op] = name
    opmap[name] = op

def name_op(name, op):
    def_op(name, op)
    hasname.append(op)

def jrel_op(name, op):
    def_op(name, op)
    hasjrel.append(op)

def jabs_op(name, op):
    def_op(name, op)
    hasjabs.append(op)
