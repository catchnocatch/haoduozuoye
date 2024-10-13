def fixed_xor(hex_str1, hex_str2):
    # Decode the hex strings into bytes
    bytes1 = bytes.fromhex(hex_str1)
    bytes2 = bytes.fromhex(hex_str2)
    
    # Ensure the buffers are of equal length
    if len(bytes1) != len(bytes2):
        raise ValueError("Buffers must be of equal length")
    
    # Perform XOR on each byte
    result_bytes = bytes(b1 ^ b2 for b1, b2 in zip(bytes1, bytes2))
    
    # Convert the result back to a hex string
    return result_bytes.hex()

# Test the function with the given example
hex_str1 = "1c0111001f010100061a024b53535009181c"
hex_str2 = "686974207468652062756c6c277320657965"

# Expected output: "746865206b696420646f6e277420706c6179"
print(fixed_xor(hex_str1, hex_str2))
