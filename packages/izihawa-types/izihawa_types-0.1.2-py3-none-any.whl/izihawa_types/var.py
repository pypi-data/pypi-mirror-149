from typing import Tuple


def varint(x: int, inverted: bool = False) -> bytes:
    buf = b''
    while True:
        towrite = x & 0x7f
        x >>= 7
        if bool(x) != inverted:
            buf += bytes((towrite | 0x80, ))
        else:
            buf += bytes((towrite, ))
        if not x:
            break
    return buf


def varstr(s: bytes, inverted: bool = False) -> bytes:
    return varint(len(s), inverted=inverted) + s


def process_varint(payload: bytes, inverted: bool = False) -> Tuple[int, int]:
    """Read a varint from `stream`"""
    shift = 0
    result = 0
    count = 0
    while True:
        i = payload[count]
        count += 1
        result |= (i & 0x7f) << shift
        shift += 7
        if bool(i & 0x80) == inverted:
            break
    return result, count


def process_varstr(payload: bytes, inverted: bool = False) -> Tuple[bytes, int]:
    n, length = process_varint(payload, inverted=inverted)
    return payload[length:length + n], length + n
