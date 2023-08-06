import rsa
from .sym_enc_base import SymEncBase


class SymRsa(SymEncBase):
    def __init__(self, pubkey: str, privkey: str,
                 pub_format: str = "PEM", priv_format: str = "PEM") -> None:
        self.pubkey = rsa.PublicKey.load_pkcs1(pubkey, pub_format)
        self.privkey = rsa.PrivateKey.load_pkcs1(privkey, priv_format)

    def encode(self, data: bytes) -> bytearray:
        return rsa.encrypt(data, self.pubkey)

    def decode(self, data: bytes) -> bytearray:
        return rsa.decrypt(data, self.privkey)

