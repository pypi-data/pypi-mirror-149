# -*- coding: utf-8 -*-
"""
asaloader程式CLI介面的進入點。
"""

from asaloader import cli_arg
from asaloader import business

import argparse
import sys

def run():
    # CLI 參數解析
    parser = argparse.ArgumentParser()
    cli_arg.parser_init(parser)
    args = parser.parse_args()

    # 副命令分發
    if args.subcmd == 'print-devices' or args.subcmd == 'pd':
        if cli_arg.chk_print_devices_args(args) is False:
            sys.exit(1)
        else:
            business.do_print_devices(args)

    elif args.subcmd == 'print-ports' or args.subcmd == 'pp':
        if cli_arg.chk_print_ports_args(args) is False:
            sys.exit(1)
        else:
            business.do_print_ports(args)

    elif args.subcmd == 'prog':
        if cli_arg.chk_prog_args(args) is False:
            sys.exit(1)
        else:
            business.do_prog(args)

    else:
        parser.print_help()


if __name__ == '__main__':
    run()
