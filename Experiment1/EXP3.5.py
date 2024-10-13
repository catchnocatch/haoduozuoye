def xor_with_repeating_key(repeating_key, input_text):
    key_length = len(repeating_key)
    encrypted_chars = []
    
    for index, char in enumerate(input_text):
        key_index = index % key_length
        # Perform XOR operation and append the result
        encrypted_char = chr(ord(repeating_key[key_index]) ^ ord(char))
        encrypted_chars.append(encrypted_char)
    
    return ''.join(encrypted_chars)

def main():
    plaintext = "IIIAADSADIZXCLZJL"
    key = 'ICE'
    
    # XOR the plaintext with the key
    encrypted_text = xor_with_repeating_key(key, plaintext)
    
    # Convert the result to hexadecimal representation
    hex_output = encrypted_text.encode('utf-8').hex()
    
    print(hex_output)

if __name__ == '__main__':
    main()