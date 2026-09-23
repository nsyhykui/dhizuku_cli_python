# -*- coding: utf-8 -*-
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

"""
Main client logic: argument parsing, TCP communication, command dispatch.

Protocol: <UID> <IP> <PORT> <TOTP> <CMD> [ARG]
The whole message is encrypted with AES-GCM and Base64-encoded.
"""

import sys
import os
import socket
import base64

from .i18n import t, IS_ZH
from .totp import totp_generate
from .crypto import CRYPTO_OK, derive_aes_key, encrypt_payload
from .config import (
    DEFAULT_PORT,
    load_key,
    load_host,
)

SERVER_TIMEOUT = 65
RECV_BUF = 4096


# ---- 命令表 ----
HELP = {
    "ping": {
        "desc": "测试连接是否正常" if IS_ZH else "Test connection",
        "usage": "dcli ping",
        "example": "dcli ping",
    },
    "lock_now": {
        "desc": "立即锁屏" if IS_ZH else "Lock screen now",
        "usage": "dcli lock_now",
        "example": "dcli lock_now",
    },
    "hide": {
        "desc": "隐藏指定应用" if IS_ZH else "Hide app",
        "usage": "dcli hide <package>",
        "example": "dcli hide com.example.app",
    },
    "unhide": {
        "desc": "取消隐藏指定应用" if IS_ZH else "Unhide app",
        "usage": "dcli unhide <package>",
        "example": "dcli unhide com.example.app",
    },
    "suspend": {
        "desc": "挂起指定应用" if IS_ZH else "Suspend app",
        "usage": "dcli suspend <package>",
        "example": "dcli suspend com.example.app",
    },
    "resume": {
        "desc": "恢复挂起指定应用" if IS_ZH else "Resume app",
        "usage": "dcli resume <package>",
        "example": "dcli resume com.example.app",
    },
    "block_uninstall": {
        "desc": "阻止卸载指定应用" if IS_ZH else "Block uninstall",
        "usage": "dcli block_uninstall <package>",
        "example": "dcli block_uninstall com.example.app",
    },
    "unblock_uninstall": {
        "desc": "允许卸载指定应用" if IS_ZH else "Unblock uninstall",
        "usage": "dcli unblock_uninstall <package>",
        "example": "dcli unblock_uninstall com.example.app",
    },
}


def print_global_help():
    print("dcli - " + ("DO Server 命令行客户端" if IS_ZH else "DO Server CLI client"))
    print()
    print(t("usage"))
    print("  dcli [--host <ip>] help [command]")
    print("  dcli [--host <ip>] <command> [args]")
    print()
    print("Options:" if not IS_ZH else "选项:")
    print(t("opt_host"))
    print(t("opt_end"))
    print()
    print(t("available"))
    for name in sorted(HELP.keys()):
        print("  %-18s %s" % (name, HELP[name]["desc"]))
    print()
    print(t("remote"))
    print("  dcli --host 192.168.1.100 ping")
    print(t("or_env") + " export DCLI_HOST=192.168.1.100")
    print(t("or_file") + " echo 192.168.1.100 > ~/.dcli_host")
    print()
    print(t("examples"))
    print("  dcli ping")
    print("  dcli lock_now")
    print("  dcli hide com.example.app")


def print_command_help(cmd):
    if cmd not in HELP:
        print(t("unknown_cmd") % cmd)
        print(t("see_help"))
        sys.exit(1)
    info = HELP[cmd]
    print(t("usage_short") % info["usage"])
    print(t("desc") % info["desc"])
    print(t("example") % info["example"])


def parse_args(args):
    """
    解析命令行参数，返回 (host, remaining_args)。

    支持：
      --host <ip> / -H <ip> / --host=<ip>
      --                    停止解析后续选项
      --help / -h           保留在 remaining 里由 main 处理
    """
    host = None
    remaining = []
    stop = False
    i = 0

    while i < len(args):
        a = args[i]

        if stop:
            remaining.append(a)
            i += 1
            continue

        if a == "--":
            stop = True
            i += 1
            continue

        if a in ("--host", "-H"):
            if i + 1 >= len(args):
                print(t("err_missing_arg") % a, file=sys.stderr)
                sys.exit(2)
            host = args[i + 1]
            i += 2
            continue

        if a.startswith("--host="):
            host = a[len("--host="):]
            i += 1
            continue

        if a in ("--help", "-h"):
            remaining.append(a)
            i += 1
            continue

        if a.startswith("-") and a != "-":
            print(t("err_unknown_opt") % a, file=sys.stderr)
            sys.exit(2)

        remaining.append(a)
        i += 1

    return host, remaining


def send_command(host, port, cmd_line, key):
    """
    一次连接，服务端内部阻塞等待授权，最长 60 秒。
    返回服务端响应字符串。
    """
    aes_key = derive_aes_key(key)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(SERVER_TIMEOUT)
    try:
        s.connect((host, port))

        local_ip, local_port = s.getsockname()[:2]
        uid = os.getuid()
        code = totp_generate(key)

        plaintext = "%d %s %d %s %s" % (uid, local_ip, local_port, code, cmd_line)
        encrypted = encrypt_payload(aes_key, plaintext.encode("utf-8"))
        s.sendall(base64.b64encode(encrypted) + b"\n")

        data = b""
        while not data.endswith(b"\n"):
            chunk = s.recv(RECV_BUF)
            if not chunk:
                break
            data += chunk

        return data.decode("utf-8").strip()
    finally:
        s.close()


def main():
    if not CRYPTO_OK:
        print(t("err_no_crypto"), file=sys.stderr)
        print(t("err_crypto_hint"), file=sys.stderr)
        return 1

    host_arg, args = parse_args(sys.argv[1:])

    # 无参数 → 全局帮助
    if not args:
        print_global_help()
        return 0

    # dcli help / dcli --help
    if args[0] in ("help", "--help"):
        if len(args) < 2:
            print_global_help()
        else:
            print_command_help(args[1])
        return 0

    # dcli <cmd> --help / dcli <cmd> -h
    if len(args) >= 2 and args[0] in HELP and args[1] in ("--help", "-h"):
        print_command_help(args[0])
        return 0

    cmd_line = " ".join(args)

    key = load_key()
    if not key:
        print(t("err_no_key"), file=sys.stderr)
        print(t("err_key_hint1"), file=sys.stderr)
        print(t("err_key_hint2"), file=sys.stderr)
        return 1

    host = load_host(host_arg)

    try:
        result = send_command(host, DEFAULT_PORT, cmd_line, key)
    except socket.timeout:
        print(t("err_timeout") % host, file=sys.stderr)
        return 1
    except ConnectionRefusedError:
        print(t("err_refused") % host, file=sys.stderr)
        return 1
    except OSError as e:
        print(t("err_connect") % (host, e), file=sys.stderr)
        return 1
    except Exception as e:
        print(t("err_generic") % e, file=sys.stderr)
        return 1

    if result == "Success":
        print("Success")
        return 0
    if result.startswith("Success "):
        print(result[len("Success "):])
        return 0

    print(result)
    return 1
