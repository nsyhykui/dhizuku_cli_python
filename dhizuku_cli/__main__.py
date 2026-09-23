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
Entry point for dhizuku-cli.

Usage:
    dcli [--host <ip>] help [command]
    dcli [--host <ip>] <command> [args]

Or:
    python -m dhizuku_cli <args>
"""

import sys

from .client import main

if __name__ == "__main__":
    sys.exit(main())
