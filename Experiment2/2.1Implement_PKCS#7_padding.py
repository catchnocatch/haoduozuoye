def pkcs7_padding(data: bytes, block_size: int) -> bytes:
    # 计算当前数据长度
    padding_length = block_size - (len(data) % block_size)
    
    # 生成填充字节
    padding = bytes([padding_length] * padding_length)
    
    # 返回填充后的数据
    return data + padding

# 示例使用
message = b"YELLOW SUBMARINE"
block_size = 20
padded_message = pkcs7_padding(message, block_size)

print(padded_message)  # 输出: b'YELLOW SUBMARINE\x04\x04\x04\x04'