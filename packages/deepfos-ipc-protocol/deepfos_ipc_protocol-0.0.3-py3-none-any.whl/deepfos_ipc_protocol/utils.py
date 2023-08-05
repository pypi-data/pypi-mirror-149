from typing import Dict
from deepfos_ipc_protocol.const import (
    HEADER_REVERSE_FIELD_MAP,
    SUBTASKUPDATE_META,
    SUBTASKUPDATE_FIELD_MAP,
    SUBTASKUPDATE_REVERSE_FIELD_MAP,
    HEADER_META,
    HEADER_FIELD_MAP,
)

import sys


def read_int32(buf):
    return int.from_bytes(buf, sys.byteorder)


def int_to_int32(i: int):
    """将数字转为4字节的字节流"""
    return i.to_bytes(4, sys.byteorder)


def int_to_int16(i: int):
    """将数字转为2字节的字节流"""
    return i.to_bytes(2, sys.byteorder)


def get_filed_map(mtype, reverse: bool) -> Dict[str, str]:
    '''获取字段映射表'''
    if mtype in HEADER_META:
        if reverse:
            return HEADER_REVERSE_FIELD_MAP
        return HEADER_FIELD_MAP
    elif mtype in SUBTASKUPDATE_META:
        if reverse:
            return SUBTASKUPDATE_REVERSE_FIELD_MAP
        return SUBTASKUPDATE_FIELD_MAP
    else:
        raise ValueError("Unknown meta type: {}".format(mtype))


def _to_filed_protocol(mtype: str, d: Dict[str, str]) -> bytes:
    '''filed protocol'''
    buf = b""
    field_map = get_filed_map(mtype, False)
    reversed_field_map = get_filed_map(mtype, True)
    for index, key in field_map.items():
        if key not in reversed_field_map:
            continue
        vlen = int_to_int32(len(d[key]))
        buf += index + vlen + d[key].encode("utf8")
    return buf


def resolve_field_protocol(mtype, num_fields, buf: bytes) -> Dict[str, str]:
    """解析field protocol"""
    ptr = 0
    buf_len = len(buf)
    field_map = get_filed_map(mtype, False)
    result = {}
    while num_fields and ptr < buf_len:
        key = buf[ptr: ptr + 2]
        if key not in field_map:
            raise ValueError(f"Unsupported field: {key}")
        vlen = read_int32(buf[ptr + 2: ptr + 6])
        value = buf[ptr + 6: vlen + ptr + 6]
        result[field_map[key]] = value.decode("utf8")
        ptr += vlen + 6
        num_fields -= 1

    if ptr != buf_len or num_fields != 0:
        raise ValueError("Bad message")

    return result

# ------------------message protocol------------------


def to_msg_protocol(mtype: str, body: str) -> bytes:
    '''message protocol'''
    mtype = mtype.encode("utf8")
    mlen = int_to_int32(len(body))
    body = body.encode("utf8")
    return mtype + mlen + body


def resolve_msg_protocol(buf: bytes) -> str:
    '''解析message protocol'''
    str_len = read_int32(buf[1:5])
    return buf[5: 5+str_len].decode("utf8")


# ------------------header protocol------------------


def to_header_protocol(mtype: str, d: Dict[str, str]):
    '''header protocol'''
    _mtype = mtype.encode("utf8")
    buf_fields = _to_filed_protocol(mtype, d)
    mlen = int_to_int32(len(buf_fields))
    num_fields = int_to_int32(len(d))
    return _mtype + mlen + num_fields + buf_fields


def resolve_header_protocol(buf: bytes) -> Dict[str, str]:
    '''解析header protocol'''
    ptr = 0
    buf_len = len(buf)

    mtype = buf[ptr]
    num_fields = read_int32(buf[5: 9])

    field_buf = buf[9: buf_len]
    result = resolve_field_protocol(mtype, num_fields, field_buf)

    return result

# ------------------DetailList protocol------------------


def to_detaillist_protocol(mtype: str, value_list: list) -> bytes:
    '''detaillist protocol'''
    _mtype = mtype.encode("utf8")
    num_elements = int_to_int32(len(value_list))
    detail_buf = b""
    for index, value in enumerate(value_list):
        detail_buf += _to_detail_protocol(index, value)
    mlen = int_to_int32(len(detail_buf))
    return _mtype + mlen + num_elements + detail_buf


def _to_detail_protocol(index, d: Dict[str, str]) -> bytes:
    index_buf = int_to_int32(index)
    num_fields = int_to_int32(len(d))
    buf_fields = _to_filed_protocol("U", d)
    return index_buf + num_fields + buf_fields


def resolve_detaillist_protocol(buf: bytes) -> list:
    ptr = 0
    field_map = get_filed_map("U", False)
    mlen = read_int32(buf[ptr + 1: ptr + 5])
    num_elements = read_int32(buf[5: 9])
    detail_buf = buf[9: mlen + 9]
    field_buf = detail_buf[8: mlen + 9]
    for _ in range(num_elements):
        result = {}
        num_fields = read_int32(detail_buf[4:8])
        while num_fields:
            key = field_buf[ptr: ptr + 2]
            if key not in field_map:
                raise ValueError(f"Unsupported field: {key}")
            vlen = read_int32(field_buf[ptr + 2: ptr + 6])
            value = field_buf[ptr + 6: vlen + ptr + 6]
            result[field_map[key]] = value.decode("utf8")
            ptr += vlen + 6
            num_fields -= 1
        ptr += 8
        yield result

        if num_fields != 0:
            raise ValueError("Bad message")
