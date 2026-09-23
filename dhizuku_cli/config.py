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
Configuration loading for dhizuku-cli.

Priority (highest to lowest):
  1. Command-line argument
  2. Environment variable
  3. File in current dir
  4. File in $HOME
  5. Built-in default
"""

import os

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 12345
KEY_FILE = ".dcli_key"
HOST_FILE = ".dcli_host"


def read_field(fname, envname):
    """
    读取配置字段。

    优先级：环境变量 > 当前目录文件 > HOME 文件
    都找不到返回 None。
    """
    env = os.environ.get(envname, "").strip()
    if env:
        return env

    paths = [fname]
    home = os.environ.get("HOME")
    if home:
        paths.append(os.path.join(home, fname))

    for p in paths:
        if os.path.exists(p):
            with open(p, "r") as f:
                v = f.read().strip()
            if v:
                return v

    return None


def load_key():
    """读取 TOTP 密钥。"""
    return read_field(KEY_FILE, "DCLI_KEY")


def load_host(cli_host=None):
    """
    读取服务端地址。

    cli_host 是命令行参数（优先级最高），
    为 None 时回退到环境变量 / 文件 / 默认值。
    """
    if cli_host:
        return cli_host
    return read_field(HOST_FILE, "DCLI_HOST") or DEFAULT_HOST
