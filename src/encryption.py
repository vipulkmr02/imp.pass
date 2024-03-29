from base64 import b64decode
from base64 import b64encode

from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad


class AESCipher:
    def __init__(self, pwd: str, salt: bytes):
        # self.key = md5(pwd.encode('utf8')).digest()
        self.key = PBKDF2(pwd, salt, dkLen=16)

    def encrypt(self, data: str):
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return b64encode(
            iv + cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        )

    def decrypt(self, data: bytes):
        raw = b64decode(data)
        cipher = AES.new(self.key, AES.MODE_CBC, raw[:AES.block_size])
        return unpad(cipher.decrypt(raw[AES.block_size:]), AES.block_size)
