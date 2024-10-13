import base64  
from Cryptodome.Cipher import AES  

# 逆向解密过程：
# 1.进行CBC（ECB）解密（解密后判断有无填充）
# 2.与前一个密文异或出明文

# 检查是否使用了 PKCS#7 填充
def is_pkcs7_padded(data: bytes) -> bool:
    padding_length = data[-1]
    padding = data[-padding_length:]
    return all(byte == padding_length for byte in padding)

# 去除 PKCS#7 填充
def remove_pkcs7_padding(data: bytes) -> bytes:
    if is_pkcs7_padded(data):
        padding_length = data[-1]
        return data[:-padding_length]
    return data

# ECB 模式解密
def decrypt_aes_ecb(ciphertext: bytes, aes_key: bytes) -> bytes:
    cipher = AES.new(aes_key, AES.MODE_ECB)
    decrypted_data = cipher.decrypt(ciphertext)
    return remove_pkcs7_padding(decrypted_data)

# CBC 模式解密
def decrypt_aes_cbc(ciphertext: bytes, iv: bytes, aes_key: bytes) -> bytes:
    previous_block = iv
    block_size = len(aes_key)
    plaintext = b''

    for i in range(0, len(ciphertext), block_size):
        decrypted_block = decrypt_aes_ecb(ciphertext[i:i + block_size], aes_key)
        # XOR 当前解密块和前一个密文块
        plaintext_block = bytes(b1 ^ b2 for b1, b2 in zip(decrypted_block, previous_block))
        plaintext += plaintext_block
        previous_block = ciphertext[i:i + block_size]

    return plaintext

def main():
    try:
        # 读取文件内容，假定内容为 Base64 编码
        with open("2-2.txt", "r") as file:
            base64_data = file.read()
        
        aes_key = b"YELLOW SUBMARINE"
        ciphertext_bytes = base64.b64decode(base64_data)
        iv = b'\x00' * AES.block_size  # 使用全零的 IV
        plaintext = decrypt_aes_cbc(ciphertext_bytes, iv, aes_key)
        print(plaintext.decode("utf-8"))
    except Exception as error:
        print(f"Error: {error}")

if __name__ == "__main__":
    main()