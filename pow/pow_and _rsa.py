import hashlib
from typing import List, Tuple

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey


# 生成RSA密钥对
def generate_keys() -> tuple[RSAPrivateKey, RSAPublicKey]:
    private_key: RSAPrivateKey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )
    public_key: RSAPublicKey = private_key.public_key()
    return private_key, public_key


# 生成符合特定PoW条件的消息
def create_pow_message(nickname, difficulty=4) -> tuple[bytes, int]:
    nonce = 0
    prefix = '0' * difficulty
    while True:
        message: bytes = f"{nickname}{nonce}".encode()
        hash_hex: str = hashlib.sha256(message).hexdigest()
        if hash_hex.startswith(prefix):
            return message, nonce
        nonce += 1


# 使用私钥签名消息
def sign_message(private_key: RSAPrivateKey, message: bytes) -> bytes:
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


# 使用公钥验证签名
def verify_signature(public_key: RSAPublicKey, message: bytes, signature: bytes) -> bool:
    try:
        public_key.verify(
            signature,
            message,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception as e:
        return False


# 主函数
def main():
    # 生成密钥
    private_key, public_key = generate_keys()

    # 创建符合PoW条件的消息
    nickname = "pi"
    message, nonce = create_pow_message(nickname)
    print(f"PoW Message: {message}, Nonce: {nonce}")

    # 签名消息
    signature = sign_message(private_key, message)

    # 验证签名
    is_valid = verify_signature(public_key, message, signature)
    print("Signature valid:", is_valid)


if __name__ == "__main__":
    main()
