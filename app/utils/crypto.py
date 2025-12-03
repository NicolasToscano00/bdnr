# Cifrado/descifrado AES-GCM.

# Generación de claves.

from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os
import base64
from typing import Dict

def gen_aes_key() -> bytes:
    return AESGCM.generate_key(bit_length=128)

def key_to_b64(key: bytes) -> str:
    return base64.b64encode(key).decode()

def b64_to_key(b64: str) -> bytes:
    return base64.b64decode(b64.encode())

def encrypt_bytes(plain: bytes, key: bytes) -> Dict[str,str]:
    aesgcm = AESGCM(key)
    nonce = os.urandom(12)
    ct = aesgcm.encrypt(nonce, plain, None)
    return {
        "nonce": base64.b64encode(nonce).decode(),
        "ciphertext": base64.b64encode(ct).decode()
    }

def decrypt_bytes(enc: Dict[str,str], key: bytes) -> bytes:
    aesgcm = AESGCM(key)
    nonce = base64.b64decode(enc["nonce"])
    ct = base64.b64decode(enc["ciphertext"])
    return aesgcm.decrypt(nonce, ct, None)
