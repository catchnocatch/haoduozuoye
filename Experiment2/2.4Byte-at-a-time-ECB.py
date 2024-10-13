from base64 import b64decode
from Cryptodome import Random
from Cryptodome.Cipher import AES

ENCODED_STRING = b"""
Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK"""

SECRET_KEY = Random.new().read(16)

def apply_padding(input_string, message):
    padded_message = input_string + message
    block_size = 16
    length = len(padded_message)
    
    if length % block_size == 0:
        return padded_message

    padding_length = block_size - (length % block_size)
    padding_value = bytes([padding_length])
    padded_message += padding_value * padding_length

    return padded_message


def encryption_service(input_string):
    plaintext = b64decode(ENCODED_STRING)
    padded_plaintext = apply_padding(input_string, plaintext)

    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    ciphertext = cipher.encrypt(padded_plaintext)

    return ciphertext


def find_block_size():
    test_input = b"A"
    previous_length = 0
    
    while True:
        current_ciphertext = encryption_service(test_input)
        current_length = len(current_ciphertext)
        
        if previous_length != 0 and current_length > previous_length:
            return current_length - previous_length
        
        previous_length = current_length
        test_input += b"A"


def identify_mode(ciphertext):
    block_size = 16
    blocks = [ciphertext[i:i + block_size] for i in range(0, len(ciphertext), block_size)]
    unique_blocks = set(blocks)
    
    if len(blocks) > len(unique_blocks):
        return "ECB"
    return "not ECB"


def decrypt_ecb(block_size):
    common_chars = list(range(ord('a'), ord('z'))) + list(range(ord('A'), ord('Z'))) + [ord(' ')] + list(range(ord('0'), ord('9')))
    uncommon_chars = [i for i in range(256) if i not in common_chars]
    possible_bytes = bytes(common_chars + uncommon_chars)

    decrypted_message = b''
    check_length = block_size

    while True:
        prepend_length = block_size - 1 - (len(decrypted_message) % block_size)
        prepend_string = b'A' * prepend_length
        expected_block = encryption_service(prepend_string)[:check_length]

        found_byte = False
        for byte in possible_bytes:
            byte_value = bytes([byte])
            test_string = prepend_string + decrypted_message + byte_value
            produced_block = encryption_service(test_string)[:check_length]
            if expected_block == produced_block:
                decrypted_message += byte_value
                found_byte = True
                break

        if not found_byte:
            print(f'Possible end of plaintext: No matches found.')
            print(f"Decrypted Message: \n{decrypted_message.decode('ascii')}")
            return

        if len(decrypted_message) % block_size == 0:
            check_length += block_size


def main():
    block_size = find_block_size()
    print(f"Detected Block Size: {block_size}")

    repeated_input = b"A" * 50
    ciphertext = encryption_service(repeated_input)
    mode = identify_mode(ciphertext)
    print(f"Detected Mode of Encryption: {mode}")

    decrypt_ecb(block_size)


if __name__ == "__main__":
    main()