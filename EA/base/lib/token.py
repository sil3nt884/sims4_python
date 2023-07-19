__all__ = ['tok_name', 'ISTERMINAL', 'ISNONTERMINAL', 'ISEOF']
def ISTERMINAL(x):
    return x < NT_OFFSET

def ISNONTERMINAL(x):
    return x >= NT_OFFSET

def ISEOF(x):
    return x == ENDMARKER

def _main():
    import re
    import sys
    args = sys.argv[1:]
    if args:
        pass
    inFileName = 'Include/token.h'
    outFileName = 'Lib/token.py'
    if len(args) > 1:
        outFileName = args[1]
    try:
        fp = open(inFileName)
    except OSError as err:
        sys.stdout.write('I/O error: %s\n' % str(err))
        sys.exit(1)
    with fp:
        lines = fp.read().split('\n')
    prog = re.compile('#define[ \\t][ \\t]*([A-Z0-9][A-Z0-9_]*)[ \\t][ \\t]*([0-9][0-9]*)', re.IGNORECASE)
    comment_regex = re.compile('^\\s*/\\*\\s*(.+?)\\s*\\*/\\s*$', re.IGNORECASE)
    tokens = {}
    prev_val = None
    for line in lines:
        match = prog.match(line)
        if match:
            (name, val) = match.group(1, 2)
            val = int(val)
            tokens[val] = {'token': name}
            prev_val = val
        else:
            comment_match = comment_regex.match(line)
            if comment_match and prev_val is not None:
                comment = comment_match.group(1)
                tokens[prev_val]['comment'] = comment
    keys = sorted(tokens.keys())
    try:
        fp = open(outFileName)
    except OSError as err:
        sys.stderr.write('I/O error: %s\n' % str(err))
        sys.exit(2)
    with fp:
        format = fp.read().split('\n')
    try:
        start = format.index('#--start constants--') + 1
        end = format.index('#--end constants--')
    except ValueError:
        sys.stderr.write('target does not contain format markers')
        sys.exit(3)
    lines = []
    for key in keys:
        lines.append('%s = %d' % (tokens[key]['token'], key))
        if 'comment' in tokens[key]:
            lines.append('# %s' % tokens[key]['comment'])
    format[start:end] = lines
    try:
        fp = open(outFileName, 'w')
    except OSError as err:
        sys.stderr.write('I/O error: %s\n' % str(err))
        sys.exit(4)
    with fp:
        fp.write('\n'.join(format))

    _main()