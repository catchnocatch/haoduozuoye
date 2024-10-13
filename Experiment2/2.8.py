from Cryptodome.Random import get_random_bytes
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
# globals
AES_BLOCK_SIZE = 16

def xor_several(*args: bytes) -> bytes:
    """Perform XOR operation on multiple byte strings.
    
    Args:
        *args: One or more byte strings of the same length.

    Returns:
        bytes: The result of the XOR operation.
    """
    # 确保所有输入的字节串长度相同
    length = len(args[0])
    for arg in args:
        if len(arg) != length:
            raise ValueError("All input byte strings must have the same length.")
    
    result = bytearray(length)  # 使用 bytearray 以便可变
    for i in range(length):
        xor_result = 0
        for arg in args:
            xor_result ^= arg[i]  # 对每个字节进行异或操作
        result[i] = xor_result

    return bytes(result)  # 返回不可变的 bytes 对象

def aes_cbc_encrypt(plaintext: bytes, key: bytes, nonce: bytes, add_padding: bool = True) -> bytes:
    """使用 AES CBC 模式加密明文。

    Args:
        plaintext (bytes): 要加密的明文。
        key (bytes): 16, 24 或 32 字节的 AES 密钥。
        nonce (bytes): 16 字节的初始化向量（IV）。
        add_padding (bool): 是否在加密前添加填充。

    Returns:
        bytes: 加密后的密文。
    """
    # 确保密钥长度为 16, 24 或 32 字节
    if len(key) not in {16, 24, 32}:
        raise ValueError("密钥长度必须为 16, 24 或 32 字节。")

    # 创建 AES 加密器
    cipher = AES.new(key, AES.MODE_CBC, nonce)

    # 添加填充
    if add_padding:
        plaintext = pad(plaintext, AES.block_size)

    # 进行加密
    ciphertext = cipher.encrypt(plaintext)

    return ciphertext

def aes_cbc_decrypt(ciphertext: bytes, key: bytes, nonce: bytes, remove_padding: bool = True) -> bytes:
    """使用 AES CBC 模式解密密文。

    Args:
        ciphertext (bytes): 要解密的密文。
        key (bytes): 16, 24 或 32 字节的 AES 密钥。
        nonce (bytes): 16 字节的初始化向量（IV）。
        remove_padding (bool): 是否在解密后去除填充。

    Returns:
        bytes: 解密后的明文。
    """
    # 确保密钥长度为 16, 24 或 32 字节
    if len(key) not in {16, 24, 32}:
        raise ValueError("密钥长度必须为 16, 24 或 32 字节。")

    # 创建 AES 解密器
    cipher = AES.new(key, AES.MODE_CBC, nonce)

    # 进行解密
    decrypted_data = cipher.decrypt(ciphertext)

    # 去除填充
    if remove_padding:
        decrypted_data = unpad(decrypted_data, AES.block_size)

    return decrypted_data


class Oracle:
    def __init__(self):
        self.key = get_random_bytes(AES_BLOCK_SIZE)
        self.nonce = get_random_bytes(AES_BLOCK_SIZE)

    def encode(self, plaintext: bytes) -> bytes:
        prefix = b"comment1=cooking%20MCs;userdata="
        suffix = b";comment2=%20like%20a%20pound%20of%20bacon"

        # quote out ";" and "="
        plaintext = plaintext.replace(b";", b"").replace(b"=", b"")
        plaintext = prefix + plaintext + suffix

        # encrypt and return
        ciphertext = aes_cbc_encrypt(plaintext, key=self.key, nonce=self.nonce, add_padding=True)
        return ciphertext

    def parse(self, ciphertext: bytes) -> bool:
        decrypted = aes_cbc_decrypt(ciphertext, key=self.key, nonce=self.nonce, remove_padding=True)
        print("DECRYPT: ",decrypted)
        return b';admin=true;' in decrypted

def find_prefix_length(oracle: Oracle, block_size: int) -> int:
    full_block_len = 0
    c1 = oracle.encode(b'')
    c2 = oracle.encode(b'A')
    for i in range(0, len(c2), block_size):
        if c1[i:i+block_size] != c2[i:i+block_size]:
            full_block_len = i
            break

    block_idx = slice(full_block_len, full_block_len + block_size)
    prev_block = c1[block_idx]
    pad_len = 0
    for i in range(1, block_size + 2):
        new_block = oracle.encode(b'A' * i)[block_idx]
        if new_block == prev_block:
            pad_len = i - 1
            break
        prev_block = new_block

    prefix_len = full_block_len + block_size - pad_len
    return prefix_len

def generate_result(oracle: Oracle, prefix_len: int):
    if prefix_len % AES_BLOCK_SIZE != 0:
        pad_len = AES_BLOCK_SIZE - (prefix_len % AES_BLOCK_SIZE)
    else:
        pad_len = 0

    prev_blocks_len = prefix_len + pad_len
    known_plaintext = b'B' * pad_len + b'A' * 2 * AES_BLOCK_SIZE
    ciphertext = oracle.encode(known_plaintext)

    target = b';admin=true'
    target = b'A' * (AES_BLOCK_SIZE - len(target)) + target

    c1_original = ciphertext[prev_blocks_len: prev_blocks_len + AES_BLOCK_SIZE]
    p2_original = b'A' * AES_BLOCK_SIZE
    c1_modified = xor_several(c1_original, p2_original, target)

    result = ciphertext[:prev_blocks_len]
    result += c1_modified
    result += ciphertext[prev_blocks_len + AES_BLOCK_SIZE:]
    print("**************************")
    print(result[prefix_len:prefix_len+AES_BLOCK_SIZE])
    print("**************************")
    print(xor_several(result[prefix_len:prefix_len+AES_BLOCK_SIZE],c1_original,p2_original))
    print("**************************")
    return result

def main():
    oracle = Oracle()
    prefix_len = find_prefix_length(oracle, AES_BLOCK_SIZE)
    print(f'{prefix_len=}')
    result = generate_result(oracle, prefix_len=prefix_len)
    find_admin = oracle.parse(result)
    print(f'{find_admin=}')

if __name__ == '__main__':
    main()