from oracle import *
import sys

# 将十六进制字符串转换为整数列表
def hex_to_int_list(hex_string):
    return [int(hex_string[i:i+2], 16) for i in range(0, len(hex_string), 2)]

# 发送密文并获取返回值
def send_to_oracle(ctext, num_blocks):
    return Oracle_Send(ctext, num_blocks)

# 初始化参数
data = "9F0B13944841A832B2421B9EAF6D9836813EC9D944A5C8347A7CA69AA34D8DC0DF70E343C4000A2AE35874CE75E64C31"
ctext = hex_to_int_list(data)
print(f"Length of ctext: {len(ctext)}")

# 连接到 Oracle
Oracle_Connect()

# 初始化 IV 和中间值存储
iv = [0] * 16
middle1 = [0] * 16
middle2 = [0] * 16

# 逐字节破解循环
for l in range(16):
    for i in range(256):
        iv[15 - l] = i  # 设置 IV 的当前字节
        c = iv + ctext[16:32]  # 组合 IV 和密文的一部分
        if send_to_oracle(c, 2) == 49:  # 发送并检查返回值
            middle1[15 - l] = i ^ (l + 1)  # 计算中间值
            # 更新后续 IV 字节
            for j in range(15 - l, 16):
                iv[j] = middle1[j] ^ (l + 2)
            print(f"Found byte: {i}")
            break

print(f"Middle1 values: {middle1}")

# 断开 Oracle 连接
Oracle_Disconnect()

# 异或函数
def xor_lists(a, b):
    return [a[i] ^ b[i] for i in range(16)]

# 恢复明文
iv = ctext[:16]
m = xor_lists(iv, middle1) + xor_lists(ctext[16:32], middle2)

# 打印恢复的明文
for i in m:
    print(chr(i), end="")
print()  # 添加换行