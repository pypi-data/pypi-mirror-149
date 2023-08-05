# -*- coding: utf-8 -*-
"""
裝置列表及相關函式
"""

from asaloader.locale import _

device_list = [
    {
        'name': 'auto',
        'dev_type': 0,
        'protocol_version': 0,
        'userapp_start': 0,
        'userapp_size':  0,
        'note': _('Default, auto detect device type.')
    },
    {
        'name': 'asa_m128_v1',
        'dev_type': 1,
        'protocol_version': 1,
        'userapp_start': 0x00000000,
        'userapp_size':  0x0001F000,
        'note': ''
    },
    {
        'name': 'asa_m128_v2',
        'dev_type': 2,
        'protocol_version': 1,
        'userapp_start': 0x00000000,
        'userapp_size':  0x0001F000,
        'note': ''
    },
    {
        'name': 'asa_m128_v3',
        'dev_type': 3,
        'protocol_version': 2,
        'userapp_start': 0x00000000,
        'userapp_size':  0x0001F000,
        'note': ''
    },
    {
        'name': 'asa_m3_v1',
        'dev_type': 4,
        'protocol_version': 2,
        'userapp_start': 0x00001000,
        'userapp_size':  0x0007F000,
        'note': ''
    },
    {
        'name': 'asa_m4_v1',
        'dev_type': 5,
        'protocol_version': 2,
        'userapp_start': 0x00010000,
        'userapp_size':  0x000F0000,
        'note': ''
    }
]

def get_device_by_str(s: str) -> int:
    """取得字串對應的裝置編號

    Args:
        s (str): 字串，可為裝置名稱、數字字串

    Returns:
        int: 裝置編號。-1代表失敗，s不符合格式。
    """
    if s.isdigit():
        for d in device_list:
            if int(s) == d['dev_type']:
                return d['dev_type']
    else:
        for d in device_list:
            if s == d['name']:
                return d['dev_type']
    return -1
