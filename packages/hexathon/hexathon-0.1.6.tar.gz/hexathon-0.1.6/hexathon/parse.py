import re


__re_valid = '^[0-9a-fA-F]+$'
def valid(hx, allow_compact=False):
    l = len(hx)
    if l == 0:
        raise ValueError('invalid hex (invalid length {})'.format(l))
    if not allow_compact and l % 2 != 0:
        raise ValueError('invalid hex (invalid length {}, no compact allowed)'.format(l))
    if not re.match(__re_valid, hx):
        raise ValueError('invalid hex (non-hex character)')
    return hx


def even(hx, allow_empty=False, allow_compact=False):
    if len(hx) % 2 != 0:
        hx = '0' + hx
    if allow_empty and len(hx) == 0:
        return ''
    return valid(hx, allow_compact=allow_compact)


def uniform(hx):
    return even(hx).lower()


def strip_0x(hx, allow_empty=False, compact_value=False, pad=True):
    if len(hx) == 0 and not allow_empty:
        raise ValueError('invalid hex')
    elif len(hx) > 1:
        if hx[:2] == '0x':
            hx = hx[2:]
    if len(hx) > 0:
        hx = valid(hx, allow_compact=True)

    if compact_value:
        v = compact(hx, allow_empty=allow_empty)
    elif pad:
        v = even(hx, allow_empty=allow_empty, allow_compact=True)
    else:
        v = hx
    return v


def add_0x(hx, allow_empty=False, compact_value=False, pad=True):
    if len(hx) == 0 and not allow_empty:
        raise ValueError('invalid hex')
    if hx[:2] == '0x':
        hx = hx[2:]
    v = ''
    if compact_value:
        v = compact(hx, allow_empty=allow_empty)
    elif pad:
        v = even(hx, allow_empty=allow_empty, allow_compact=True)
    else:
        v = hx
    return '0x' + v


def compact(hx, allow_empty=False):
    if len(hx) == 0:
        if not allow_empty:
            raise ValueError('invalid hex (empty)')
    else:
        hx = valid(hx, allow_compact=True)
    i = 0
    for i in range(len(hx)):
        if hx[i] != '0':
            break
    return hx[i:]


def unpad(hx):
    return even(compact(hx))


def pad(hx, byte_length=0, allow_compact=False):
    hx = valid(hx, allow_compact=allow_compact)
    if byte_length == 0:
       hx = even(hx, allow_compact=allow_compact)
    else:
        hx = hx.rjust(byte_length * 2, '0')
    return hx


def int_to_minbytes(v, byteorder='big'):
#    c = 0x100
#    i = 1
#    while c <= v:
#        i += 1
#        c = c << 8
    l = ((v.bit_length() - 1) >> 3) + 1
    return v.to_bytes(l, byteorder=byteorder)


def int_to_minhex(v):
    return int_to_minbytes(v).hex()


def to_int(v, need_prefix=False):
    if len(v) == 0:
        raise ValueError('empty value')
    if need_prefix:
        if len(v) < 2:
            raise ValueError('value too short')
        if v[:2] != '0x':
            raise ValueError('missing prefix')

    v = strip_0x(v)
    return int(v, 16)
