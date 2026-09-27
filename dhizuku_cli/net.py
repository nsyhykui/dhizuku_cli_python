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
TCP 通信：发送加密命令，接收响应。
"""

import os
import socket
import base64

from .totp import totp_generate
from .crypto import derive_aes_key, encrypt_payload
from .config import DEFAULT_PORT

RECV_BUF = 4096


def send_command(host, cmd_line, key, timeout_sec):
    """
    连接服务端，发送命令，读到 EOF 为止。
    返回完整响应字符串（去掉末尾换行）。
    """
    aes_key = derive_aes_key(key)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout_sec)
    try:
        s.connect((host, DEFAULT_PORT))

        local_ip, local_port = s.getsockname()[:2]
        uid = os.getuid()
        code = totp_generate(key)
        plaintext = "%d %s %d %s %s" % (uid, local_ip, local_port, code, cmd_line)
        encrypted = encrypt_payload(aes_key, plaintext.encode("utf-8"))
        s.sendall(base64.b64encode(encrypted) + b"\n")

        chunks = []
        while True:
            chunk = s.recv(RECV_BUF)
            if not chunk:
                break
            chunks.append(chunk)
        return b"".join(chunks).decode("utf-8").rstrip("\n")
    finally:
        s.close()


def query_server_version(host, key, timeout_sec=3):
    """
    查询服务端版本。
    返回：版本号字符串 / "unknown" / None（连不上）
    """
    try:
        result = send_command(host, "#$%version", key, timeout_sec)
    except Exception:
        return None

    if result.startswith("Success "):
        return result[len("Success "):].strip()
    if result.startswith("Unknown"):
        return "unknown"
    return None
