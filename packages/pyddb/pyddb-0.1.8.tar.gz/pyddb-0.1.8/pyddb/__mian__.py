# -*- coding: utf-8 -*- 
# @Time : 2022/4/6 0006 10:37 
# @Author : ruomubingfeng
# @File : __mian__.py
import argparse
import os
import sys

from pyddb._version import __version__
from pyddb._proto import PROGRAM_NAME
from pyddb._usbmux import Device


def ddb_version(args: argparse.Namespace):
    print(PROGRAM_NAME, "version", __version__)


def ddb_list(args: argparse.Namespace):
    devices = Device.device_info()
    if devices == "[]":
        sys.exit("No devices")
    else:
        sys.exit(devices)


def ddb_device_info(args: argparse.Namespace):
    pass


def ddb_system_info(args: argparse.Namespace):
    pass


def ddb_app_list(args: argparse.Namespace):
    pass


def ddb_screenshot(args: argparse.Namespace):
    pass


def ddb_install(args: argparse.Namespace):
    pass


def ddb_uninstall(args: argparse.Namespace):
    pass


def ddb_reboot(args: argparse.Namespace):
    pass


def ddb_shutdown(args: argparse.Namespace):
    pass


def ddb_xctest(args: argparse.Namespace):
    pass


def ddb_wdaproxy(args: argparse.Namespace):
    pass


def ddb_syslog(args: argparse.Namespace):
    pass


def ddb_crashreport(args: argparse.Namespace):
    pass


def ddb_perf(args: argparse.Namespace):
    pass


def ddb_anr(args: argparse.Namespace):
    pass


def ddb_file(args: argparse.Namespace):
    pass


_commands = [
    dict(action=ddb_version, command="version", help="show current version"),
    dict(action=ddb_list,
         command="list",
         flags=[
             dict(args=['--json'],
                  action='store_true',
                  help='output in json format'),
             dict(args=['--usb'],
                  action='store_true',
                  help='usb USB device'),
             dict(args=['-1'],
                  dest="one",
                  action='store_true',
                  help='output one entry per line')
         ],
         help="show connected devices"),
    dict(
        action=ddb_device_info,
        command="info",
        flags=[
            dict(args=['--json'],
                 action='store_true',
                 help="output as json format"),
            dict(
                args=['-s', '--simple'],
                action='store_true',
                help=
                'use a simple connection to avoid auto-pairing with the device'
            ),
            dict(args=['-k', '--key'],
                 type=str,
                 help='only query specified KEY'),
            dict(args=['--domain'], help='set domain of query to NAME.'),
        ],
        help="show device info"),
    dict(action=ddb_system_info,
         command="sysinfo",
         help="show device system info"),
    dict(action=ddb_app_list,
         command="applist",
         flags=[
             dict(args=['--type'], default='user', help='filter app with type', choices=['user', 'system', 'all'])
         ],
         help="list packages for iOS"),
    dict(action=ddb_screenshot,
         command="screenshot",
         help="take screenshot",
         flags=[dict(args=['filename'], nargs="?", help="output filename")]),
    dict(action=ddb_install,
         command="install",
         flags=[
             dict(args=['-L', '--launch'],

                  help='launch after installed'),
             dict(args=['filepath_or_url'], help="local filepath or url")
         ],
         help="install application"),
    dict(action=ddb_uninstall,
         command="uninstall",
         flags=[dict(args=['bundle_id'], help="bundle_id of application")],
         help="uninstall application"),
    dict(action=ddb_reboot, command="reboot", help="reboot device"),
    dict(action=ddb_shutdown, command="shutdown", help="shutdown device"),
    dict(
        action=ddb_xctest,
        command="xctest",
        flags=[
            dict(args=['--debug'], action='store_true', help='show debug log'),
            dict(args=['-B', '--bundle_id', '--bundle-id'],
                 default="com.*.xctrunner",
                 help="bundle id of the test to launch"),
            dict(args=['--target-bundle-id'],
                 help='bundle id of the target app [optional]'),
            #  dict(args=['-I', '--install-wda'],
            #       action='store_true',
            #       help='install webdriveragent app'),
            dict(args=['-e', '--env'],
                 action='append',
                 help="set env with format key:value, support multi -e"),
        ],
        help="run XCTest"),
    dict(
        action=ddb_wdaproxy,
        command='wdaproxy',
        flags=[
            dict(
                args=['-B', '--bundle_id'],
                default="com.*.xctrunner",
                help="test application bundle id"),
            dict(
                args=['-p', '--port'],
                type=int,
                default=8100,
                help='pc listen port, set to 0 to disable port forward'),
            dict(
                args=['-e', '--env'],
                action='append',
                help="set env with format key:value, support multi -e"),
            dict(
                args=['--check-interval'],
                type=float,
                default=30.0,
                help=
                "check if wda is alive every CHECK_INTERVAL seconds, stop check when set to 0"
            ),
        ],
        help='keep WDA running and relay WDA service to pc for iOS'),
    dict(action=ddb_syslog, command='syslog', help="print device syslog"),
    dict(action=ddb_crashreport,
         command="crashreport",
         flags=[
             dict(args=['--list'], action='store_true', help='list all crash files'),
             dict(args=['--keep'], action='store_true', help="copy but do not remove crash reports from device"),
             dict(args=['--clear'], action='store_true', help='clear crash files'),
             dict(args=['output_directory'], nargs="?", help='The output dir to save crash logs synced from device'),
         ],
         help="crash log tools"),
    dict(action=ddb_perf,
         command="perf",
         flags=[
             dict(args=['-B', '--bundle_id'],
                  help='app bundle id',
                  required=True),
             dict(args=['-o'],
                  dest='perfs',
                  help='cpu,memory,fps,network,screenshot. separate by ","',
                  required=False),
         ],
         help="performance of app"),
    dict(action=ddb_anr,
         command='anr',
         flag=[
             dict(args=['--trace'],
                  help='Below Android 7.0',
                  required=True),
             dict(args=['--bugreport'],
                  help='Above Android 7.0',
                  required=True),
         ],
         help="Android ANR Log"),
    dict(action=ddb_file,
         command='file',
         flag=[
             dict(args=['--push'],
                  help='push file from PC to Android',
                  required=True),
             dict(args=['--pull'],
                  help='pull file from Android to PC',
                  required=True),
         ],
         help="Android push and pull file"),
]


def main():
    parser = argparse.ArgumentParser(
        description="ddb - Device Debug Bridge "
                    "Tool for merge adb and tidevice, version {}, "
                    "created: ruomubingfeng 2022/04/06".format(__version__),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("-v", "--version", action="store_true", help="show current version"),
    parser.add_argument("-d", "--device", help="specify unique device")
    subparser = parser.add_subparsers(dest='subparser')
    actions = {}
    for c in _commands:
        cmd_name = c['command']
        actions[cmd_name] = c['action']
        sp = subparser.add_parser(cmd_name, help=c.get('help'),
                                  formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        for f in c.get('flags', []):
            args = f.get('args')
            # if not args:
            #     args = ['-' * min(2, len(n)) + n for n in f['name']]
            kwargs = f.copy()
            kwargs.pop('name', None)
            kwargs.pop('args', None)
            sp.add_argument(*args, **kwargs)
    args = parser.parse_args()
    if args.version:
        print(__version__)
        return
    if not args.subparser:
        parser.print_help()
        return
    actions[args.subparser](args)


if __name__ == '__main__':
    main()
