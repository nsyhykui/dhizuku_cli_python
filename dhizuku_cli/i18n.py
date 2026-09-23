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
Language strings for dhizuku-cli.

Detects language from $LANG environment variable.
"""

import os

_LANG = os.environ.get("LANG", "en").lower()
IS_ZH = _LANG.startswith("zh")


_S = {
    "en": {
        "usage": "Usage:",
        "opt_host": "  --host, -H <ip>      Server IP (default 127.0.0.1)",
        "opt_end": "  --                   Stop option parsing",
        "available": "Available commands:",
        "remote": "Remote examples:",
        "or_env": "  or env:",
        "or_file": "  or file:",
        "examples": "Examples:",
        "unknown_cmd": "Unknown command: %s",
        "see_help": "Run 'dcli help' for all commands",
        "usage_short": "Usage:  %s",
        "desc": "Desc:   %s",
        "example": "Example: %s",
        "err_no_key": "Error: no key found",
        "err_key_hint1": "Copy the key from the App to ~/.dcli_key",
        "err_key_hint2": "or set env DCLI_KEY",
        "err_no_crypto": "Error: cryptography library not installed",
        "err_crypto_hint": "Run: pip install cryptography",
        "err_timeout": "Error: connect %s timeout",
        "err_refused": "Error: %s not listening or server not started",
        "err_connect": "Error: cannot connect to %s (%s)",
        "err_generic": "Error: %s",
        "err_missing_arg": "Error: %s requires an argument",
        "err_unknown_opt": "Error: unknown option: %s",
    },
    "zh": {
        "usage": "用法:",
        "opt_host": "  --host, -H <ip>      服务端 IP（默认 127.0.0.1）",
        "opt_end": "  --                   停止解析后续选项",
        "available": "可用命令:",
        "remote": "远程连接示例:",
        "or_env": "  或环境变量:",
        "or_file": "  或写入文件:",
        "examples": "示例:",
        "unknown_cmd": "未知命令: %s",
        "see_help": "用 'dcli help' 查看所有命令",
        "usage_short": "用法:  %s",
        "desc": "说明:  %s",
        "example": "示例:  %s",
        "err_no_key": "错误: 未找到密钥",
        "err_key_hint1": "请从 App 复制密钥，写入 ~/.dcli_key",
        "err_key_hint2": "或设置环境变量 DCLI_KEY",
        "err_no_crypto": "错误: 未安装 cryptography 库",
        "err_crypto_hint": "运行: pip install cryptography",
        "err_timeout": "错误: 连接 %s 超时",
        "err_refused": "错误: %s 未监听或服务端未启动",
        "err_connect": "错误: 无法连接 %s (%s)",
        "err_generic": "错误: %s",
        "err_missing_arg": "错误: %s 后缺参数",
        "err_unknown_opt": "错误: 未知选项: %s",
    }
}


def t(key):
    """返回当前语言的字符串。"""
    return _S["zh" if IS_ZH else "en"].get(key, key)
