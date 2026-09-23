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
HKDF-SHA256 key derivation and AES-GCM encryption.

Derives an AES key from the shared secret (TOTP key), then encrypts
each message with a random 12-byte nonce.
"""

import secrets

try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes
    CRYPTO_OK = True
except ImportError:
    CRYPTO_OK = False

HKDF_SALT = b"\x00" * 32
HKDF_INFO = b"dhizuku-cli-v1"
AES_KEY_LEN = 32
NONCE_LEN = 12


def derive_aes_key(shared_secret):
    """从共享密钥派生 AES-256 密钥。"""
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=AES_KEY_LEN,
        salt=HKDF_SALT,
        info=HKDF_INFO,
    )
    return hkdf.derive(shared_secret.encode("utf-8"))


def encrypt_payload(aes_key, plaintext_bytes):
    """AES-GCM 加密，返回 nonce + ciphertext + tag。"""
    aesgcm = AESGCM(aes_key)
    nonce = secrets.token_bytes(NONCE_LEN)
    ct = aesgcm.encrypt(nonce, plaintext_bytes, None)
    return nonce + ct
