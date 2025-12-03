from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import os

key = AESGCM.generate_key(bit_length=128)
aesgcm = AESGCM(key)
nonce = os.urandom(12)

ciphertext = aesgcm.encrypt(nonce, b"hola mundo", None)
print("cipher:", ciphertext)

plaintext = aesgcm.decrypt(nonce, ciphertext, None)
print("plain:", plaintext)
