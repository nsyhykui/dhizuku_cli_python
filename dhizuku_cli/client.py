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
客户端主流程。
"""

import sys
import socket

from .i18n import t, IS_ZH, err
from .crypto import CRYPTO_OK
from .config import DEFAULT_PORT, load_key, load_host
from .args import parse as parse_args
from .net import send_command, query_server_version
from .output import print_response
from . import help as help_mod


TIMEOUT_NORMAL = 65
TIMEOUT_VERSION = 3


def do_status(host, key):
    """本地处理 dcli status：用 ping 包装。"""
    try:
        reply = send_command(host, "ping", key, TIMEOUT_VERSION)
    except Exception:
        reply = None

    if reply is None:
        state = "未运行" if IS_ZH else "Not running"
    elif reply == "Success":
        state = "正在运行（已授权）" if IS_ZH else "Running (authorized)"
    elif reply == "uid: denied":
        state = "正在运行（未授权）" if IS_ZH else "Running (unauthorized)"
    elif reply == "totp: denied":
        state = "正在运行（TOTP 验证失败）" if IS_ZH else "Running (TOTP failed)"
    elif reply == "crypto: denied":
        state = "正在运行（解密失败）" if IS_ZH else "Running (crypto failed)"
    else:
        state = "正在运行（状态未知）" if IS_ZH else "Running (unknown)"

    print("%s: %s" % ("服务端状态" if IS_ZH else "Server status", state))
    print("%s: %s" % ("服务端IP" if IS_ZH else "Server IP", host))
    print("%s: %d" % ("服务端端口" if IS_ZH else "Server port", DEFAULT_PORT))
    print("%s: TCP" % ("模式" if IS_ZH else "Mode"))
    return 0


def main():
    if not CRYPTO_OK:
        err(t("err_no_crypto"))
        err(t("err_crypto_hint"))
        return 1

    host_arg, is_version, args = parse_args(sys.argv[1:])

    # --version
    if is_version:
        key = load_key()
        if not key:
            help_mod.print_version(None)
            return 0
        host = load_host(host_arg)
        sv = query_server_version(host, key)
        help_mod.print_version(sv)
        return 0

    # 无参数 → 全局帮助
    if not args:
        help_mod.print_global()
        return 0

    # help / --help / -h
    if args[0] in ("help", "--help", "-h"):
        if len(args) < 2:
            help_mod.print_global()
        else:
            help_mod.print_command(args[1])
        return 0

    # <cmd> --help / <cmd> -h
    if len(args) >= 2 and args[0] in help_mod.HELP and args[1] in ("--help", "-h"):
        help_mod.print_command(args[0])
        return 0

    # 顶层命令无子命令 → 本地帮助
    if len(args) == 1:
        if args[0] == "list":
            help_mod.print_list()
            return 0
        if args[0] == "pm":
            help_mod.print_pm()
            return 0
        if args[0] == "cache":
            help_mod.print_cache()
            return 0

    # 读密钥
    key = load_key()
    if not key:
        err(t("err_no_key"))
        err(t("err_key_hint1"))
        err(t("err_key_hint2"))
        return 1

    host = load_host(host_arg)

    # dcli status → 本地处理
    if len(args) == 1 and args[0] == "status":
        return do_status(host, key)

    # 发送
    cmd_line = " ".join(args)
    try:
        result = send_command(host, cmd_line, key, TIMEOUT_NORMAL)
    except socket.timeout:
        err(t("err_timeout") % host)
        return 1
    except ConnectionRefusedError:
        err(t("err_refused") % host)
        return 1
    except OSError as e:
        err(t("err_connect") % (host, e))
        return 1
    except Exception as e:
        err(t("err_generic") % e)
        return 1

    return 1 if print_response(result) else 0
