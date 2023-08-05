# -*- coding: utf-8 -*-
"""
CLI介面參數解析處理
"""

from asaloader.locale import _
from asaloader import device
from asaloader import business
from asaloader import ihex

import argparse
import os
import sys
import serial.tools.list_ports
import gettext


def parser_init(parser: argparse.ArgumentParser):

    parser.description = _('Program to ASA-series board.')

    # lc 語系參數
    parser.add_argument(
        '--lc',
        action='store',
        dest='lc',
        type=str,
        required=False,
        default='',
        help=_('Set the language code. e.g. `zh_TW`, `en_US`')
    )

    subparsers = parser.add_subparsers(dest='subcmd')

    # parser of programming subcommand
    # "燒錄"副命令的解析器
    parser_pr = subparsers.add_parser(
        'prog',
        aliases=[],
        help=_('Program code to board.')
    )

    parser_prog_init(parser_pr)

    # parser of print-devices subcommand
    # "印出可選裝置列表"副命令的解析器
    parser_pd = subparsers.add_parser(
        'print-devices',
        aliases=['pd'],
        help=_('List all available devices.')
    )

    # parser of print-ports subcommand
    # "印出串列埠列表"副命令的解析器
    parser_pp = subparsers.add_parser(
        'print-ports',
        aliases=['pp'],
        help=_('List all available serial ports.')
    )


def parser_prog_init(parser: argparse.ArgumentParser):
    """初始化"燒錄"副命令的解析器

    Args:
        parser (argparse.ArgumentParser): "燒錄"副命令的解析器
    """

    ## 裝置種類選擇參數 -d
    arg_d_help = _('The name or number of the device type to be programmed. ')
    arg_d_help += _('Can see available device type by subcommand print-device-list.')
    parser.add_argument(
        *('-d', '--decice'),
        action='store',
        dest='device',
        type=str,
        default='auto',
        help=arg_d_help
    )

    ## 串列埠選擇參數 -p
    arg_p_help = _('The serial port which program burn the device.')
    parser.add_argument(
        *('-p', '--port'),
        action='store',
        dest='port',
        type=str,
        required=True,
        help=arg_p_help
    )

    # flash 燒錄檔案參數 -f
    arg_f_help = _('Set binary file which program to flash.')
    parser.add_argument(
        *('-f', '--flash'),
        action='store',
        dest='flash_file',
        type=str,
        required=False,
        help=arg_f_help
    )

    # ext_flash 燒錄檔案參數 -E
    arg_E_help = _('Set binary file which program to externel flash.')
    parser.add_argument(
        *('-E', '--extflash'),
        action='store',
        dest='ext_flash_file',
        type=str,
        required=False,
        help=arg_E_help
    )

    # ext_to_int 燒錄檔案參數 -i
    arg_i_help = _('Program from externel flash to internel flash.')
    parser.add_argument(
        *('-i', '--ext2int'),
        action='store_true',
        dest='ext_to_int',
        # type=str,
        required=False,
        help=arg_i_help
    )

    # eeprom 燒錄檔案參數 -e
    arg_e_help = _('Set binary file which program to eeprom.')
    parser.add_argument(
        *('-e', '--eeprom'),
        action='store',
        dest='eep_file',
        type=str,
        required=False,
        help=arg_e_help
    )

    ## 燒錄完執行應用參數 -a
    arg_a_help = _('Enter the application after programing.')
    parser.add_argument(
        *('-a', '--after-prog-go-app'),
        action='store_true',
        dest='is_go_app',
        required=False,
        help=arg_a_help
    )

    ## 執行應用延遲參數 -D
    arg_D_help = _(
        'Set delay time from programing completion to executing application.(in ms)')
    parser.add_argument(
        *('-D', '--go-app-delay'),
        dest='go_app_delay',
        type=int,
        required=False,
        default=50,
        help=arg_D_help
    )


def chk_prog_args(args: argparse.Namespace) -> bool:
    """檢查副命令'prog'的參數是否合法

    Args:
        args (argparse.Namespace): CLI介面解析完的參數

    Returns:
        bool: True，合法；False，不合法。
    """

    # 裝置種類選擇參數 -d
    res = device.get_device_by_str(args.device)

    if res == -1:
        print(_('Error: Parameter --device is illegal.'))
        business.do_print_devices(args)
        return False

    # 是否為 ext_to_int，
    # 否，則進入 ext-flash, flash, eeprom ，判斷有無指定檔案
    # 沒有要燒錄的檔案
    if (args.ext_to_int):
        pass
    elif (args.flash_file is None) and \
       (args.eep_file is None) and \
       (args.ext_flash_file is None):
        errmsg = _(
            'Error: No flash or eeprom needs to be burned, please use \'-f \', \'-e \', \'-E \' to specify the file.')
        print(errmsg)
        return False

    # Flash 檔案檢查
    if args.flash_file is not None:
        if not os.path.isfile(args.flash_file):
            errmsg = _('Error: Cannot find flash binary file {0}.')
            print(errmsg.format(args.flash_file))
            return False
        elif not ihex.is_ihex(args.flash_file):
            errmsg = _(
                'Error: The flash binary file {0} is not ihex formatted.')
            print(errmsg.format(args.flash_file))
            return False

    # Flash 檔案檢查 (外部 flash)
    if args.ext_flash_file is not None:
        if not os.path.isfile(args.ext_flash_file):
            errmsg = _('Error: Cannot find flash binary file {0}.')
            print(errmsg.format(args.ext_flash_file))
            return False
        elif not ihex.is_ihex(args.ext_flash_file):
            errmsg = _(
                'Error: The flash binary file {0} is not ihex formatted.')
            print(errmsg.format(args.ext_flash_file))
            return False

    # EEPROM 檔案檢查
    if args.eep_file is not None:
        if not os.path.isfile(args.eep_file):
            errmsg = _('Error: Cannot find eeprom binary file {0}.')
            print(errmsg.format(args.eep_file))
            return False
        elif not ihex.is_ihex(args.eep_file):
            errmsg = _(
                'Error: The eeprom binary file {0} is not ihex formatted.')
            print(errmsg.format(args.eep_file))
            return False

    # 串列埠合法檢查
    if args.port not in [p[0] for p in serial.tools.list_ports.comports()]:
        print(_('Error: Cannot find serial port {0}.').format(args.port))
        print(_('The available serial ports are as follows:'))
        business.do_print_ports(args)
        return False

def chk_print_ports_args(args: argparse.Namespace) -> bool:
    """檢查副命令'print-ports'的參數是否合法

    Args:
        args (argparse.Namespace): CLI介面解析完的參數

    Returns:
        bool: True，合法；False，不合法。
    """
    # 無參數直接回傳正確
    return True

def chk_print_devices_args(args: argparse.Namespace) -> bool:
    """檢查副命令'print-devices'的參數是否合法

    Args:
        args (argparse.Namespace): CLI介面解析完的參數

    Returns:
        bool: True，合法；False，不合法。
    """
    # 無參數直接回傳正確
    return True
