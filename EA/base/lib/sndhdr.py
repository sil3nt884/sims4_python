__all__ = ['what', 'whathdr']
def what(filename):
    res = whathdr(filename)
    return res

def whathdr(filename):
    with open(filename, 'rb') as f:
        h = f.read(512)
        for tf in tests:
            res = tf(h, f)
            if res:
                return SndHeaders(*res)
        return

def test_aifc(h, f):
    import aifc
    if not h.startswith(b'FORM'):
        return
    if h[8:12] == b'AIFC':
        fmt = 'aifc'
    elif h[8:12] == b'AIFF':
        fmt = 'aiff'
    else:
        return
    f.seek(0)
    try:
        a = aifc.open(f, 'r')
    except (EOFError, aifc.Error):
        return
    return (fmt, a.getframerate(), a.getnchannels(), a.getnframes(), 8*a.getsampwidth())

def test_au(h, f):
    if h.startswith(b'.snd'):
        func = get_long_be
    elif h[:4] in (b'\x00ds.', b'dns.'):
        func = get_long_le
    else:
        return
    filetype = 'au'
    hdr_size = func(h[4:8])
    data_size = func(h[8:12])
    encoding = func(h[12:16])
    rate = func(h[16:20])
    nchannels = func(h[20:24])
    sample_size = 1
    if encoding == 1:
        sample_bits = 'U'
    elif encoding == 2:
        sample_bits = 8
    elif encoding == 3:
        sample_bits = 16
        sample_size = 2
    else:
        sample_bits = '?'
    frame_size = sample_size*nchannels
    if frame_size:
        nframe = data_size/frame_size
    else:
        nframe = -1
    return (filetype, rate, nchannels, nframe, sample_bits)

def test_hcom(h, f):
    if h[65:69] != b'FSSD' or h[128:132] != b'HCOM':
        return
    divisor = get_long_be(h[144:148])
    if divisor:
        rate = 22050/divisor
    else:
        rate = 0
    return ('hcom', rate, 1, -1, 8)
