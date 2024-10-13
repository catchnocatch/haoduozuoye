from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes
import urllib.parse

def parse_query_string(query_string):
    if not query_string:
        return {}
    pairs = query_string.split('&')
    result = {}
    for pair in pairs:
        if '=' not in pair:
            key = pair
            result[key] = ''
            continue
        key, value = pair.split('=', 1)
        result[key] = value
    return result

def create_user_data(email):
    # URL编码邮箱以防止特殊字符注入
    encoded_email = urllib.parse.quote(email, safe='')
    user_id = 10
    user_role = 'user'
    return f"email={encoded_email}&uid={user_id}&role={user_role}"

def generate_random_key():
    return get_random_bytes(16)  # AES-128

def encrypt_aes(key, plaintext):
    padding_length = 16 - (len(plaintext) % 16)
    padded_plaintext = plaintext.encode() + bytes([padding_length] * padding_length)
    
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(padded_plaintext)

def decrypt_aes(key, ciphertext):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    
    padding_length = decrypted[-1]
    return decrypted[:-padding_length].decode()

def generate_user_profile(email, key):
    user_data = create_user_data(email)
    return encrypt_aes(key, user_data)

def ecb_attack(encryption_function):
    prefix_length = AES.block_size - len("email=")
    suffix_length = AES.block_size - len("admin")
    
    # 构造一个邮箱以操控角色
    manipulated_email = 'x' * prefix_length + "admin" + (chr(suffix_length) * suffix_length)
    encrypted_admin = encryption_function(manipulated_email)
    
    normal_email = "foo@bar.com"
    encrypted_normal = encryption_function(normal_email)
    
    # 将encrypted_normal的前一个块与encrypted_admin的后一个块组合
    crafted_ciphertext = encrypted_normal[:AES.block_size] + encrypted_admin[AES.block_size:AES.block_size * 2]
    
    return crafted_ciphertext

def main():
    key = generate_random_key()
    
    # 加密oracle
    def encryption_function(email):
        return generate_user_profile(email, key)

    # 使用切割和粘贴攻击创建admin角色
    modified_ciphertext = ecb_attack(encryption_function)
    
    # 解密修改后的配置文件
    decrypted_profile = decrypt_aes(key, modified_ciphertext)
    
    # 解析修改后的配置文件
    parsed_profile = parse_query_string(decrypted_profile)
    
    print(parsed_profile)  # 应该显示角色为admin

if __name__ == "__main__":
    main()