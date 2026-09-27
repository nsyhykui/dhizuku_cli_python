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
命令行参数解析。只解析前导选项。
"""

import sys

from .i18n import t, err


def parse(args):
    """
    只解析前导选项。遇到第一个非选项后，剩余全部当位置参数。
    返回 (host, is_version, remaining)
    """
    host = None
    is_version = False
    remaining = []
    parsing_options = True

    i = 0
    while i < len(args):
        a = args[i]

        if not parsing_options:
            remaining.append(a)
            i += 1
            continue

        # 单独的 "-" 当位置参数
        if not a.startswith("-") or a == "-":
            parsing_options = False
            remaining.append(a)
            i += 1
            continue

        if a == "--":
            parsing_options = False
            i += 1
            continue

        if a in ("--host", "-H"):
            if i + 1 >= len(args):
                err(t("err_missing_arg") % a)
                sys.exit(2)
            host = args[i + 1]
            i += 2
            continue

        if a.startswith("--host="):
            host = a[len("--host="):]
            i += 1
            continue

        if a in ("--version", "-V"):
            is_version = True
            i += 1
            continue

        if a in ("--help", "-h"):
            remaining.append(a)
            i += 1
            continue

        err(t("err_unknown_opt") % a)
        sys.exit(2)

    return host, is_version, remaining
