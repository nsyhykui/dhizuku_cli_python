# dcli - 通过 TCP 调用 Dhizuku 的 DO 命令工具
# Copyright (C) 2026 nsyhykui
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

# -*- coding: utf-8 -*-
"""
帮助文本、命令表和版本输出。
"""

import sys

from . import __version__
from .i18n import t, IS_ZH, err


HELP = {
    "ping": {
        "desc": "测试连接是否正常" if IS_ZH else "Test connection",
        "usage": "dcli ping",
    },
    "lock_now": {
        "desc": "立即锁屏" if IS_ZH else "Lock screen now",
        "usage": "dcli lock_now",
    },
    "hide": {
        "desc": "隐藏指定应用" if IS_ZH else "Hide app",
        "usage": "dcli hide <package>",
    },
    "unhide": {
        "desc": "取消隐藏指定应用" if IS_ZH else "Unhide app",
        "usage": "dcli unhide <package>",
    },
    "suspend": {
        "desc": "挂起指定应用" if IS_ZH else "Suspend app",
        "usage": "dcli suspend <package>",
    },
    "resume": {
        "desc": "恢复挂起指定应用" if IS_ZH else "Resume app",
        "usage": "dcli resume <package>",
    },
    "block_uninstall": {
        "desc": "阻止卸载指定应用" if IS_ZH else "Block uninstall",
        "usage": "dcli block_uninstall <package>",
    },
    "unblock_uninstall": {
        "desc": "允许卸载指定应用" if IS_ZH else "Unblock uninstall",
        "usage": "dcli unblock_uninstall <package>",
    },
    "status": {
        "desc": "查询状态" if IS_ZH else "Query status",
        "usage": "dcli status <subcommand>",
    },
}


def is_known_command(cmd):
    return cmd in HELP


def print_global():
    print("dcli - " + ("DO Server 命令行客户端" if IS_ZH else "DO Server CLI client"))
    print()
    print(t("usage"))
    print("  dcli [--host <ip>] help [command]")
    print("  dcli [--host <ip>] <command> [args]")
    print()
    print("Options:" if not IS_ZH else "选项:")
    print(t("opt_host"))
    print(t("opt_version"))
    print(t("opt_help"))
    print(t("opt_end"))
    print()
    print(t("available"))
    for name in sorted(HELP.keys()):
        print("  %-18s %s" % (name, HELP[name]["desc"]))
    print()
    print(t("examples"))
    print("  dcli ping")
    print("  dcli lock_now")
    print("  dcli status hid")
    print("  dcli status permission android.permission.CAMERA")


def print_command(cmd):
    if cmd not in HELP:
        err(t("unknown_cmd") % cmd)
        sys.exit(1)
    info = HELP[cmd]
    print(t("usage_short") % info["usage"])
    print(t("desc") % info["desc"])


def print_version(server_version):
    """
    server_version:
      None      → 连不上服务端
      "unknown" → 服务端不认 #$%version
      其他字符串  → 服务端版本号
    """
    if server_version is None:
        print("dcli " + __version__)
    elif server_version == "unknown":
        suffix = "Dhizuku Cli 2.0.0 或更早" if IS_ZH else "Dhizuku Cli 2.0.0 or earlier"
        print("dcli %s, %s" % (__version__, suffix))
    else:
        print("dcli %s, Dhizuku Cli %s" % (__version__, server_version))

    print("Copyright (C) 2026 nsyhykui")
    print("License GPLv3+: GNU GPL version 3 or later <https://gnu.org/licenses/gpl.html>.")
    print("This is free software: you are free to change and redistribute it.")
    print("There is NO WARRANTY, to the extent permitted by law.")
    print()
    print("Written by nsyhykui.")


def print_status():
    print("用法: dcli status <子命令>" if IS_ZH else "Usage: dcli status <subcommand>")
    print()
    print("子命令:" if IS_ZH else "Subcommands:")
    print("  %-14s %s" % ("hid", "列出被隐藏的应用" if IS_ZH else "List hidden apps"))
    print("  %-14s %s" % ("suspend", "列出被挂起的应用" if IS_ZH else "List suspended apps"))
    print("  %-14s %s" % ("block_uninstall",
                         "列出阻止卸载的应用" if IS_ZH else "List apps with uninstall blocked"))
    print("  %-14s %s" % ("permission", "查询应用权限" if IS_ZH else "Query app permissions"))
    print()
    print("示例:" if IS_ZH else "Examples:")
    print("  dcli status hid")
    print("  dcli status permission android.permission.CAMERA")
    print("  dcli status permission --package com.example.app")


def print_status_permission():
    print("用法: dcli status permission <子命令>"
          if IS_ZH else "Usage: dcli status permission <subcommand>")
    print()
    print("子命令:" if IS_ZH else "Subcommands:")
    print("  %-14s %s" % ("update",
                         "重新扫描所有应用并更新缓存"
                         if IS_ZH else "Rescan all apps and update cache"))
    print("  %-14s %s" % ("<perm>",
                         "列出拥有该权限的应用"
                         if IS_ZH else "List apps with this permission"))
    print("  %-14s %s" % ("--package <pkg>",
                         "列出该应用的所有权限"
                         if IS_ZH else "List all permissions of this app"))
    print("  %-14s %s" % ("<perm> --package <pkg>",
                         "查询某应用某权限的状态"
                         if IS_ZH else "Query one app's one permission"))
    print()
    print("示例:" if IS_ZH else "Examples:")
    print("  dcli status permission update")
    print("  dcli status permission android.permission.CAMERA")
    print("  dcli status permission --package com.example.app")
    print("  dcli status permission android.permission.CAMERA --package com.example.app")
