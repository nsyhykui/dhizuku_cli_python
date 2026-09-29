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
    "ping": {"desc": "测试连接" if IS_ZH else "Test connection"},
    "lock_now": {"desc": "立即锁屏" if IS_ZH else "Lock screen now"},
    "hide": {"desc": "隐藏应用" if IS_ZH else "Hide app"},
    "unhide": {"desc": "取消隐藏" if IS_ZH else "Unhide app"},
    "suspend": {"desc": "挂起应用" if IS_ZH else "Suspend app"},
    "resume": {"desc": "恢复挂起" if IS_ZH else "Resume app"},
    "block_uninstall": {"desc": "阻止卸载" if IS_ZH else "Block uninstall"},
    "unblock_uninstall": {"desc": "允许卸载" if IS_ZH else "Unblock uninstall"},
    "status": {"desc": "显示服务端状态" if IS_ZH else "Show server status"},
    "list": {"desc": "列出隐藏/挂起/阻止卸载的应用"
                     if IS_ZH else "List hidden/suspended/blocked apps"},
    "pm": {"desc": "包管理操作（pm 风格）"
                   if IS_ZH else "Package manager operations (pm-style)"},
    "cache": {"desc": "缓存操作" if IS_ZH else "Cache operations"},
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
    print("  dcli list hidden")
    print("  dcli pm list packages -3")
    print("  dcli pm list permissions android.permission.CAMERA")


def print_command(cmd):
    if cmd == "status":
        print_status()
        return
    if cmd == "list":
        print_list()
        return
    if cmd == "pm":
        print_pm()
        return
    if cmd == "cache":
        print_cache()
        return

    if cmd not in HELP:
        err(t("unknown_cmd") % cmd)
        sys.exit(1)
    print(t("desc") % HELP[cmd]["desc"])


def print_version(server_version):
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
    print("用法: dcli status" if IS_ZH else "Usage: dcli status")
    print("显示服务端运行状态、IP、端口和模式。"
          if IS_ZH else "Show server running status, IP, port and mode.")


def print_list():
    print("用法: dcli list <子命令>" if IS_ZH else "Usage: dcli list <subcommand>")
    print()
    print("子命令:" if IS_ZH else "Subcommands:")
    print("  %-12s %s" % ("hidden",
                         "列出被隐藏的应用" if IS_ZH else "List hidden apps"))
    print("  %-12s %s" % ("suspended",
                         "列出被挂起的应用" if IS_ZH else "List suspended apps"))
    print("  %-12s %s" % ("blocked",
                         "列出阻止卸载的应用"
                         if IS_ZH else "List apps with uninstall blocked"))


def print_pm():
    print("用法: dcli pm <子命令>" if IS_ZH else "Usage: dcli pm <subcommand>")
    print()
    print("子命令:" if IS_ZH else "Subcommands:")
    print("  %-12s %s" % ("list packages",
                         "列出应用（同 pm list packages）"
                         if IS_ZH else "List packages (same as pm list packages)"))
    print("  %-12s %s" % ("list permissions",
                         "查询应用权限状态"
                         if IS_ZH else "Query app permission state"))
    print("  %-12s %s" % ("grant",
                         "授予运行时权限"
                         if IS_ZH else "Grant a runtime permission"))
    print("  %-12s %s" % ("revoke",
                         "拒绝运行时权限"
                         if IS_ZH else "Revoke a runtime permission"))
    print("  %-12s %s" % ("reset",
                         "恢复权限到默认状态"
                         if IS_ZH else "Reset a permission to default"))
    print()
    print("示例:" if IS_ZH else "Examples:")
    print("  dcli pm list packages -3")
    print("  dcli pm list packages -f wechat")
    print("  dcli pm list permissions android.permission.CAMERA")
    print("  dcli pm grant com.example.app android.permission.CAMERA")
    print("  dcli pm revoke com.example.app android.permission.CAMERA")
    print("  dcli pm reset com.example.app android.permission.CAMERA")


def print_cache():
    print("用法: dcli cache <子命令>" if IS_ZH else "Usage: dcli cache <subcommand>")
    print()
    print("子命令:" if IS_ZH else "Subcommands:")
    print("  %-12s %s" % ("update",
                         "重新扫描所有应用并更新缓存"
                         if IS_ZH else "Rescan all apps and update cache"))
