import random
from Cryptodome.Cipher import AES
from Cryptodome.Random import get_random_bytes

# Constants
BLOCK_SIZE = 16

def pad_pkcs7(data: bytes, block_size: int) -> bytes:

    padding_length = block_size - (len(data) % block_size)
    padding = bytes([padding_length] * padding_length)
    return data + padding

def xor_byte_strings(first_bytes: bytes, second_bytes: bytes) -> bytes:

    return bytes(a ^ b for a, b in zip(first_bytes, second_bytes))

def encrypt_aes_cbc(plaintext: bytes, key: bytes, iv: bytes) -> bytes:

    if len(iv) != BLOCK_SIZE:
        raise ValueError(f"IV must be of size {BLOCK_SIZE}")
    if len(plaintext) % BLOCK_SIZE != 0:
        raise ValueError(f"Plaintext must have length multiple of block size")

    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = bytes()
    previous_block = iv

    for i in range(0, len(plaintext), BLOCK_SIZE):
        block = plaintext[i:i + BLOCK_SIZE]
        block = xor_byte_strings(block, previous_block)
        encrypted_block = cipher.encrypt(block)
        ciphertext += encrypted_block
        previous_block = encrypted_block

    return ciphertext

def generate_aes_key() -> bytes:

    return get_random_bytes(BLOCK_SIZE)

def encryption_service(plaintext: bytes) -> tuple[bytes, str]:

    key = generate_aes_key()
    
    # Add random padding
    pre_padding = get_random_bytes(random.randint(5, 10))
    post_padding = get_random_bytes(random.randint(5, 10))
    plaintext = pre_padding + plaintext + post_padding
    padded_plaintext = pad_pkcs7(plaintext, BLOCK_SIZE)

    if random.random() < 0.5:
        # Use ECB mode
        cipher = AES.new(key, AES.MODE_ECB)
        ciphertext = cipher.encrypt(padded_plaintext)
        return ciphertext, 'ECB'
    else:
        # Use CBC mode
        iv = get_random_bytes(BLOCK_SIZE)
        ciphertext = encrypt_aes_cbc(padded_plaintext, key, iv)
        return ciphertext, 'CBC'

def identify_encryption_mode(cipher: bytes) -> str:

    blocks = [cipher[i:i + BLOCK_SIZE] for i in range(0, len(cipher), BLOCK_SIZE)]
    repetitions = len(blocks) - len(set(blocks))
    return 'ECB' if repetitions > 0 else 'CBC'

def test_mode_detection() -> bool:

    plaintext = bytes(BLOCK_SIZE) * 5
    cipher, actual_mode = encryption_service(plaintext)
    detected_mode = identify_encryption_mode(cipher)
    return actual_mode == detected_mode

def main():
    """Main function to run tests."""
    for _ in range(1000):
        if not test_mode_detection():
            print('Test Failed!')
            return
    print('Test Passed!')

if __name__ == '__main__':
    main()