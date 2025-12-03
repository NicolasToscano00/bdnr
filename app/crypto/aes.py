import os
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from app.config import settings
import base64

MASTER_KEY = bytes.fromhex(settings.AES_MASTER_KEY)

def encrypt_sensitive(data: str) -> str:
    aesgcm = AESGCM(MASTER_KEY)
    nonce = os.urandom(12)
    encrypted = aesgcm.encrypt(nonce, data.encode(), None)
    return base64.b64encode(nonce + encrypted).decode()

def decrypt_sensitive(encoded: str) -> str:
    raw = base64.b64decode(encoded.encode())
    nonce, ciphertext = raw[:12], raw[12:]
    aesgcm = AESGCM(MASTER_KEY)
    decrypted = aesgcm.decrypt(nonce, ciphertext, None)
    return decrypted.decode()
