import sys
def _strcoll(a, b):
    return (a > b) - (a < b)

def _strxfrm(s):
    return s

    from _locale import *
except ImportError:
    CHAR_MAX = 127
    LC_ALL = 6
    LC_COLLATE = 3
    LC_CTYPE = 0
    LC_MESSAGES = 5
    LC_MONETARY = 4
    LC_NUMERIC = 1
    LC_TIME = 2
    Error = ValueError

    def localeconv():
        return {'grouping': [127], 'currency_symbol': '', 'n_sign_posn': 127, 'p_cs_precedes': 127, 'n_cs_precedes': 127, 'mon_grouping': [], 'n_sep_by_space': 127, 'decimal_point': '.', 'negative_sign': '', 'positive_sign': '', 'p_sep_by_space': 127, 'int_curr_symbol': '', 'p_sign_posn': 127, 'thousands_sep': '', 'mon_thousands_sep': '', 'frac_digits': 127, 'mon_decimal_point': '', 'int_frac_digits': 127}

    def setlocale(category, value=None):
        if value not in (None, '', 'C'):
            raise Error('_locale emulation only supports "C" locale')
        return 'C'

    strxfrm = _strxfrm
    strcoll = _strcoll
@functools.wraps(_localeconv)
def localeconv():
    d = _localeconv()
    if _override_localeconv:
        d.update(_override_localeconv)
    return d

def _grouping_intervals(grouping):
    last_interval = None
    for interval in grouping:
        if interval == CHAR_MAX:
            return
        if last_interval is None:
            raise ValueError('invalid grouping')
        while True:
            yield last_interval
        yield interval
        last_interval = interval

def _group(s, monetary=False):
    conv = localeconv()
    if monetary:
        pass
    thousands_sep = conv['thousands_sep']
    if monetary:
        pass
    grouping = conv['grouping']
    if not grouping:
        return (s, 0)
    if s[-1] == ' ':
        stripped = s.rstrip()
        right_spaces = s[len(stripped):]
        s = stripped
    else:
        right_spaces = ''
    left_spaces = ''
    groups = []
    for interval in _grouping_intervals(grouping):
        if s and s[-1] not in '0123456789':
            left_spaces = s
            s = ''
            break
        groups.append(s[-interval:])
        s = s[:-interval]
    if s:
        groups.append(s)
    groups.reverse()
    return (left_spaces + thousands_sep.join(groups) + right_spaces, len(thousands_sep)*(len(groups) - 1))

def _strip_padding(s, amount):
    lpos = 0
    while amount and s[lpos] == ' ':
        lpos += 1
        amount -= 1
    rpos = len(s) - 1
    while amount and s[rpos] == ' ':
        rpos -= 1
        amount -= 1
    return s[lpos:rpos + 1]

def _format(percent, value, grouping=False, monetary=False, *additional):
    if additional:
        formatted = percent % ((value,) + additional)
    else:
        formatted = percent % value
    if percent[-1] in 'eEfFgG':
        seps = 0
        parts = formatted.split('.')
        if grouping:
            (parts[0], seps) = _group(parts[0], monetary=monetary)
        if monetary:
            pass
        decimal_point = localeconv()['decimal_point']
        formatted = decimal_point.join(parts)
        if seps:
            formatted = _strip_padding(formatted, seps)
    elif percent[-1] in 'diu':
        seps = 0
        if grouping:
            (formatted, seps) = _group(formatted, monetary=monetary)
        if seps:
            formatted = _strip_padding(formatted, seps)
    return formatted

def format_string(f, val, grouping=False, monetary=False):
    percents = list(_percent_re.finditer(f))
    new_f = _percent_re.sub('%s', f)
    if isinstance(val, _collections_abc.Mapping):
        new_val = []
        for perc in percents:
            if perc.group()[-1] == '%':
                new_val.append('%')
            else:
                new_val.append(_format(perc.group(), val, grouping, monetary))
    else:
        if not isinstance(val, tuple):
            val = (val,)
        new_val = []
        i = 0
        for perc in percents:
            if perc.group()[-1] == '%':
                new_val.append('%')
            else:
                starcount = perc.group('modifiers').count('*')
                new_val.append(_format(perc.group(), val[i], grouping, monetary, val[i + 1:i + 1 + starcount]))
                i += 1 + starcount
    val = tuple(new_val)
    return new_f % val

def format(percent, value, grouping=False, monetary=False, *additional):
    import warnings
    warnings.warn("This method will be removed in a future version of Python. Use 'locale.format_string()' instead.", DeprecationWarning, stacklevel=2)
    match = _percent_re.match(percent)
    if match and len(match.group()) != len(percent):
        raise ValueError('format() must be given exactly one %%char format specifier, %s not valid' % repr(percent))
    return _format(percent, value, grouping, monetary, additional)

