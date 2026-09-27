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

from .i18n import t, err
from .crypto import CRYPTO_OK
from .config import load_key, load_host
from .args import parse as parse_args
from .net import send_command, query_server_version
from .output import print_response
from . import help as help_mod


TIMEOUT_NORMAL = 65


def main():
    if not CRYPTO_OK:
        err(t("err_no_crypto"))
        err(t("err_crypto_hint"))
        return 1

    host_arg, is_version, args = parse_args(sys.argv[1:])

    # --version / -V
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

    # status 本地帮助
    if args[0] == "status":
        if len(args) == 1:
            help_mod.print_status()
            return 0
        if len(args) == 2 and args[1] == "permission":
            help_mod.print_status_permission()
            return 0

    cmd_line = " ".join(args)

    key = load_key()
    if not key:
        err(t("err_no_key"))
        err(t("err_key_hint1"))
        err(t("err_key_hint2"))
        return 1

    host = load_host(host_arg)

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
