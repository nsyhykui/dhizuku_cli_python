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
服务端响应按行分流到 stdout / stderr。
"""

from .i18n import warn, err


_ERROR_PREFIXES = ("Error:", "Failed:", "Denied",
                   "timeout", "crypto: denied", "totp: denied", "uid: denied")


def print_response(reply):
    """
    按行分流。返回 True 表示有错误行（退出码应为 1）。
    """
    has_error = False

    for line in reply.split("\n"):
        if line.startswith("Warning:"):
            warn(line)
        elif any(line == p or line.startswith(p) for p in _ERROR_PREFIXES):
            err(line)
            has_error = True
        elif line == "Success":
            print("Success")
        elif line.startswith("Success "):
            print(line[len("Success "):])
        else:
            print(line)

    return has_error