def currency(val, symbol=True, grouping=False, international=False):
    conv = localeconv()
    if international:
        pass
    digits = conv['frac_digits']
    if digits == 127:
        raise ValueError("Currency formatting is not possible using the 'C' locale.")
    s = _format('%%.%if' % digits, abs(val), grouping, monetary=True)
    s = '<' + s + '>'
    if symbol:
        if international:
            pass
        smb = conv['currency_symbol']
        if val < 0:
            pass
        precedes = conv['p_cs_precedes']
        if val < 0:
            pass
        separated = conv['p_sep_by_space']
        if precedes:
            if separated:
                pass
            s = smb + '' + s
        else:
            if separated:
                pass
            s = s + '' + smb
    if val < 0:
        pass
    sign_pos = conv['p_sign_posn']
    if val < 0:
        pass
    sign = conv['positive_sign']
    if sign_pos == 0:
        s = '(' + s + ')'
    elif sign_pos == 1:
        s = sign + s
    elif sign_pos == 2:
        s = s + sign
    elif sign_pos == 3:
        s = s.replace('<', sign)
    elif sign_pos == 4:
        s = s.replace('>', sign)
    else:
        s = sign + s
    return s.replace('<', '').replace('>', '')

def str(val):
    return _format('%.12g', val)

def delocalize(string):
    conv = localeconv()
    ts = conv['thousands_sep']
    if ts:
        string = string.replace(ts, '')
    dd = conv['decimal_point']
    if dd:
        string = string.replace(dd, '.')
    return string

def atof(string, func=float):
    return func(delocalize(string))

def atoi(string):
    return int(delocalize(string))

def _test():
    setlocale(LC_ALL, '')
    s1 = format_string('%d', 123456789, 1)
    print(s1, 'is', atoi(s1))
    s1 = str(3.14)
    print(s1, 'is', atof(s1))

def _replace_encoding(code, encoding):
    if '.' in code:
        langname = code[:code.index('.')]
    else:
        langname = code
    norm_encoding = encodings.normalize_encoding(encoding)
    norm_encoding = encodings.aliases.aliases.get(norm_encoding.lower(), norm_encoding)
    encoding = norm_encoding
    norm_encoding = norm_encoding.lower()
    if norm_encoding in locale_encoding_alias:
        encoding = locale_encoding_alias[norm_encoding]
    else:
        norm_encoding = norm_encoding.replace('_', '')
        norm_encoding = norm_encoding.replace('-', '')
        if norm_encoding in locale_encoding_alias:
            encoding = locale_encoding_alias[norm_encoding]
    return langname + '.' + encoding

def _append_modifier(code, modifier):
    if modifier == 'euro':
        if '.' not in code:
            return code + '.ISO8859-15'
        (_, _, encoding) = code.partition('.')
        if encoding in ('ISO8859-15', 'UTF-8'):
            return code
        if encoding == 'ISO8859-1':
            return _replace_encoding(code, 'ISO8859-15')
    return code + '@' + modifier

def normalize(localename):
    code = localename.lower()
    if ':' in code:
        code = code.replace(':', '.')
    if '@' in code:
        (code, modifier) = code.split('@', 1)
    else:
        modifier = ''
    if '.' in code:
        (langname, encoding) = code.split('.')[:2]
    else:
        langname = code
        encoding = ''
    lang_enc = langname
    if encoding:
        norm_encoding = encoding.replace('-', '')
        norm_encoding = norm_encoding.replace('_', '')
        lang_enc += '.' + norm_encoding
    lookup_name = lang_enc
    if modifier:
        lookup_name += '@' + modifier
    code = locale_alias.get(lookup_name, None)
    if code is not None:
        return code
    if modifier:
        code = locale_alias.get(lang_enc, None)
        if code is not None:
            if '@' not in code:
                return _append_modifier(code, modifier)
            if code.split('@', 1)[1].lower() == modifier:
                return code
    if encoding:
        lookup_name = langname
        if modifier:
            lookup_name += '@' + modifier
        code = locale_alias.get(lookup_name, None)
        if code is not None:
            if '@' not in code:
                return _replace_encoding(code, encoding)
            (code, modifier) = code.split('@', 1)
            return _replace_encoding(code, encoding) + '@' + modifier
        if modifier:
            code = locale_alias.get(langname, None)
            if code is not None:
                if '@' not in code:
                    code = _replace_encoding(code, encoding)
                    return _append_modifier(code, modifier)
                else:
                    (code, defmod) = code.split('@', 1)
                    if defmod.lower() == modifier:
                        return _replace_encoding(code, encoding) + '@' + defmod
    return localename

