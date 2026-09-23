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
TOTP generation (RFC 6238, HMAC-SHA1, 30s step, 6 digits).
"""

import hmac
import hashlib
import struct
import time

TIME_STEP = 30


def totp_generate(key, t_val=None):
    """
    生成 TOTP 验证码。

    key: 共享密钥（字符串）
    t_val: 时间计数器（默认取当前时间 / 30）
    返回: 6 位数字字符串
    """
    if t_val is None:
        t_val = int(time.time()) // TIME_STEP

    msg = struct.pack(">Q", t_val)
    h = hmac.new(key.encode("utf-8"), msg, hashlib.sha1).digest()
    off = h[-1] & 0x0F
    code = ((h[off] & 0x7F) << 24 |
            (h[off + 1] & 0xFF) << 16 |
            (h[off + 2] & 0xFF) << 8 |
            (h[off + 3] & 0xFF)) % 1000000
    return "%06d" % code
