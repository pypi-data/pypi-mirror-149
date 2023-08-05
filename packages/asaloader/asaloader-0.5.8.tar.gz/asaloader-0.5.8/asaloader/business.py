# -*- coding: utf-8 -*-
"""
處理各個副命令對應的業務
"""

from asaloader.locale import _
from asaloader import device
from asaloader import loader
from asaloader import exceptions

import serial.tools.list_ports

import progressbar
import serial
import sys
import time
import math


def do_print_devices(args):
    s = _("Available device list:\n")
    s += _("    device name   \t num \t note\n")
    for dev in device.device_list:
        s += "  - {0:11s}  \t {1:4s}\t {2}\n".format(
            dev['name'], str(dev['dev_type']), dev['note'])

    print(s)


def do_print_ports(args):
    for (port, desc, hwid) in serial.tools.list_ports.comports():
        print("{:20}".format(port))
        print("    desc: {}".format(desc))
        print("    hwid: {}".format(hwid))

def do_prog(args):

    # 建立串列埠物件
    ser = serial.Serial()
    ser.port = args.port
    ser.baudrate = 115200
    ser.timeout = 1
    try:
        ser.open()
    except:
        print(
            _('ERROR: com port has been opened by another application.').format(args.port))
        sys.exit(1)

    # 是否有內部 flash 要被燒錄
    if args.flash_file is None:
        is_prog_flash = False
    else:
        is_prog_flash = True

    # 是否有外部 flash 要被燒錄，
    if args.ext_flash_file is None:
        is_ext_flash = False
    else:
        is_ext_flash = True

    # 是否有 EEPROM 要被燒錄
    if args.eep_file is None:
        is_prog_eep = False
    else:
        is_prog_eep = True

    # 是否要將外部 flash 檔案燒錄至內部 flash
    # TODO: 修正，應不為判定檔案，應只判定 True or False
    # NOTE: 配合 cli_arg.py :114
    if args.ext_to_int is True:
        is_ext_to_int = True
    else:
        is_ext_to_int = False

    # 裝置編號
    device_type = device.get_device_by_str(args.device)

    try:
        l = loader.Loader(
            ser=ser,
            device_type=device_type,
            is_flash_prog=is_prog_flash,
            is_ext_flash_prog=is_ext_flash,
            is_eeprom_prog=is_prog_eep,
            is_ext_to_int=is_ext_to_int,
            is_go_app=args.is_go_app,
            flash_file=args.flash_file,
            ext_flash_file=args.ext_flash_file,
            eeprom_file=args.eep_file,
            go_app_delay=args.go_app_delay
        )
    except exceptions.ComuError:
        print(_("ERROR: Can't communicate with the device."))
        print(_("       Please check the comport and the device."))
        sys.exit(1)
    except exceptions.CheckDeviceError as e:
        print(_("ERROR: Device is not match."))
        print(_("       Assigned device is '{0:s}'".format(
            device.device_list[e.in_dev]['name'])))
        print(_("       Detected device is '{0:s}'".format(
            device.device_list[e.real_dev]['name'])))
        sys.exit(1)

    print(_("Device is '{0:s}'").format(
        device.device_list[l.device_type]['name']))
    print(_('Flash hex size is {0:0.2f} KB ({1} bytes)').format(
        l.flash_size/1024, l.flash_size))
    print(_('Externel Flash hex size is {0:0.2f} KB ({1} bytes)').format(
        l.ext_flash_size/1024, l.ext_flash_size))
    print(_('EEPROM hex size is {0} bytes.').format(l.eeprom_size))
    print(_('Estimated time  is {0:0.2f} s.').format(l.prog_time))

    widgets = [
        ' [', progressbar.Timer(_('Elapsed Time: %(seconds)0.2fs'), ), '] ',
        progressbar.Bar(),
        progressbar.Counter(format='%(percentage)0.2f%%'),
    ]

    bar = progressbar.ProgressBar(
        max_value=l.total_steps, widgets=widgets)
    bar.update(0)
    for i in range(l.total_steps):
        try:
            l.do_step()
            bar.update(i)
        except exceptions.ComuError:
            print(_("ERROR: Can't communicate with the device."))
            print(_("Please check the comport is correct."))
            break
        except Exception:
            bar.finish(end='\n', dirty=True)
            print(_("ERROR: Can't communicate with the device."))
            print(_("Please check the comport is correct."))
            break

    bar.finish(end='\n')
    ser.close()
