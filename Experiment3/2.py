from egcd import mod_inverse
from sympy import randprime

def generate_random_prime(lower, upper):
    # 生成指定范围内的随机素数
    return randprime(lower, upper)

# 示例：生成一个范围内的随机素数
lower_bound = 2**2  # 下限
upper_bound = 2**10  # 上限
p = 0
q = 0
# 确保 p 和 q 不相等
while p == q:
    p = generate_random_prime(lower_bound, upper_bound)
    q = generate_random_prime(lower_bound, upper_bound)
n = p * q
print(f"生成的随机数: p = {p}, q = {q}, n = {n}")

def encrypt(m, e, n):
    return pow(m, e, n)  # 使用 pow 函数进行模运算

def decrypt(c, d, n):
    return pow(c, d, n)

# 计算 φ(n)
et = (p - 1) * (q - 1)

# 选择公钥 e
e = 3

# 计算私钥 d
d = mod_inverse(e, et)

m = 42  # 原始消息
c = encrypt(m, e, n)  # 加密
decrypted_m = decrypt(c, d, n)  # 解密

print(f"密文 c = {c}, 解密后的消息 m = {decrypted_m}")