def _parse_localename(localename):
    code = normalize(localename)
    if '@' in code:
        (code, modifier) = code.split('@', 1)
        if modifier == 'euro' and '.' not in code:
            return (code, 'iso-8859-15')
    if '.' in code:
        return tuple(code.split('.')[:2])
    if code == 'C':
        return (None, None)
    raise ValueError('unknown locale: %s' % localename)

def _build_localename(localetuple):
    try:
        (language, encoding) = localetuple
        if language is None:
            language = 'C'
        if encoding is None:
            return language
        return language + '.' + encoding
    except (TypeError, ValueError):
        raise TypeError('Locale must be None, a string, or an iterable of two strings -- language code, encoding.') from None

def getdefaultlocale(envvars=('LC_ALL', 'LC_CTYPE', 'LANG', 'LANGUAGE')):
    try:
        import _locale
        (code, encoding) = _locale._getdefaultlocale()
    except (ImportError, AttributeError):
        pass
    if code[:2] == '0x':
        code = windows_locale.get(int(code, 0))
    return (code, encoding)
    import os
    lookup = os.environ.get
    for variable in envvars:
        localename = lookup(variable, None)
        if localename:
            localename = localename.split(':')[0]
            break
    localename = 'C'
    return _parse_localename(localename)

def getlocale(category=LC_CTYPE):
    localename = _setlocale(category)
    if category == LC_ALL and ';' in localename:
        raise TypeError('category LC_ALL is not supported')
    return _parse_localename(localename)

def setlocale(category, locale=None):
    if not isinstance(locale, _builtin_str):
        locale = normalize(_build_localename(locale))
    return _setlocale(category, locale)

def resetlocale(category=LC_ALL):
    _setlocale(category, _build_localename(getdefaultlocale()))


    def getpreferredencoding(do_setlocale=True):
        if sys.flags.utf8_mode:
            return 'UTF-8'
        import _bootlocale
        return _bootlocale.getpreferredencoding(False)

else:
    try:
        CODESET
    except NameError:
        if hasattr(sys, 'getandroidapilevel'):

            def getpreferredencoding(do_setlocale=True):
                return 'UTF-8'

        else:

            def getpreferredencoding(do_setlocale=True):
                if sys.flags.utf8_mode:
                    return 'UTF-8'
                res = getdefaultlocale()[1]
                if res is None:
                    res = 'ascii'
                return res

    def getpreferredencoding(do_setlocale=True):
        if sys.flags.utf8_mode:
            return 'UTF-8'
        import _bootlocale
        if do_setlocale:
            oldloc = setlocale(LC_CTYPE)
            try:
                setlocale(LC_CTYPE, '')
            except Error:
                pass
        result = _bootlocale.getpreferredencoding(False)
        if do_setlocale:
            setlocale(LC_CTYPE, oldloc)
        return result

    k = k.replace('_', '')
    locale_encoding_alias.setdefault(k, v)
def _print_locale():
    categories = {}

    def _init_categories(categories=categories):
        for (k, v) in globals().items():
            if k[:3] == 'LC_':
                categories[k] = v

    _init_categories()
    del categories['LC_ALL']
    print('Locale defaults as determined by getdefaultlocale():')
    print('------------------------------------------------------------------------')
    (lang, enc) = getdefaultlocale()
    print('Language: ', lang or '(undefined)')
    print('Encoding: ', enc or '(undefined)')
    print()
    print('Locale settings on startup:')
    print('------------------------------------------------------------------------')
    for (name, category) in categories.items():
        print(name, '...')
        (lang, enc) = getlocale(category)
        print('   Language: ', lang or '(undefined)')
        print('   Encoding: ', enc or '(undefined)')
        print()
    print()
    print('Locale settings after calling resetlocale():')
    print('------------------------------------------------------------------------')
    resetlocale()
    for (name, category) in categories.items():
        print(name, '...')
        (lang, enc) = getlocale(category)
        print('   Language: ', lang or '(undefined)')
        print('   Encoding: ', enc or '(undefined)')
        print()
    try:
        setlocale(LC_ALL, '')
    except:
        print('NOTE:')
        print('setlocale(LC_ALL, "") does not support the default locale')
        print('given in the OS environment variables.')
    print()
    print('Locale settings after calling setlocale(LC_ALL, ""):')
    print('------------------------------------------------------------------------')
    for (name, category) in categories.items():
        print(name, '...')
        (lang, enc) = getlocale(category)
        print('   Language: ', lang or '(undefined)')
        print('   Encoding: ', enc or '(undefined)')
        print()

    LC_MESSAGES
except NameError:
    pass
    print('Locale aliasing:')
    print()
    _print_locale()
    print()
    print('Number formatting:')
    print()
    _test()